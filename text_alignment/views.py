# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render
from text_viewer.kiln_requester import CachedRequesterKiln
from django.core.cache import caches
from api_vars import API_Vars
from text_alignment.api_vars import get_key_from_name
from cms.templatetags.cms_tags import json


def view_alignment(request, path):
    # e.g. /textviewer/
    alignment = Alignment()
    return alignment.process_request(request, path)


class Alignment(object):
    '''
    Responds to user and ajax requests with a list of paragraphs
    for a given range (e.g. sections) and a given set of manuscripts.

    Sources:
        * alignment file (XML/TEI) obtained from Kiln then cached
        * converted into python dictionary and cached
    '''

    def process_request(self, request, path):
        '''
        If user request, we regenerate the python dictionary from the XML file.
        If ajax request, we read the dictionary from the cache.
        The response contains only the requested data from the dictionary.
        '''
        is_fragment = request.GET.get('js', 0)
        if is_fragment:
            # ajax request
            return self.get_alignment_fragment(request, path)

        alignment_data = self.fetch_all_alignment_data(True)
        config = self.get_config(request, path, alignment_data)
        context = {
            'config': config.get_list()
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
            'config': config.get_list(),
            'html': template.render(context),
            'qs': config.get_query_string(),
        }

        from django.http import JsonResponse
        return JsonResponse(json_res)

    def set_context_table(self, context):
        # easier for template to check which fields to show in table
        for k in context['config'].get('fields'):
            context['fields_%s' % k] = 1

    def set_context_bars_old(self, context):
        for k in context['config'].get('fields'):
            context['fields_%s' % k] = 1

    def set_context_bars(self, context):
        for k in context['config'].get('fields'):
            context['fields_%s' % k] = 1

    def set_context_column(self, context):
        for k in context['config'].get('fields'):
            context['fields_%s' % k] = 1

    def fetch_all_alignment_data(self, nocache=False):
        '''
        Cache and returns a python dictionary with ALL alignment data.
        If the dictionary is not in the django cache or <nocache> is True,
        we request the alignment file (XML) from Kiln then convert it to
        a dictionary.

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

        possible_mss = getattr(settings, 'ALIGNMENT_MSS', None)

        ret = [
            {
                'key': 'view',
                'default': 'table',
                # 'options': ['table', 'bars', 'bars_v2', 'viztest'],
                'options': ['table', 'bars', 'column'],
                'type': 'single',
            },
            {
                'key': 'sections',
                'default': ['eneas'],
                'options': alignment_data['sections'],
                'type': 'multi',
            },
            {
                'key': 'unit',
                'default': 'para',
                'options': ['section', 'para'],
                'type': 'single',
                'hidden': 1,
            },
            {
                'key': 'mss',
                'default': ['fr-20125', 'royal-20-d-1'],
                'options': [
                    ms['name']
                    for ms
                    in alignment_data['mss']
                    if (not possible_mss) or
                    get_key_from_name(ms['name']) in possible_mss
                ],
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
        '''
        Remove all non requested data from <alignment_data> and returns it.

        <alignment_data>: the whole alignment data as a python dictionary
        <config>: requested data
        '''
        ret = alignment_data

        sections = config.get('sections')
        mss = config.get('mss', prop='name')

        for i in range(len(ret['paras']) - 1, -1, -1):
            # remove unwanted sections
            if sections and ret['paras'][i]['section'].lower() not in sections:
                del ret['paras'][i]
                continue
            # remove unwanted manuscripts
            if mss:
                for ms_name in ret['paras'][i]['mss'].keys():
                    if ms_name not in mss:
                        del ret['paras'][i]['mss'][ms_name]

        return ret

    def get_dict_from_alignemnt_xml(self, xml_string):
        '''
        Convert the XML alignment file into a python dictionary.

        paras: [
            'id': 'fr20125_00001',
            'section': 'Genesis',
            'mss': {
                Fr 20125:
                    {
                        'ms_name': 'Fr 20125',
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
        mss: [
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
#         fields = {}
        sections = []

        # extract, normalise and merge the manuscript names
        # <seg type="ms_name">Vienna</seg>
        ms_names = self.get_ms_names_from_xml(root)

        def get_nat_parts(astring):
            ret = []
            for p in re.findall(ur'(\d+|\D+)', astring):
                try:
                    p = int(p)
                except Exception:
                    pass
                ret.append(p)

            return ret

        # multivalued_seg_types = []
        multivalued_seg_types = ['rubric']
        dict_seg_types = ['locus', 'note', 'rubric']

        # extract the paras
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
                            typ = seg.attrib.get('type')
                            text = seg.text

                            if text and len(text) <= 3 and typ in ['rubric']:
                                continue

                            if text:
                                text = re.sub(r'\s+', r' ', text)

                            if typ in dict_seg_types:
                                val = {
                                    re.sub(r'\{.*\}', r'', k): v
                                    for k, v
                                    in seg.attrib.items()
                                }
                                val['t'] = text
                                del val['type']
                            else:
                                val = text

                            if typ in multivalued_seg_types:
                                if typ in para_ms:
                                    para_ms[typ].append(val)
                                else:
                                    para_ms[typ] = [val]
                            else:
                                para_ms[typ] = val
#                             if seg.text is not None:
#                                 fields[seg.attrib.get('type')] = seg.text

                        ms_name = para_ms['ms_name'] or 'UNSPECIFIED'
                        # take normalised name
                        ms_name = ms_names.get(ms_name, ms_name)

                        para['mss'][ms_name] = para_ms

                        location_clean = (
                            para_ms.get('location') or 'none'
                        ).lower().strip()
                        if 'absent' in location_clean:
                            para_ms['absent'] = 1
                        if location_clean == '':
                            # NO LONGER USED
                            para_ms['absent'] = 2
                        if location_clean == 'none':
                            para_ms['absent'] = 3

                        if ms_name not in mss:
                            mss[ms_name] = {
                                'name': ms_name, 'para_count': 0}

                        if not para_ms.get('absent', False):
                            mss[ms_name]['para_count'] += 1

                            # detect displaced text
                            # 12ra
                            location = para_ms.get('location')

                            if 0 and not re.match(r'^\d+[rv][ab]?$', location):
                                print u'FORMAT: {}, {} : \'{}\''.format(
                                    ms_name, para['id'], re.sub(
                                        ur'(?musi)\s+', ' ', location)
                                )

                            last_location = mss[ms_name].get('location', None)
                            if last_location and\
                                (get_nat_parts(last_location) >
                                 get_nat_parts(location)) and\
                                    (last_location.strip('ab') != location):

                                s = u'{0:5s} {1:15s} {2:20.20s} {3:20.20s}'
                                if 0:
                                    print s.format(
                                        para['id'], ms_name,
                                        last_location, location
                                    )

                            mss[ms_name]['location'] = location

                    paras.append(para)

        ret = {
            'paras': paras,
            'mss': sorted(mss.values(), key=lambda ms: ms['name'].lower()),
            'sections': sections,
        }

        print len(json(paras))

        return ret

    def get_ms_names_from_xml(self, root):
        '''
        Returns a mapping between all unique MS names
        found in root and normalised names.
        e.g. {Dijon -> Dijon 262, Dijon262 -> Dijon 262, ...}
        '''

        # get all unique names
        ms_names = {}
        for seg in root.findall('.//seg[@type="ms_name"]'):
            name = seg.text
            if name:
                ms_names[name] = ms_names.get(name, 0) + 1

        # now normalise the names
        # Fr15455 | Fr 15455, Marciana_fr_Z_II | Marciana Fr Z Ii
        import re
        for name in ms_names:
            normalised = name.replace(
                '-',
                ' ').replace(
                '_',
                ' ').lower().strip()
            normalised = re.sub(ur'(?i)([a-z])(\d)', ur'\1 \2', normalised)
            normalised = normalised.title()
            ms_names[name] = normalised

        # merge
        # e.g. Dijon -> Dijon 562
        for name, normalised in ms_names.items():
            if ' ' not in normalised:
                candidates = [
                    v
                    for v
                    in set(ms_names.values())
                    if v.startswith(normalised + ' ')
                ]
                c = len(candidates)
                if c == 1:
                    ms_names[name] = candidates[0]
                elif c > 2:
                    print 'WARNING: ambiguous MS name: %s (%s ?)' %\
                        (name, ', '.join(candidates))
                elif c == 0:
                    print 'INFO: MS name without number: %s' % name

        # print '\n'.join(['%s | %s' % (k, v) for k, v in ms_names.items()])

        return ms_names


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
