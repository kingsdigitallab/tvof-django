import requests
from django.conf import settings
from text_viewer import TextViewerAPI
import xml.etree.ElementTree as ET
import re

# TODO: move this to another package, outside of generic text_viewer
'''
    http://localhost:8000/textviewer/api/?jx=1
    http://localhost:8000/textviewer/api/Fr20125/?jx=1
    http://localhost:8000/textviewer/api/Fr20125/interpretive/section/588/?jx=1
'''


class TextViewerAPITvof(TextViewerAPI):

    location_types = [
        {
            'slug': 'section',
            'label': 'Section',
            'xpath': './/div[@class="tei body"]/div[@id]',
        }
    ]

    def request_documents(self):
        # TODO: kiln pipeline for returning all texts under a path
        documents = [
            {
                'slug': 'Fr20125',
                'label': 'Fr20125',
            },
        ]

        self.response = {'documents': documents}

    def request_document(self):
        '''Returns all the views for a given document
            For each view, return the location_types.
            For each location_type, return the locations.
           These together should allow a client to get to
           any location in any view of the document.
        '''
        # TODO: improve kiln pipeline for this call
        document_slug = self.requested_path[0]
        xml = self.fetch_xml_from_kiln(document_slug, 'critical')

        views = []
        for version in xml.findall('.//versions/version'):
            slug = version.attrib.get('name', 'undefined')
            view = {
                'slug': slug,
                'label': slug,
            }

            # add location types and locations
            view['location_types'] = []
            view_xml = self.fetch_xml_from_kiln(self.requested_path[0], slug)
            for location_type in self.location_types:
                locations = []
                for location_xml in view_xml.findall(location_type['xpath']):
                    location = self.get_location_info_from_xml(
                        location_xml, location_type)
                    locations.append(location)
                location_type_info = {
                    'slug': location_type['slug'],
                    'label': location_type['label'],
                    'locations': locations,
                }
                view['location_types'].append(location_type_info)

            views.append(view)

        self.response = {
            'slug': document_slug,
            'label': document_slug,
            'views': views,
        }

    def get_location_info_from_xml(self, xml, location_type):
        if location_type['slug'] == 'section':
            # id="edfr20125_00588"
            number = xml.attrib.get('id', '')
            number = re.sub(ur'^.*_0*(\d+)$', ur'\1', number)
            rubric = xml.find('.//h4')

            label_long = rubric.text
            label_long = rubric.text
            for e in rubric:
                if e.tag not in ['a', 'div']:
                    label_long += ET.tostring(e)
            label_long = self.compress_html(label_long)
            ret = {
                'slug': number,
                'label': number,
                'label_long': label_long,
            }
        else:
            ret = {'slug': '?', 'label': '?', 'label_long': '?'}

        return ret

    def compress_html(self, html_str):
        return re.sub(ur'(\s)+', ur'\1', html_str)

    def request_chunk(self):
        path = self.requested_path[::-1]
        document = path.pop()
        view = path.pop()
        location_type = path.pop() if path else ''
        location = path.pop() if path else ''

        xml = self.fetch_xml_from_kiln(document, view)

        chunk = None

        # extract chunk
        if location_type == 'section':
            if location == 'all':
                chunk = xml.find('content')
            else:
                xpath = ur".//div[@id='edfr20125_%s']" % location.zfill(5)
                chunk = xml.find(xpath)

        if chunk is None:
            self.add_error('notfound', 'Chunk not found')
        else:
            chunk = ET.tostring(chunk)

            address = '/'.join([document, view, location_type, location])

            self.response = {
                'chunk': chunk,
                'address': address,
            }

    def fetch_xml_from_kiln(self, document, view):
        text_path = 'texts/{}/{}/'.format(document, view)
        kiln_base_url = settings.KILN_BASE_URL.strip('/')
        url = kiln_base_url + '/backend/' + text_path

        # Send the request to Kiln.
        print url
        r = requests.get(url, timeout=5)
        response = r.text.encode('utf-8')

        # Create a new XML tree from the response.
        root = ET.fromstring(response)

        ret = root.find('.//text[@name="{}"]'.format(document))

        return ret
