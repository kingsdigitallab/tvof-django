from .text_viewer_xml import (TextViewerAPIXML)
import xml.etree.ElementTree as ET
from django.conf import settings
import re
from . import utils

# TODO: move this to another package, outside of generic text_viewer
'''
    http://localhost:8000/textviewer/api/?jx=1
    http://localhost:8000/textviewer/api/Fr20125/?jx=1
    http://localhost:8000/textviewer/api/Fr20125/interpretive/section/588/?jx=1
'''

# TODO: ALL this info should come for the TEI documents
# but too many files managed by editors already so
# not possible at the moment to make that change.
DOCUMENT_IDS_ARRAY = [
    {
        # this document slug in the Web API
        # TODO: at the moment it MUST be = to kiln_file
        'slug': 'Fr20125',
        # name of the file in kiln (used to request kiln)
        'kiln_file': 'Fr20125',
        # document part of the internal reference system in the TEI
        # e.g. name of segment, paragragh, ...
        'kiln_ref': 'fr20125',
        # the public label in the text viewer
        # TODO: not consistent, /api/ uses this
        # but /api/<slug>/ uses the label found in the TEI
        'label': 'Fr20125',
    },
    {
        'slug': 'Royal',
        'kiln_file': 'Royal',
        'kiln_ref': 'Royal20D1',
        'label': 'Royal 20 D I',
    },
]

DOCUMENT_IDS = {}
for docids in DOCUMENT_IDS_ARRAY:
    DOCUMENT_IDS[docids['slug'].lower()] = docids
    DOCUMENT_IDS[docids['kiln_file']] = docids
    DOCUMENT_IDS[docids['kiln_ref'].lower()] = docids

docs_sections = None


def _get_xpath_from_location(slug, view, location_type, location,
                             synced_with):
    ret = []

    if synced_with:
        if synced_with['document'] == slug:
            # synced with same doc
            location = synced_with['location']
        else:
            # synced with different document
            if location_type == 'paragraph' and\
                    synced_with['location_type'] == location_type:
                location = get_location_translated(
                    synced_with['document'], synced_with['location'], slug)

    docids = DOCUMENT_IDS.get(slug.lower(), None)
    if docids:
        if not isinstance(location, list):
            location = [location]
        for loc in location:
            ret.append('.//div[@id="ed{}_{}"]'.format(
                docids['kiln_ref'], str(loc).rjust(5, '0')))

    return ret


def _get_xpath_from_location_section(slug, view, location_type, location,
                                     synced_with):
    ret = []

    if synced_with:
        # TODO: error if we don't sync with location_type = section
        location = synced_with['location']

    docids = DOCUMENT_IDS.get(slug.lower(), None)
    if docids:
        if not isinstance(location, list):
            location = [location]
        for loc in location:
            ret.append('.//div[@id="section-{}"]'.format(str(loc)))

    return ret


def get_location_translated(doc_from, location_from, doc_to):
    '''Returns the sync'ed location from one doc to another
    e.g. para 600 in fr could be 540 in royal
    This function return an array of unit numbers e.g. [540, 541].'''
    global docs_sections
    # ret = location_from
    ret = []

    if docs_sections is None:
        tvof = TextViewerAPITvof()
        docs_sections = tvof.compute_section_mappings()
        if 0:
            # for inspection/debugging only
            import json
            print('sync.json')
            with open('sync.json', 'wt') as fh:
                fh.write(json.dumps(docs_sections))

    units = docs_sections.get(doc_from + '_' + doc_to, None)
    if units:
        location_to = units.get(location_from, None)
        if location_to:
            # TVOF 108
            # fill in the gaps, e.g. [621, 623] => [621, 622, 623]
            # assumes all para have are numbers only, i.e. no 123a, 123b
            ret = [str(n) for n in range(
                int(location_to[0]), int(location_to[-1]) + 1)]

    return ret


