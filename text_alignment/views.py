# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render
from text_viewer.text_viewer_tvof import TextViewerAPITvof
from text_viewer.kiln_requester import CachedRequesterKiln

'''
http://localhost:9999/backend/preprocess/alists/TVOF_para_alignment.xml

<div type="alignments">
    <milestone unit="section" n="1" type="Genesis"/>
    <div type="alignment" xml:id="fr20125_00001">
        <ab type="ms_instance" subtype="base" corresp="#edfr20125_00001"
            computed-corresp="#edfr20125_00001">
            <seg type="ms_name">Fr20125</seg>
            <seg type="rubric">
            Ci comence li prologues du liure des estories Rogier [et] la
            porsiuance
            </seg>
            <seg type="location">1ra</seg>
            <seg type="note">
            Inhabited initial, 10 lines, with gold and partial border
            </seg>
            <seg type="verse">284 lines</seg>
        </ab>
        <ab type="ms_instance">
            <seg type="ms_name">Add 19669</seg>
            <seg type="rubric"/>
            <seg type="location">absent</seg>
        </ab>
        <ab type="ms_instance">
            <seg type="ms_name">Vienna</seg>
            <seg type="rubric">[no rubric]</seg>
            <seg type="location">1ra</seg>
            <seg type="note">
            Incipit: 'Seignors ie ai oi retraire condoit· ides bie[n] dir [et]
            faire·'
            </seg>
        </ab>
'''


def fetch_alignment_data(nocache=False):
    from django.core.cache import caches
    cache = caches['kiln']

    ret = cache.get('alignment_data')

    if ret:
        return ret

    res = None
    if not nocache:
        kiln = CachedRequesterKiln()
        url = '{}/backend/preprocess/alists/TVOF_para_alignment.xml'.format(
            settings.KILN_BASE_URL
        )
        res = kiln.request(url)

    if res:
        '''
        paras = [
            'id': 'fr20125_00001',
            'section': 'Genesis',
            'mss': {
                Fr20125:
                    {
                        'ms_name': 'Fr20125',
                        'note': """Inhabited initial, 10 lines, with gold and
                            partial border""",
                        'verse': '284 lines',
                        'rubric': """Ci comence li prologues du liure des
                            estories Rogier [et] la porsiuance""",
                        'location': '1ra'
                    },
                [...]
            },
            [...]
        ]
        mss = [
            {
                'name': 'Fr20125',
                'para_count': 0,
            },
            [...]
        ]
        '''

        import re
        res = re.sub('xmlns\s*=\s*".*?"', '', res)
        res = re.sub('xml:\s*(\w+)\s*=', r'\1=', res)
        import xml.etree.ElementTree as ET
        root = ET.fromstring(res)
        alignments_set = root.findall('.//div[@type="alignments"]')

        section = 'UNSPECIFIED'

        paras = []
        mss = {}
        fields = {}

        for alignments in alignments_set:
            for element in alignments:
                if element.tag == 'milestone' and element.attrib.get(
                        'unit') == 'section':
                    section = element.attrib.get('type', 'UNSPECIFIED')
                elif element.tag == 'div' and\
                        element.attrib.get('type') == 'alignment':
                    para = {
                        'mss': {},
                        'section': section,
                        'id': element.attrib.get('id')
                    }
                    for manuscript in element:
                        para_ms = {}
                        for seg in manuscript:
                            para_ms[seg.attrib.get('type')] = seg.text
                            if seg.text is not None:
                                fields[seg.attrib.get('type')] = seg.text
                        ms_name = para_ms['ms_name']
                        para['mss'][ms_name] = para_ms
                        if (para_ms.get('location') or '').lower(
                        ).strip() in ['', 'absent']:
                            para_ms['absent'] = 1

                        if ms_name not in mss:
                            mss[ms_name] = {'name': ms_name, 'para_count': 0}
                        mss[ms_name]['para_count'] += 1

                    paras.append(para)

        ret = {
            'paras': paras,
            'mss': sorted(mss.values(), key=lambda ms: -ms['para_count']),
        }

        cache.set('alignment_data', ret)

    return ret


def view_alignment(request, path):
    # e.g. /textviewer/

    alignment_data = fetch_alignment_data()

    alignment_data['paras'] = alignment_data['paras'][:5]

    context = {
        'alignment_data': alignment_data,
    }
    return render(request, 'text_alignment/alignment.html', context)


# TODO: convert to django rest framework?
def view_text_viewer_api(request, path):
    viewer = TextViewerAPITvof()
    viewer.process_request(request, path)
    return viewer.get_response_json()
