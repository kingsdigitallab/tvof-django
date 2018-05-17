from django.conf import settings
from text_viewer import (TextViewerAPI, get_unicode_from_xml,
                         remove_xml_elements)
import xml.etree.ElementTree as ET
import re


class TextViewerAPIXML(TextViewerAPI):

    location_types = [
    ]

    def get_location_type(self, slug):
        ret = self.location_types[0]
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
        xml = self.fetch_xml_from_kiln(document_slug, 'interpretive')

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

            document_title = self.get_doc_title(view_xml) or document_slug

            # add notational conventions
            view['conventions'] = self.get_notational_conventions(
                view_xml, view['slug'])

            # get all the location
            for location_type in self.location_types:

                # TODO: don't hard-code this
                if self.client == 'textviewer' and\
                        location_type['slug'] == 'whole':
                    # Hide 'Whole' on the Text Viewer app, too large for
                    # browser
                    continue

                locations = []
                xpath = location_type.get('xpath', None)
                if xpath:
                    for location_xml in\
                            view_xml.findall(location_type['xpath']):
                        if not self.is_location_visible(
                                location_xml, document_slug, view['slug'],
                                location_type['slug']):
                            continue

                        location = self.get_location_info_from_xml(
                            location_xml, location_type)
                        if location['slug']:
                            locations.append(location)

                if location_type['slug'] == 'whole':
                    locations = [{
                        'slug': 'whole',
                        'label': 'Whole',
                        'label_long': 'Whole'
                    }]

                if locations:
                    location_type_info = {
                        'slug': location_type['slug'],
                        'label': location_type['label'],
                        'locations': locations,
                    }
                    view['location_types'].append(location_type_info)

            if view['location_types']:
                views.append(view)

        self.response = {
            'slug': document_slug,
            'label': document_title or document_slug,
            'views': views,
        }

    def get_doc_title(self, xml):
        ret = xml.find('title')
        if ret is not None:
            ret = get_unicode_from_xml(ret, text_only=True)

        return ret

    def get_location_info_from_xml(self, xml, location_type):
        ret = {'slug': '', 'label': '?', 'label_long': '?'}

        return ret

    def compress_html(self, html_str):
        return re.sub(ur'(\s)+', ur'\1', html_str)

    def request_chunk(self, address_parts=None, synced_with=None):
        '''
        Fetch the text chunk closest to the requested address.
        Set the response with the HTML chunk and its actual address.

        Return True if found a chunk.

        TODO: generalise this. But very difficult as the information for
        address resolution can require the document and vice versa depending on
        the document backend and the document format. Both of wich can vary
        from one project to another.
        '''

        ret = False

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
        location_type = self.get_location_type(location_type_slug)
        location_type_slug = location_type['slug']

        # extract chunk from document and address
        xpath_from_location = location_type.get('xpath_from_location')
        if location == 'default' or xpath_from_location is None:
            xpaths = location_type.get('xpath')
        else:
            xpaths = xpath_from_location(
                document, view, location_type_slug, location, synced_with)
        if not isinstance(xpaths, list):
            xpaths = [xpaths]

        chunks = []
        address = ''
        for xpath in xpaths:
            chunk_list = xml.findall(xpath)

            chunk = None
            # try until we get a visible one
            # TODO: optimise, this is really inefficient to scan all elements
            for achunk in chunk_list:
                # print achunk
                if self.is_location_visible(
                        achunk, document, view, location_type_slug):
                    chunk = achunk
                    break

            # build response from chunk and address
            if chunk is None:
                self.add_error(
                    'notfound', 'Chunk not found: {}'.format(
                        self.get_requested_address()),
                    'XPATH = {}'.format(xpath)
                )
            else:
                location_from_chunk = location_type.get(
                    'location_from_chunk')
                if location_from_chunk:
                    location = location_from_chunk(chunk)

                chunks.append(ET.tostring(chunk))

                address = '/'.join([document, view,
                                    location_type_slug, location])

        if not xpaths:
            self.add_error(
                'notfound', 'Text not found ({})'.format(
                    self.get_requested_address()),
                ''
            )

        if chunks:
            # TVOF 146: move all the reveals to the end otherwise they disrupt
            # the html rendering, e.g. <div> within <span>
            reveals = []

            def extract_reveal(match):
                reveals.append(match.group(0))
            chunk = re.sub(ur'(?musi)<div[^<>]+reveal.*?</button>\s*</div>',
                           extract_reveal, u'\n'.join(chunks))
            self.response = {
                'chunk': ur'<div>{}<div class="reveals">{}</div></div>'.
                format(chunk, u'\n'.join(reveals)),
                'address': address,
                'generated': self.generated_date
            }
            ret = True

        return ret

    def get_notational_conventions(self, xml, view_slug):
        conventions = ''
        return conventions

    def fetch_xml_from_kiln(self, kilnid, view):
        text_path = 'texts/{}/{}/'.format(kilnid, view)
        kiln_base_url = settings.KILN_BASE_URL.strip('/')
        url = kiln_base_url + '/backend/' + text_path

        # Send the request to Kiln.
        # print url
        response = self.request_backend(url)

        # Create a new XML tree from the response.
        root = ET.fromstring(response)

        ret = root.find('.//text[@name="{}"]'.format(kilnid))

        # extract the date
        self.generated_date = None
        generated_date = root.find('.//generated/date')
        if generated_date is not None:
            self.generated_date = generated_date.text

        return ret