class TextViewerAPITvof(TextViewerAPIXML):
    '''
    Implementation of TextViewerXML specific to TVoF project and texts.
    '''

    '''
    <div class="section" id="section-6" data-n="6" data-type="Eneas">
        <div id="edfr20125_00588"
        data-corresp="#edRoyal20D1_00525_01 #edRoyal20D1_00525_04">
    '''
    location_types = [
        {
            'slug': 'section',
            'label': 'Section',
            # used to find default/first chunk
            # used to extract all locations
            'xpath': './/div[@class="section"]',
            # used to locate a chunk from a location
            'xpath_from_location': _get_xpath_from_location_section,
            # used to get location of a default chunk
            'location_from_chunk': lambda c: str(c.attrib['data-n'])
        },
        {
            'slug': 'paragraph',
            'label': 'Paragraph',
            # used to find default/first chunk
            # used to extract all locations
            'xpath': './/div[@class="section"]/div[h4]',
            # used to locate a chunk from a location
            'xpath_from_location': _get_xpath_from_location,
            # used to get location of a default chunk
            'location_from_chunk': lambda c: str(int(c.attrib['id'][-5:]))
        },
        {
            'slug': 'whole',
            'label': 'Whole Text',
            'xpath': './/div[@class="tei body"]',
        },
    ]

    def get_sublocationid_from_address(self, address, chunk):
        '''
        :param address: e.g. 'Fr20125/interpretive/paragraph/588/2'
        :param chunk: chunk of xml content that contains the id
        :return: 'edfr20125_00588_02'
        '''
        ret = ''
        parts = self.get_address_parts(address)

        para = parts.get('location', '')
        seg = parts.get('sublocation', '')
        if para and seg:
            pattern = 'id="([^"]+0*{}_0*{})"'.format(para, seg)
            m = re.search(pattern, chunk)
            if m:
                ret = m.group(1)
                # attrib = 'id="'+ret+'"'
                # chunk = chunk.replace(attrib, attrib+' cla')

        return ret, chunk

    def compute_section_mappings(self):
        '''
        Build a mapping among the units from Royal and its corresp(s)
        e.g.
        ret = {
            'Royal_Fr20125': {
                '544': ['621', '623'],
                ...
            },
            'Fr20125_Royal': {
                '621': ['544'],
                ...
            }
        }
        '''
        ret = {}

        # <span data-corresp="#edfr20125_00621" id="edRoyal20D1_00544_01">
        xml = self.fetch_xml_from_kiln('Royal', 'semi-diplomatic')
        for correpondance in xml.findall('.//*[@data-corresp]'):
            # pair = [edRoyal20D1_00544_01, #edfr20125_00621]
            pair = []
            for attrib in ['id', 'data-corresp']:
                m = re.search(r'ed([^_]+)_(\d+)',
                              correpondance.attrib.get(attrib, ''))
                if m:
                    pair.append([m.group(1), str(int(m.group(2)))])

            if len(pair) == 2:
                # pair = [['Royal20D1', '00544'], ['fr20125', '00621']]

                for i in [0, 1]:
                    # k = 'Royal_Fr20125' (for i = 0)
                    k = '_'.join([DOCUMENT_IDS[p[0].lower()]['slug']
                                  for p in pair])
                    if k not in ret:
                        ret[k] = {}
                    if pair[0][1] not in ret[k]:
                        ret[k][pair[0][1]] = []
                    if pair[1][1] not in ret[k][pair[0][1]]:
                        ret[k][pair[0][1]].append(pair[1][1])

                    # now map the other way round
                    pair[0], pair[1] = pair[1], pair[0]

        if 1:
            self._report_gap_in_mappings(ret)

        return ret

    def _report_gap_in_mappings(self, mappings):
        '''For debugging purpose, we report all the ids from Royal
        that have no mapping with Fr
        '''

        # a block is a range if ids with no mapping to Fr
        blocks = [[]]
        for i in range(1, 1500):
            if str(i) not in mappings['Royal_Fr20125']:
                if not blocks[-1]:
                    blocks[-1].append(i)
            else:
                if blocks[-1]:
                    if i - 1 not in blocks[-1]:
                        blocks[-1].append(i - 1)
                    blocks.append([])

        if blocks[-1]:
            print('WARNING: these ids in Royal are not mapped to Fr: {}'.format(
                repr(blocks)))

    def set_chunk_not_found_error(self, xpath=None):
        message = 'Chunk not found: {}'.format(
            self.get_requested_address()
        )

        if self.synced_with:
            address = '/'.join(
                self.get_list_from_address_parts(self.synced_with)
            )
            tv_errors = getattr(settings, 'TV_NOT_FOUND_ERRORS', [])
            for anerror in tv_errors:
                if re.search(anerror[0], address):
                    message = anerror[1]
                    break

        self.add_error(
            'notfound',
            message,
            'XPATH = {}'.format(xpath)
        )

    def is_location_visible(self, location_xml, doc_slug, view_slug,
                            location_type_slug):
        '''Returns True if the location can be shown on the site
        according to the filters set in settings.TEXT_VIEWER_FILTERS_PATH'''
        ret = True

        filters = utils.get_text_viewer_filters()
        if filters:
            filter = filters.get(doc_slug, None)
            if filter is not None:
                filter = filter.get(view_slug, None)
            if filter is not None:
                # filter is a white list of section slugs
                # filter = ['6', '6bis']
                if location_type_slug == 'section':
                    ret = location_xml.attrib.get('data-n') in filter
                if location_type_slug == 'paragraph':
                    ret = location_xml.attrib.get('data-section') in filter
        return ret

    def request_documents(self):
        # TODO: kiln pipeline for returning all texts under a path
        self.response = {'documents': self.fetch_documents()}

    def fetch_documents(self):
        # TODO: kiln pipeline for returning all texts under a path
        ret = DOCUMENT_IDS_ARRAY

        return ret

    def get_notational_conventions(self, xml, view_slug):
        conventions = ''

        conventions_xml = xml.find('.//div[@id="text-conventions"]')
        if conventions_xml is not None:
            conventions = utils.get_unicode_from_xml(conventions_xml)
            conventions = re.sub(r'id="([^"]+)"', r'class="\1"', conventions)

        return conventions

    def get_doc_title(self, xml):
        ret = super(TextViewerAPITvof, self).get_doc_title(xml)

        patterns = [
            'TVOF transcription template',
            'TVOF edition',
        ]
        for pattern in patterns:
            ret = ret.replace(pattern, '').strip()

        return ret

    def read_all_sections_data(self):
        '''
        For each section in Fr and Royal,
        returns the sections number, name and first para-number.
        '''
        ret = {}

        for doc in DOCUMENT_IDS_ARRAY:
            sections = []
            xml = self.fetch_xml_from_kiln(doc['kiln_file'], 'semi-diplomatic')
            for section_node in xml.findall('.//div[@class="section"]'):
                section = {
                    'number': section_node.attrib.get('data-n', ''),
                    'name': section_node.attrib.get('data-type', '')
                }
                para = section_node.find('div[h4]')
                if para is not None:
                    section['para'] = para.attrib.get('id', '')
                sections.append(section)
            ret[doc['slug']] = sections

        return ret

    def get_location_info_from_xml(self, xml, location_type):
        ret = {'slug': '', 'label': '?', 'label_long': '?'}

        if location_type['slug'] == 'section':
            ret = {
                'slug': xml.attrib.get('data-n', '0'),
                'label_long': xml.attrib.get('data-n', '') + '. ' +
                xml.attrib.get('data-type', 'untitled').replace('_', ' '),
            }
            ret['label'] = ret['label_long']

        '''
        <h4 class="tei-rubric">958.  Que la <span>a cele</span> dure bataille
        n'eussent mestier coart chevalier<span class="tei-note tei-type-note
        tei-subtype-source" data-tei-subtype="source"
        id="edfr20125_00958_peach"><span class="note-text">Orose, <em>HaP</em>,
        <a class="bibliography" href="Pavlidès_1989">Pavlidès (1989)</a></span>
        </span></h4>

        958. Que la a cele dure bataille n'eussent mestier coart chevalier
        '''
        rubric_hidden_classes = re.compile(
            r'\b(bibliography|tei-note|tei-pb|tei-cb)\b'
        )
        if location_type['slug'] == 'paragraph':
            # TODO: move this to a class?
            # id="edfr20125_00588"
            number = xml.attrib.get('id', '')
            number = re.sub(r'^.*_0*(\d+)$', r'\1', number)

            rubric = xml.find('.//*[@class="tei-rubric"]')
            if rubric is not None:

                label_long = rubric.text
                for e in rubric:
                    if (rubric_hidden_classes.search(e.attrib.get('class', ''))
                            is None):
                        label_long += utils.get_unicode_from_xml(e)
                    label_long += (e.tail or '')
                label_long = self.compress_html(label_long)

                # TODO: move this to TVOF
                # capitalise letters in the location label, HTML <option>
                # doesn't support css styling on nested elements.
                def rep(match):
                    ret = match.group(1).title()
                    return ret

                label_long = re.sub(
                    r'<span class="tei-critToUpper">([^<]+)</span>',
                    rep,
                    label_long)

                ret = {
                    'slug': number,
                    'label': number,
                    'label_long': label_long,
                }

        return ret

    def prepare_view_version(self, chunk, view):
        ret = chunk

        if view == 'interpretive':
            utils.remove_xml_elements(ret, './/span[@data-tei-type="gloss"]')

        return ret

    def prepare_print_version(self, chunk, notes_info):
        self.transform_to_print_version(chunk)
        self.extract_notes_from_chunk(chunk, notes_info)

    def transform_to_print_version(self, chunk):
        '''
        Minor conversions of the XML for the print version
        '''
        # ac-337: make ms reading inline
        # <span class="tei-corr" data-sic=" aidier aidier">aidier</span>
        # =>
        # <span class="tei-corr" data-sic=" aidier aidier">aidier</span>
        # <span class="corr-sic">aidier aidier</span>
        from .utils import findall_in_etree
        for corr in findall_in_etree(chunk, './/span[@data-sic]'):
            sic = ET.Element('span')
            sic.set('class', 'corr-sic')
            sic.text = corr['el'].attrib.get('data-sic')
            sic.tail = (corr['el'].tail or '')
            corr['el'].tail = ''
            corr['parent'].insert(corr['index'] + 1, sic)

    def extract_notes_from_chunk(self, chunk, notes_info):
        '''
        Move notes to the end of the document (like footnotes).
        Insert inline references from the text.
        Both will link to each other.

        Each notes receives a unique handle based on a sequential number
        suffixed with a letter indicating the type of note:
            S: source
            T: trad(ition)
            G: gen(eral)
            A: gloss / note de lecteur medieval / annotation
            ?: unspecified / unknown type

        eg. of a note block to extract

        <div class="tei-note tei-type-note tei-subtype-source"
            data-tei-subtype="source" id="edfr20125_0590_peach">
            <div class="note-text">
                [...]HTML
            </div>
        </div>

        In the code below:
            <note_ref> is the inline reference to the footnote;
            <note> is the html of a footnote;
            <notes_info> is populated with the list of all <note>s;
        '''

        def get_location_string_from_note(note_xml):
            '''
            note_xml: a xml node for a note (see example above)
            return §590 for id="edfr20125_0590_peach"
            return §509.14 for id="edfr20125_0590_14_sycamore"
            '''
            ret = ''
            noteid = note_xml.attrib.get('id', '')
            if noteid:
                parts = re.findall(
                    r'_0*(\d+)(?=_)', noteid
                )
                if parts:
                    ret = '§' + '.'.join(parts)

            return ret

        # nested loop is b/c ET needs parent to remove child but
        # there is no .parent() function
        for parent in chunk.findall('.//*[@class="note-text"]/../..'):
            for note in parent.findall('.//*[@class="note-text"]/..'):
                note_tail = note.tail
                note.tail = ''

                # create a unique note handle
                note_number = len(notes_info['notes']) + 1

                note_cat_from_subtype = {
                    '': '?',
                    'source': 'S',
                    'trad': 'T',
                    'gen': 'G',
                }
                note_subtype = note.attrib.get('data-tei-subtype', '')
                note_cat = note_cat_from_subtype.get(note_subtype, '')

                if note.attrib.get('data-tei-type', '') == 'gloss':
                    note_cat = 'A'  # as in annotation

                # unique handle for that note
                note_handle = '{}:{}'.format(note_number, note_cat)

                note_text = note.find('*[@class="note-text"]')

                note_text.text = note_text.text or ''
                if not note_text.text:
                    print('WARNING: empty note ({})'.format(note_number))

                note_prefixes = []

                # the anchor / handle
                note_prefixes.append(
                    '<a class="note-anchor" id="note-{}" '
                    ' href="#ref-{}">{}</a>'.
                    format(
                        note_number,
                        note_number,
                        note_handle,
                    )
                )

                # ac-332.1: add location at the beginning of footnote
                # chapter number.seg number, e.g. §526.14
                note_location = get_location_string_from_note(note) or\
                    get_location_string_from_note(parent)
                if note_location:
                    note_prefixes.append(
                        '<span class="note-location">{}</span>'.format(
                            note_location
                        )
                    )

                # ac-332.3: prepare tooltip/title for some notes
                note_title = ''
                if note_cat in ['A']:
                    hand_code = note.attrib.get('data-tei-resp', '?')
                    hand_name = settings.SHORT_HANDS.get(hand_code, hand_code)
                    if note_text.text:
                        note_text.text = ' « {} »'.format(
                            note_text.text.replace('\n', ' ')
                        )
                    note_title = 'Note de lecteur médiéval ' + \
                        '(main: {}):'.format(
                            hand_name,
                        )
                    note_prefixes.append('<span>{}</span>'.format(note_title))
                    note_title += note_text.text

                # actually insert the handle and location at the beginning
                # of the footnote.
                for i, note_prefix in enumerate(note_prefixes):
                    note_prefix = ET.fromstring(note_prefix)
                    note_text.insert(i, note_prefix)
                # make sure the note text appears after the inserted elements
                note_prefix.tail = note_text.text or ''
                note_text.text = ''

                # print(ET.tostring(note_text))

                # add note to the notes_info
                notes_info['notes'].append(utils.get_unicode_from_xml(note))

                # replace note in chunk with an inline reference
                note.clear()
                note_ref = note
                note_ref.tail = note_tail
                note_ref.tag = 'a'
                note_ref.attrib['class'] = 'note-ref tei-subtype-{}'\
                    .format(note_subtype)
                note_ref.attrib['href'] = '#note-{}'.format(note_number)
                note_ref.attrib['id'] = 'ref-{}'.format(note_number)
                if note_title:
                    note_ref.attrib['title'] = note_title
                note_ref.text = note_handle
                # print(note.tail)
                # parent.remove(note)
