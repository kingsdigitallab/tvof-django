

class TextViewerAPI(object):
    '''
    Text Viewer Web API Skeleton

    To be inherited for specific text backends (e.g. kiln, database)

    API: /document/view/location_type/location
    '''

    def __init__(self):
        pass

    def add_error(self, code, message):
        error = {'code': code, 'message': message}
        self.errors.append(error)

    def process_request(self, request, path):
        self.response = {}
        self.errors = []

        self.request = request
        self.requested_path = path.strip('/').split('/')

        if not self.requested_path[0]:
            self.request_documents()
        elif len(self.requested_path) == 1:
            self.request_document()
        elif len(self.requested_path) == 4:
            self.request_chunk()
        else:
            self.add_error('invalid_call', 'Invalid API call')

    def request_documents(self):
        ''' Add the list of all documents to self.response['documents']

        self.response['documents'] [
            {
                'slug': 'Fr_20125',
                'label': 'Fr20125',
            },
            ...
        ]
        '''
        documents = []

        self.response = {'documents': documents}

    def request_chunk(self):
        '''
        document = self.requested_path[0]
        view = self.requested_path[1]

        location_type = 'whole'
        location = ''
        '''

    def get_response_json(self):
        from django.http import JsonResponse
        return JsonResponse(self.get_response())

    def get_response(self):
        ret = self.response
        if self.errors:
            ret = {
                'errors': self.errors
            }
        return ret
