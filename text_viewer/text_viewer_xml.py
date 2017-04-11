from django.conf import settings
from text_viewer import (TextViewerAPI, get_unicode_from_xml,
                         remove_xml_elements)
import xml.etree.ElementTree as ET
import re


class TextViewerAPIXML(TextViewerAPI):

    location_types = [
    ]

    def get_location_type(self, slug):
        ret = None
        for location_type in self.location_types:
            if location_type['slug'] == slug:
                ret = location_type
                break
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
        document_title = None
        for version in xml.findall(
                './/manuscript[@name="{}"]/versions/version'.
                format(document_slug)):
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

            document_title = view_xml.find('title')
            if document_title is None:
                document_title = document_slug
            else:
                document_title = get_unicode_from_xml(
                    document_title, text_only=True)
            # TODO: remove this from here and TEI doc
            document_title = document_title.replace(
                'TVOF transcription template', '')

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
            'label': document_title or document_slug,
            'views': views,
        }

    def get_location_info_from_xml(self, xml, location_type):
        ret = {'slug': '', 'label': '?', 'label_long': '?'}

        return ret

    def compress_html(self, html_str):
        return re.sub(ur'(\s)+', ur'\1', html_str)

    def request_chunk(self, address_parts=None, synced_with=None):
        '''
        Fetch the text chunk closest to the requested address.
        Set the response with the HTML chunk and its actual address.

        TODO: generalise this. But very difficult as the information for
        address resolution can require the document and vice versa depending on
        the document backend and the document format. Both of wich can vary
        from one project to another.
        '''

        # resolve address (e.g. 'default')
        document, view, location_type_slug, location = \
            self.get_list_from_address_parts(address_parts)

        if document in ['default', '']:
            document = self.fetch_documents()[0]['slug']
        if view in ['default', '']:
            # TODO: get it from the xml
            view = 'semi-diplomatic'

        # get the XML document
        xml = self.fetch_xml_from_kiln(document, view)
        remove_xml_elements(xml, './/div[@id="text-conventions"]')

        # resolve the rest of the address
        if location_type_slug in ['default', '']:
            location_type_slug = self.location_types[0]['slug']

        location_type = self.get_location_type(location_type_slug)

        # extract chunk from document and address
        xpath_from_location = location_type.get('xpath_from_location')
        if location == 'default' or xpath_from_location is None:
            xpath = location_type.get('xpath')
        else:
            xpath = xpath_from_location(
                document, view, location_type_slug, location, synced_with)
        chunk = xml.find(xpath)

        # build response from chunk and address
        if chunk is None:
            self.add_error(
                'notfound', 'Chunk not found: {}'.format(
                    self.get_requested_address()), 'XPATH = {}'.format(xpath))
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
        return conventions

    def fetch_xml_from_kiln(self, document, view):
        text_path = 'texts/{}/{}/'.format(document, view)
        kiln_base_url = settings.KILN_BASE_URL.strip('/')
        url = kiln_base_url + '/backend/' + text_path

        # Send the request to Kiln.
        print url
        response = TextViewerAPI.get_cached_request(url)

        # Create a new XML tree from the response.
        root = ET.fromstring(response)

        ret = root.find('.//text[@name="{}"]'.format(document))

        return ret
