from text_viewer_xml import (TextViewerAPIXML)
from text_viewer import (get_unicode_from_xml,)
import xml.etree.ElementTree as ET
from django.conf import settings
import re

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
                docids['kiln_ref'], unicode(loc).rjust(5, '0')))

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
            ret.append('.//div[@id="section-{}"]'.format(unicode(loc)))

    return ret


def get_location_translated(doc_from, location_from, doc_to):
    global docs_sections
    # ret = location_from
    ret = []

    if docs_sections is None:
        tvof = TextViewerAPITvof()
        docs_sections = tvof.compute_section_mappings()

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
            'location_from_chunk': lambda c: unicode(c.attrib['data-n'])
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
            'location_from_chunk': lambda c: unicode(int(c.attrib['id'][-5:]))
        },
        {
            'slug': 'whole',
            'label': 'Whole Text',
            'xpath': './/div[@class="tei body"]',
        },
    ]

    def compute_section_mappings(self):
        '''
        Build a mapping among the units from all documents
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
                m = re.search(ur'ed([^_]+)_(\d+)',
                              correpondance.attrib.get(attrib, ''))
                if m:
                    pair.append([m.group(1), str(int(m.group(2)))])

            if len(pair) == 2:
                # pair = [['Royal20D1', 00544_01], ['fr20125', 00621]]

                for i in [0, 1]:
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

        # print ret

        return ret

    def is_location_visible(self, location_xml, doc_slug, view_slug,
                            location_type_slug):
        ret = True
        filters = getattr(
            settings,
            'TEXT_VIEWER_DOC_FILTERS',
            {}
        ).get(self.client)
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
            conventions = get_unicode_from_xml(conventions_xml)
            conventions = re.sub(ur'id="([^"]+)"', ur'class="\1"', conventions)

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

    def get_location_info_from_xml(self, xml, location_type):
        ret = {'slug': '', 'label': '?', 'label_long': '?'}

        if location_type['slug'] == 'section':
            ret = {
                'slug': xml.attrib.get('data-n', '0'),
                'label_long': xml.attrib.get('data-n', '') + '. ' +
                xml.attrib.get('data-type', 'untitled').replace('_', ' '),
            }
            ret['label'] = ret['label_long']

        if location_type['slug'] == 'paragraph':
            # TODO: move this to a class?

            #             print '-' * 40
            #             print get_unicode_from_xml(xml)

            # id="edfr20125_00588"
            number = xml.attrib.get('id', '')
            number = re.sub(ur'^.*_0*(\d+)$', ur'\1', number)

            rubric = xml.find('.//*[@class="tei-rubric"]')
            if rubric is not None:
                label_long = rubric.text
                for e in rubric:
                    if e.tag not in ['a', 'div']:
                        label_long += ET.tostring(e)
                label_long = self.compress_html(label_long)

                # TODO: move this to TVOF
                # capitalise letters in the location label, HTML <option>
                # doesn't support css styling on nested elements.
                def rep(match):
                    ret = match.group(1).title()
                    return ret
                label_long = re.sub(
                    ur'<span class="tei-critToUpper">([^<]+)</span>',
                    rep,
                    label_long)

                ret = {
                    'slug': number,
                    'label': number,
                    'label_long': label_long,
                }

        return ret
