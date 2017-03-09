from text_viewer import TextViewerAPI
import xml.etree.ElementTree as ET

# TODO: move this to another package, outside of generic text_viewer


class TextViewerAPITvof(TextViewerAPI):

    def request_documents(self):
        # TODO: kiln pipeline for returning all texts under a path
        documents = [
            {
                'slug': 'Fr20125',
                'label': 'Fr20125',
            },
        ]

        self.response = {'documents': documents}

    def request_view(self):
        path = self.requested_path[::-1]
        document = path.pop()
        view = path.pop()
        location_type = path.pop() if path else ''
        location = path.pop() if path else ''

        print '0'

        text_path = 'texts/{}/{}/'.format(document, view)
        xml = self.fetch_xml_from_kiln(text_path)

        chunk = None

        print '1'

        # extract chunk
        if location_type == 'section':
            print '1.2'
            # xpath = ur".//div[@id='edfr20125_{}']".format(location.zfill(5))
            xpath = ur".//div[@id='edfr20125_%s']" % location.zfill(5)
            print xpath
            chunk = xml.find(xpath)
            print '1.3'
            # location = ''

        print '2'

        if chunk is None:
            print '2.1'
            self.add_error('notfound', 'Chunk not found')
        else:
            chunk = ET.tostring(chunk)

            print '3'

            address = '/'.join([document, view, location_type, location])

            self.response = {
                'chunk': chunk,
                'address': address,
            }

        print '4'

    def fetch_xml_from_kiln(self, text_path):
        import requests
        from django.conf import settings

        kiln_base_url = settings.KILN_BASE_URL.strip('/')
        url = kiln_base_url + '/backend/' + text_path

        # Send the request to Kiln.
        print url
        r = requests.get(url)
        response = r.text.encode('utf-8')

        print 'get response'

        # Create a new XML tree from the response.
        root = ET.fromstring(response)

        # Parameters to be passed to the template.
        # params = {}

        ret = root.findall('texts/text')[0]

        return ret
