# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render
from text_viewer.kiln_requester import CachedRequesterKiln
from django.core.cache import caches
from api_vars import API_Vars
from text_alignment.api_vars import get_key_from_name
from cms.templatetags.cms_tags import json
import re


def view_alignment(request, path):
    # e.g. /textviewer/
    alignment = Alignment()
    return alignment.process_request(request, path)


def get_nat_parts(astring):
    '''
    tokenise a string: return a list of integers and non-integers

    'r4t55y6' => ['r', 4, 't', 55, 'y', '6']

    '''
    ret = []
    for p in re.findall(ur'(\d+|\D+)', astring):
        try:
            p = int(p)
        except Exception:
            pass
        ret.append(p)

    return ret


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

        ret = render(request, 'text_alignment/alignment.html', context)

        return ret

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
        json_res = {
            'config': config.get_list(),
            'html': self.render_template(template_path, context),
            'qs': config.get_query_string(),
        }

        from django.http import JsonResponse
        return JsonResponse(json_res)

    def render_template(self, template_path, context):
        from django.template.loader import get_template
        template = get_template(template_path)
        ret = template.render(context)
        # compress spaces (divide size by 10!)
        ret = re.sub(ur'\n+', r'\n', ret)
        ret = re.sub(ur' +', ' ', ret)
        ret = re.sub(ur'(\n )+', r'\n', ret)
        return ret

    def set_context_base(self, context):
        '''
        Each metadata field selected by the web user in the config
        will be added to the template context as a flag:
        field_XXX = 1
        (e.g. field_locus = 1, field_rubric = 1)
        '''
        # easier for template to check which fields to show in table
        for k in context['config'].get('fields'):
            context['fields_%s' % k] = 1

    def set_context_table(self, context):
        self.set_context_base(context)

    def set_context_bars_old(self, context):
        self.set_context_base(context)

    def set_context_bars(self, context):
        self.set_context_base(context)

    def set_context_column(self, context):
        self.set_context_base(context)

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
                'default': 'column',
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
                'default': ['locus', 'rubric', 'verse', 'variation'],
                'options': ['locus', 'rubric', 'verse', 'variation', 'note'],
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
            {
            'id': 'fr20125_00001',
            'section': 'Genesis',
            'mss': {
                Fr 20125:
                    {
                        'ms_name': 'Fr 20125',
                        'note': [{
                            't': """Inhabited initial, 10 lines, with gold and
                                partial border""",
                            'feat': 'ML',
                        ],
                        'verse': '284 lines',
                        'rubric': [{
                            't': """Ci comence li prologues du liure des
                                estories Rogier [et] la porsiuance""",
                            },
                        ],
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

        # multivalued_seg_types = []
        multivalued_seg_types = ['note', 'rubric']
        dict_seg_types = ['note', 'rubric']

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

                    # a paragraph

                    para = {
                        'mss': {},
                        'section': section,
                        'id': element.attrib.get('id')
                    }
                    for para_manuscript in element:
                        # para info for a particular MS

                        para_ms = self.get_para_ms_from_xml(
                            para_manuscript,
                            dict_seg_types,
                            multivalued_seg_types,
                            para
                        )

                        ms_name = para_ms['ms_name'] or 'UNSPECIFIED'
                        # take normalised name
                        ms_name = ms_names.get(ms_name, ms_name)

                        para['mss'][ms_name] = para_ms

                        if ms_name not in mss:
                            mss[ms_name] = {
                                'name': ms_name, 'para_count': 0
                            }

                        self.clean_para_ms(para_ms, mss, para, ms_name)

                    paras.append(para)

        ret = {
            'paras': paras,
            'mss': sorted(mss.values(), key=lambda ms: ms['name'].lower()),
            'sections': sections,
        }

        print len(json(paras))

        return ret

    def clean_para_ms(self, para_ms, mss, para, ms_name):
        '''Normalise the para_ms dictionary, derive some values
        from encoding conventions and make them more explicit.

        Process location & absence information
        '''

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

    def get_para_ms_from_xml(self, para_manuscript, dict_seg_types,
                             multivalued_seg_types, para):
        '''

        para_manuscript is an ElementTree that represents the following XML:

        <ab type="ms_instance">
            <seg type="abc" atr1='val1'>t1</seg>
            [...]


        The method returns a dictionary:

        {
            'abc': {
                't': 't1',
                'atr1': 'val1',
            },
            [...]
        }
        '''

        ret = {}

        # convert the corresp attribute
        # corresp="#edRoyal20D1_00001_01 #edRoyal20D1_00001_03">
        # => 'corresp': Royal20D1_00001
        corresps = para_manuscript.attrib.get('corresp', None)
        if corresps:
            corresps = re.findall(ur'#ed(\S*_(?:\d{5,5}))', corresps)
            if corresps and corresps[0] != para['id']\
                    and 'fr20125' not in corresps[0]:
                ret['corresp'] = corresps[0]
                # TODO: use this detect fr corresp not pointing
                # to fr reference!
                # i.e. remove the last AND condition
                # print(corresps[0], para['id'])

        # convert all the seg elements under the para_ms
        for seg in para_manuscript:

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
                if typ in ret:
                    ret[typ].append(val)
                else:
                    ret[typ] = [val]
            else:
                ret[typ] = val


#             if seg.text is not None:
#                 fields[seg.attrib.get('type')] = seg.text

        self.expand_para_ms(ret, para)

        return ret

    def expand_para_ms(self, para_ms_dict, para):
        '''
        Expand the dictionary that contains the description of a para in a MS.
        So the frontend code doesn't have to know about acronyms, etc.
        E.g.
        <seg type="variation">PML</seg>
        => {
            [...]
            'variation': 'PML'
        }
        => {
            [...]
            'variation': 'PML'
            'variations': [
                {
                    't': 'Partial material lacuna'
                }
            ]
        }
        '''

        # Expand variations

        # TODO: moved thos hard-coded values to settings/base.py

        variation_names = {
            'pml': 'Partial material lacuna',
            'ml': 'Material lacuna',
        }

        variations = para_ms_dict.get('variation', None)
        if variations:
            para_ms_dict['vars'] = [
                {
                    't': variation_names.get(var, var)
                }
                for var in variations.lower().split(' ')
            ]

            # MT asked us to not show location: None if there is
            # a material lacuna
            if 'ml' in variations.lower().split(' '):
                # print(para_ms_dict)
                if para_ms_dict.get('location') is None:
                    para_ms_dict['location'] = ''

        # Remove empty notes
        # => smaller json data for client
        # & no need to filter in the visualisation
        notes = para_ms_dict.get('note', [])
        for i in range(len(notes) - 1, -1, -1):
            if not notes[i]['t']:
                del notes[i]

        # expand the diff="move" => diff_label="displaced rubric"
        for rubric in para_ms_dict.get('rubric', []):
            diff = rubric.get('diff', '')
            if diff == 'move':
                rubric['diff_label'] = 'Displaced rubric'
            if diff == 'add':
                rubric['diff_label'] = 'Additional rubric'

            # expand the @dest attribute
            # e.g. "-10" -> 'Before fr20125_00025_10'
            dest = rubric.get('dest', '')
            base_seg = para['id'] + '_01'
            if dest:
                modifier = ''
                # -X means BEFORE X
                # But editors mean Before without using -
                # Hence the '1 or' bit
                if 1 or dest[0] == '-':
                    modifier = 'Before '
                    dest = re.sub(ur'^[- ]+', '', dest)
                dest = base_seg[:len(base_seg) - len(dest)] + dest
                rubric['dest_label'] = modifier + dest

        return para_ms_dict

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
