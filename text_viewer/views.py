from django.shortcuts import render


def view_text_viewer(request, path):
    # e.g. /textviewer/
    context = {
        'viewer_webpath': request.path_info[:-len(path)]
    }
    return render(request, 'text_viewer/page.html', context)


# TODO: convert to django rest framework?
def view_text_viewer_api(request, path):
    viewer = TextViewerAPITvof()
    viewer.process_request(request, path)
    return viewer.get_response()


class TextViewerAPI(object):
    '''
    Text Viewer Web API Skeleton

    To be inherited for specific text backends (e.g. kiln, database)

    API: /document/view/location_type/location
    '''

    def __init__(self):
        self.data = {}

    def process_request(self, request, path):
        self.request = request
        self.requested_path = path.strip('/').split('/')

        if not self.requested_path[0]:
            self.request_documents()

        if len(self.requested_path) > 1:
            self.request_view()

    def request_view(self):
        '''
        document = self.requested_path[0]
        view = self.requested_path[1]

        location_type = 'whole'
        location = ''
        '''

    def request_documents(self):
        '''
        Add the list of all documents to self.data['documents']

        self.data['documents'] [
            {
                'slug': 'Fr_20125',
                'label': 'Fr20125',
            },
            ...
        ]
        '''
        documents = []

        self.data = {'documents': documents}

    def get_response(self):
        ret = {
            'data': self.data,
            'status': 'ok',
            'message': '',
        }

        from django.http import JsonResponse
        return JsonResponse(ret)


# TODO: move this to another package, outside of generic text_viewer
class TextViewerAPITvof(TextViewerAPI):

    def request_documents(self):
        # TODO: kiln pipeline for returning all texts under a path
        documents = [
            {
                'slug': 'Fr_20125',
                'label': 'Fr20125',
            },
        ]

        self.data = {'documents': documents}

    def request_view(self):
        path = self.requested_path[::-1]
        document = path.pop()
        view = path.pop()
        location_type = path.pop() if path else ''
        location = path.pop() if path else ''

        text_info = self.load_text_from_kiln(
            'texts/{}/{}/'.format(document, view))

        address = '/'.join([document, view, location_type, location])

        self.data = {
            'content': text_info['content'],
            'address': address,
        }
        self.data['address'] = address

    def load_text_from_kiln(self, text_path):
        ret = {
            'content': None,
        }

        import xml.etree.ElementTree as ET
        import requests
        from django.conf import settings

        kiln_base_url = settings.KILN_BASE_URL.strip('/')
        url = kiln_base_url + '/backend/' + text_path

        # Send the request to Kiln.
        print url
        r = requests.get(url)
        response = r.text.encode('utf-8')

        # Create a new XML tree from the response.
        root = ET.fromstring(response)

        # Parameters to be passed to the template.
        # params = {}

        text_el = root.findall('texts/text')[0]
        html = ET.tostring(text_el.find('content'))

        ret['content'] = html

        return ret
