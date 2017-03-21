import requests
from django.conf import settings
from text_viewer import TextViewerAPI, get_unicode_from_xml
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
            'xpath': './/div[@class="tei body"]/div[h4]',
            'xpath_from_location':
                lambda l: ur".//div[@id='edfr20125_{}']".format(l.zfill(5)),
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

    def get_location_type(self, slug):
        ret = None
        for location_type in self.location_types:
            if location_type['slug'] == slug:
                ret = location_type
                break
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
        ]

        return ret

    def request_document(self, document_slug):
        '''Returns all the views for a given document
            For each view, return the location_types.
            For each location_type, return the locations.
           These together should allow a client to get to
           any location in any view of the document.
        '''
        # TODO: improve kiln pipeline for this call
        # call this to get all the versions (e.g. semi-diplomatic, ...)
        xml = self.fetch_xml_from_kiln(document_slug, 'critical')

        views = []
        for version in xml.findall('.//versions/version'):
            slug = version.attrib.get('name', 'undefined')
            view = {
                'slug': slug,
                'label': slug,
            }

            # add display settings
            if view['slug'] in ['interpretive']:
                view['display_settings'] = [
                    {
                        'slug': 'hide-notes',
                        'label': 'Hide notes',
                        'classes': 'hide-notes',
                    },
                    {
                        'slug': 'hide-sics',
                        'label': 'Hide corrections',
                        'classes': 'hide-sics',
                    }
                ]

            # add location types and locations
            view['location_types'] = []

            # fetch a particular version/view (e.g. semi-diplomatic, ...)
            view_xml = self.fetch_xml_from_kiln(document_slug, slug)

            # add notational conventions
            view['conventions'] = self.get_notational_conventions(
                view_xml, view['slug'])

            # get all the location
            for location_type in self.location_types:
                locations = []
                xpath = location_type.get('xpath', None)
                if xpath:
                    for location_xml in\
                            view_xml.findall(location_type['xpath']):
                        location = self.get_location_info_from_xml(
                            location_xml, location_type)
                        if location['slug']:
                            locations.append(location)

                if location_type['slug'] == 'synced':
                    locations = [{
                        'slug': 'synced',
                        'label': 'synced',
                        'label_long': 'synced'}]
                if location_type['slug'] == 'whole':
                    locations = [{
                        'slug': 'whole',
                        'label': 'Whole',
                        'label_long': 'Whole'}]
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
                ret = {
                    'slug': number,
                    'label': number,
                    'label_long': label_long,
                }

        return ret

    def compress_html(self, html_str):
        return re.sub(ur'(\s)+', ur'\1', html_str)

    def request_chunk(self, address_parts=None):
        document, view, location_type_slug, location = \
            self.get_list_from_address_parts(address_parts)

        if document in ['default', '']:
            document = self.fetch_documents()[0]['slug']
        if view in ['default', '']:
            # TODO: get it from the xml
            view = 'semi-diplomatic'

        xml = self.fetch_xml_from_kiln(document, view)

        chunk = None

        if location_type_slug in ['default', '']:
            location_type_slug = self.location_types[0]['slug']

        location_type = self.get_location_type(location_type_slug)

        # extract chunk
        xpath_from_location = location_type.get('xpath_from_location')
        if location == 'default' or xpath_from_location is None:
            xpath = location_type.get('xpath')
        else:
            xpath = location_type.get('xpath_from_location')(location)
        print xpath
        chunk = xml.find(xpath)

        if chunk is None:
            self.add_error(
                'notfound', 'Chunk not found: {}'.format(
                    self.get_requested_address()))
        else:
            location_from_chunk = location_type.get('location_from_chunk')
            if location_from_chunk:
                location = location_from_chunk(chunk)

            chunk = ET.tostring(chunk)

            address = '/'.join([document, view, location_type_slug, location])

            self.response = {
                'chunk': chunk,
                'address': address,
            }

    def get_notational_conventions(self, xml, view_slug):
        conventions = ''
        if view_slug in ['interpretive']:
            conventions = '''
            <div class="text-conventions">
                <ul>
                  <li>
                    <span class="notation">
                      <a data-toggle="xxx">
                         <sup class="note tei-source"></sup>
                      </a>
                    </span>
                    <span class="description">
                       References to sources.
                    </span>
                  </li>
                  <li>
                    <span class="notation">
                      <a data-toggle="d99280e3208">
                        <sup class="tei-corr-popup"></sup>
                      </a>
                    </span>
                    <span class="description">
                        Sic erat scriptum
                    </span>
                  </li>
                </ul>
            </div>
            '''

        conventions_xml = xml.find('.//div[@id="text-conventions"]')
        if conventions_xml is not None:
            conventions = get_unicode_from_xml(conventions_xml)
            conventions = re.sub(ur'id="([^"]+)"', ur'class="\1"', conventions)

        return conventions

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
