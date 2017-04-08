from text_viewer_xml import (TextViewerAPIXML)

# TODO: move this to another package, outside of generic text_viewer
'''
    http://localhost:8000/textviewer/api/?jx=1
    http://localhost:8000/textviewer/api/Fr20125/?jx=1
    http://localhost:8000/textviewer/api/Fr20125/interpretive/section/588/?jx=1
'''


def _get_xpath_from_location(document, view, location_type_slug, location):
    ret = 'INVALID'

    docid_from_document_slug = {
        'Fr20125': 'fr20125',
        'Royal': 'Royal20D1',
    }

    docid = docid_from_document_slug.get(document, None)
    if docid:
        ret = './/div[@id="ed{}_{}"]'.format(
            docid, unicode(location).rjust(5, '0'))

    return ret


class TextViewerAPITvof(TextViewerAPIXML):

    location_types = [
        {
            'slug': 'section',
            'label': 'Section',
            'xpath': './/div[@class="tei body"]/div[h4]',
            'xpath_from_location': _get_xpath_from_location,
            'location_from_chunk': lambda c: unicode(int(c.attrib['id'][-5:]))
        },
        {
            'slug': 'whole',
            'label': 'Whole Text',
            'xpath': './/div[@class="tei body"]',
        },
        {
            'slug': 'synced',
            'label': 'Synced',
        },
    ]

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
