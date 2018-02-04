# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render
from text_viewer.kiln_requester import CachedRequesterKiln
from django.core.cache import caches
from api_vars import API_Vars


def view_alignment(request, path):
    # e.g. /textviewer/
    alignment = Alignment()
    return alignment.process_request(request, path)


class Alignment(object):

    def process_request(self, request, path):
        is_fragment = request.GET.get('js', 0)
        if is_fragment:
            return self.get_alignment_fragment(request, path)

        alignment_data = self.fetch_all_alignment_data(True)
        config = self.get_config(request, path, alignment_data)
        context = {
            'config': config.get_dict()
        }

        return render(request, 'text_alignment/alignment.html', context)

    def get_alignment_fragment(self, request, path):
        '''
        ! None or empty value in request.GET means default value from <config>
        ! None or empty value in <config> means ALL
        '''

        # Get all alignment data from kiln XML into a dictionary
        # this can be cached.
        alignment_data = self.fetch_all_alignment_data()

        # Config holds all config parameters for the visualisation
        # and contains the selected values coming from the user request
        config = self.get_config(request, path, alignment_data)

        # Filter alignment data according to user request
        alignment_data = self.get_requested_alignment_data(
            alignment_data,
            config
        )

        context = {
            'config': config,
            'params': config.get_dict(),
            'alignment_data': alignment_data
        }

        selected_view = config.get('view', True)

        getattr(self, 'set_context_%s' % selected_view)(context)

        template_path = 'text_alignment/views/%s.html' % selected_view
        from django.template.loader import get_template
        template = get_template(template_path)
        json_res = {
            'config': config.get_dict(),
            'html': template.render(context),
            'qs': config.get_query_string(),
        }

        from django.http import JsonResponse
        return JsonResponse(json_res)

    def set_context_table(self, context):
        for k in context['config'].get('fields'):
            context['fields_%s' % k] = 1

    def fetch_all_alignment_data(self, nocache=False):
        '''
        {
            mss: []
            paras: []
            sections: []
        }
        '''
        cache = caches['kiln']

        # get from cache
        ret = None
        if not nocache:
            ret = cache.get('alignment_data')
            if ret:
                return ret

        # fetch alignment XML from Kiln
        kiln = CachedRequesterKiln()
        url = '{}/backend/preprocess/alists/TVOF_para_alignment.xml'.format(
            settings.KILN_BASE_URL
        )
        res = kiln.request(url)
        if not res:
            raise Exception('Could not fetch alignment XML from Kiln')

        # extract data from XML
        ret = self.get_dict_from_alignemnt_xml(res)

        # save in cache
        cache.set('alignment_data', ret)

        return ret

    def get_config(self, request, path, alignment_data):
        ret = API_Vars(self.get_config_schema(alignment_data))

        ret.reset_vars_from_request(request)

        return ret

    def get_config_schema(self, alignment_data):
        # cache = caches['kiln']

        ret = [
            {
                'key': 'view',
                'default': 'table',
                'options': ['table', 'bars'],
                'type': 'single',
            },
            {
                'key': 'sections',
                'default': ['Eneas'],
                'options': alignment_data['sections'],
                'type': 'multi',
            },
            {
                'key': 'unit',
                'default': 'para',
                'options': ['section', 'para'],
                'type': 'single',
            },
            {
                'key': 'mss',
                'default': ['Fr20125', 'Royal_20_D_1'],
                'options': [ms['name'] for ms in alignment_data['mss']],
                'name': 'Manuscripts',
                'type': 'multi',
            },
            {
                'key': 'paras',
                # 'default': None,
                'options': ['NUMBER'],
                'name': 'Paragraphs',
                'type': 'number_range',
                'hidden': 1,
            },
            {
                'key': 'fields',
                'default': ['locus', 'rubric', 'verse'],
                'options': ['locus', 'rubric', 'verse', 'note'],
                'name': 'Metadata fields',
                'type': 'multi',
            },
        ]

        # cache.set('alignment_config_options', ret)
        return ret

    def get_requested_alignment_data(self, alignment_data, config):
        ret = alignment_data

        sections = config.get('sections')
        mss = config.get('mss')

        print config
        print mss

        # filter by section
        for i in range(len(ret['paras']) - 1, -1, -1):
            if sections and ret['paras'][i]['section'].lower() not in sections:
                del ret['paras'][i]
                continue
            if mss:
                for ms_name in ret['paras'][i]['mss'].keys():
                    if ms_name.lower() not in mss:
                        del ret['paras'][i]['mss'][ms_name]

        # only keep requested mss and preserve the order
        if mss:
            mss2 = []
            for ms in mss:
                for ms2 in ret['mss']:
                    if (ms2['name'] or 'undefined').lower() == ms:
                        mss2.append(ms2)
            ret['mss'] = mss2

        return ret

    def get_dict_from_alignemnt_xml(self, xml_string):
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
        res = re.sub('xmlns\s*=\s*".*?"', '', xml_string)
        res = re.sub('xml:\s*(\w+)\s*=', r'\1=', res)
        import xml.etree.ElementTree as ET
        root = ET.fromstring(res)
        alignments_set = root.findall('.//div[@type="alignments"]')

        section = 'UNSPECIFIED'

        paras = []
        mss = {}
        fields = {}
        sections = []

        for alignments in alignments_set:
            for element in alignments:
                if len(paras) > 50000:
                    break

                if element.tag == 'milestone' and element.attrib.get(
                        'unit') == 'section':
                    section = element.attrib.get('type', 'UNSPECIFIED')
                    sections.append(section)
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

                        ms_name = para_ms['ms_name'] or 'UNSPECIFIED'

                        para['mss'][ms_name] = para_ms

                        if (para_ms.get('location') or '').lower(
                        ).strip() in ['', 'absent']:
                            para_ms['absent'] = 1

                        if ms_name not in mss:
                            mss[ms_name] = {
                                'name': ms_name, 'para_count': 0}

                        if not para_ms.get('absent', False):
                            mss[ms_name]['para_count'] += 1

                    paras.append(para)

        ret = {
            'paras': paras,
            # 'mss': sorted(mss.values(), key=lambda ms: -ms['para_count']),
            'mss': sorted(mss.values(), key=lambda ms: ms['name']),
            'sections': sections,
        }

        return ret


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
