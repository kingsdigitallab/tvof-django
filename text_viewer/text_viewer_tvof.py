from text_viewer_xml import (TextViewerAPIXML)
from text_viewer import (get_unicode_from_xml,)
import xml.etree.ElementTree as ET
import re

# TODO: move this to another package, outside of generic text_viewer
'''
    http://localhost:8000/textviewer/api/?jx=1
    http://localhost:8000/textviewer/api/Fr20125/?jx=1
    http://localhost:8000/textviewer/api/Fr20125/interpretive/section/588/?jx=1
'''


docid_from_document_slug = {
    'Fr20125': 'fr20125',
    'Royal': 'Royal20D1',
}

docs_sections = None


def _get_xpath_from_location(document, view, location_type, location,
                             synced_with):
    ret = []

    if synced_with:
        if synced_with['document'] == document:
            # synced with same doc
            location = synced_with['location']
        else:
            # synced with different document
            if location_type == 'section' and\
                    synced_with['location_type'] == location_type:
                location = get_location_translated(
                    synced_with['document'], synced_with['location'], document)

    docid = docid_from_document_slug.get(document, None)
    if docid:
        if not isinstance(location, list):
            location = [location]
        for loc in location:
            ret.append('.//div[@id="ed{}_{}"]'.format(
                docid, unicode(loc).rjust(5, '0')))

    return ret


def get_location_translated(doc_from, location_from, doc_to):
    global docs_sections
    ret = location_from

    if docs_sections is None:
        tvof = TextViewerAPITvof()
        docs_sections = tvof.compute_section_mappings()

    doc_sections = docs_sections.get(doc_from + '_' + doc_to, None)
    if doc_sections:
        location_to = doc_sections.get(location_from, None)
        if location_to:
            ret = location_to

    print ret

    return ret


class TextViewerAPITvof(TextViewerAPIXML):

    location_types = [
        {
            'slug': 'whole',
            'label': 'Whole Text',
            'xpath': './/div[@class="tei body"]',
        },
        {
            'slug': 'section',
            'label': 'Section',
            # used to find default/first chunk
            # used to extract all locations
            'xpath': './/div[@class="tei body"]/div[h4]',
            # used to locate a chunk from a location
            'xpath_from_location': _get_xpath_from_location,
            # used to get location of a default chunk
            'location_from_chunk': lambda c: unicode(int(c.attrib['id'][-5:]))
        },
    ]

    def compute_section_mappings(self):
        ret = {
            'Royal_Fr20125': {
                # '543': ['607', '608', '609'],
            },
            'Fr20125_Royal': {
                # '543': ['607', '608', '609'],
            }
        }
        xml = self.fetch_xml_from_kiln('Royal', 'semi-diplomatic')

        # <span id="edRoyal20D1_00543_24" data-corresp="#edfr20125_00608">
        for correpondance in xml.findall('.//*[@data-corresp]'):
            id_src = correpondance.attrib.get('id', None)
            id_dst = correpondance.attrib.get('data-corresp', None)
            if id_src and id_dst:
                id_src = re.sub(ur'^.*_(\d{5,5}).*', ur'\1', id_src)
                id_dst = re.sub(ur'^.*_(\d{5,5}).*', ur'\1', id_dst)
                if len(id_src) == 5 and len(id_dst) == 5:
                    id_src = str(int(id_src))
                    id_dst = str(int(id_dst))

                    for doc in ['Royal_Fr20125', 'Fr20125_Royal']:
                        l = ret[doc].get(id_src, None)
                        if l is None:
                            l = []
                        if id_dst not in l:
                            l.append(id_dst)
                            ret[doc][id_src] = l
                        id_src, id_dst = id_dst, id_src

        return ret

    def request_documents(self):
        # TODO: kiln pipeline for returning all texts under a path
        self.response = {'documents': self.fetch_documents()}

    def fetch_documents(self):
        # TODO: kiln pipeline for returning all texts under a path
        ret = [
            {
                'slug': 'Fr20125',
                'label': 'Fr20125',
            },
            {
                'slug': 'Royal',
                'label': 'Royal 20 D I',
            }
        ]

        return ret

    def get_notational_conventions(self, xml, view_slug):
        conventions = ''

        conventions_xml = xml.find('.//div[@id="text-conventions"]')
        if conventions_xml is not None:
            conventions = get_unicode_from_xml(conventions_xml)
            conventions = re.sub(ur'id="([^"]+)"', ur'class="\1"', conventions)

        return conventions

    def get_location_info_from_xml(self, xml, location_type):
        ret = {'slug': '', 'label': '?', 'label_long': '?'}

        if location_type['slug'] == 'section':
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
