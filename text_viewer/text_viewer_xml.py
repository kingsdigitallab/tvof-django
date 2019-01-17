from django.conf import settings
from .text_viewer import (TextViewerAPI, get_unicode_from_xml,
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
        # TODO: should be applied before the content is cached
        # otherwise we redo it each time a chunk is requested

        # remove empty class attributes
        ret = re.sub(r'''class\s*=\s*("\s*"|'\s*')''', r'', html_str)
        # compress multiple spaces
        ret = re.sub(r'(\s)+', r'\1', ret)

        # remove empty spans (invalid HTML)
        empty_spans = re.findall(r'<span[^>]*/>', ret)
        if (empty_spans):
            print('WARNING: empty <span/>')
            print(empty_spans)
            ret = re.sub(r'<span[^>]*/>', '', ret)

        # remove spans without attributes (saves a lot of space!)
        ret = re.sub(r'(?musi)<span>([^<]*)</span>', r'\1', ret)

        return ret

    def request_chunk(self, address_parts=None, synced_with=None):
        '''
        Fetch the text chunk closest to the requested address.
        Set the response with the HTML chunk and its actual address.

        Return True if found a chunk.

        TODO: generalise this. But very difficult as the information for
        address resolution can require the document and vice versa depending on
        the document backend and the document format. Both of which can vary
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
        notes_info = {
            'notes': []
        }
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
                self.set_chunk_not_found_error(xpath)
            else:
                location_from_chunk = location_type.get(
                    'location_from_chunk')
                if location_from_chunk:
                    location = location_from_chunk(chunk)

                if self.is_print:
                    self.extract_notes_from_chunk(chunk, notes_info)

                chunks.append(ET.tostring(chunk))

                address = '/'.join([document, view,
                                    location_type_slug, location])

        if not xpaths:
            self.set_chunk_not_found_error()

        if chunks:
            chunk = '\n'.join(chunks)

            if notes_info['notes']:
                chunk = '{}<div class="notes-all"><h3>Notes</h3>{}</div>'.\
                    format(
                        chunk,
                        '\n'.join(notes_info['notes'])
                    )

            chunk = self.compress_html(chunk)

            classes = ['tv-view-{}'.format(view)]
            if self.is_print:
                classes.append('tv-viewer-proofreader')
            else:
                classes.append('tv-viewer-pane')

            self.response = {
                'chunk':
                    r'<div class="{}">{}</div>'.
                    format(' '.join(classes), chunk),
                'address': address,
                'generated': self.generated_date
            }
            ret = True

        return ret

    def extract_notes_from_chunk(self, chunk, notes_info):
        pass

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
        # TODO: this is very slow, we should move that to kiln_requester
        # and cache it there. The catch though is that callers modify
        # the tree... so we'd need to clone it.
        root = ET.fromstring(response)

        ret = root.find('.//text[@name="{}"]'.format(kilnid))

        # extract the date
        self.generated_date = None
        generated_date = root.find('.//generated/date')
        if generated_date is not None:
            self.generated_date = generated_date.text

        return ret
