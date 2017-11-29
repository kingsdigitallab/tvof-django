from kiln_requester import CachedRequesterKiln

'''
TODO: instead of inheritence we should use a strategy pattern for:
* the document and its format: XML, HTML, JSON, TEXT,
* the repository and its API (DB, RestAPI, ...)
'''


class TextViewerAPI(object):
    '''
    Text Viewer Web API Skeleton

    To be inherited for specific text backends (e.g. kiln, database)

    API: /document/view/location_type/location
    '''

    part_levels = ['document', 'view', 'location_type', 'location']

    def __init__(self):
        self.requester = CachedRequesterKiln()

    def add_error(self, code, message, info=None):
        error = {'code': code, 'message': message}
        if info:
            error['info'] = info
        self.errors.append(error)

    def clear_errors(self):
        self.errors = []

    def process_request(self, request, path):
        self.response = {}
        self.errors = []

        self.request = request
        self.requested_address = path.strip('/')

        parts = self.get_address_parts()
        level = parts['level']

        if level == 'root':
            self.request_documents()
        elif level == 'document':
            self.request_document(parts['document'])
        elif level == 'location':
            synced_with = None
            best_match = False
            if request:
                synced_with = request.GET.get('sw', None)
                best_match = request.GET.get('bm', False)
            if synced_with:
                synced_with = self.get_address_parts(synced_with)
            self.request_chunk_best_match(
                parts, synced_with=synced_with, best_match=best_match)
        else:
            self.add_error('invalid_call', 'Invalid API call')

    def request_chunk_best_match(self, parts, synced_with=None,
                                 best_match=False):
        # If best_match = False and requested address doesn't exist we return
        # error
        # Otherwise we try our best to return something close to the requested
        # address.
        parts = parts.copy()
        ret = False
        while True:
            self.clear_errors()
            # print self.get_list_from_address_parts(parts)
            ret = self.request_chunk(parts, synced_with=synced_with)
            if ret or not best_match:
                break
            # we haven't found a perfect match, let's try higher
            changed = False
            for level in self.part_levels[::-1]:
                if parts[level] not in ['', 'default']:
                    changed = True
                    parts[level] = 'default'
                    break
            if not changed:
                break

        return ret

    def get_requested_address(self):
        return self.requested_address

    def get_address_parts(self, address=None):
        parts = (address or self.requested_address).split('/')[::-1]
        ret = {'level': 'root'}
        for level in self.part_levels:
            ret[level] = parts.pop() if parts else ''
            if ret[level]:
                ret['level'] = level

        return ret

    def get_list_from_address_parts(self, parts):
        return [parts[k] for k in self.part_levels]

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

    def request_chunk(self, address_parts, synced_with=None):
        '''
        document = self.requested_path[0]
        view = self.requested_path[1]

        location_type = 'whole'
        location = ''
        '''
        return ''

    def request_synced_chunk(self, address_parts=None, synced_with=None):
        # http://localhost:8000/textviewer/api/Fr20125/semi-diplomatic/section/592?jx=1&sw=Fr20125/semi-diplomatic/interpretive/section/588
        # =>
        # Fr20125/semi-diplomatic/ + section/588

        # TODO: resolution of the correspondance should be done in the subclass
        # here we do a default one, mixing both addresses
        parts_synced = self.get_address_parts(synced_with)

        parts = {k: v for k, v in address_parts.iteritems()}
        if address_parts['document'] == parts_synced['document']:
            # same doc, we simply copy the location type and location
            for k in ['location_type', 'location']:
                parts[k] = parts_synced[k]
        else:
            # different documents, we need to translate the address
            if parts['location_type'] == 'section':
                parts['location'] = 'default'

        return self.request_chunk(parts)

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

    def request_backend(self, url):
        import time
        t0 = time.time()
        ret = self.requester.request(url)
        t1 = time.time()
        print t1 - t0
        return ret


def get_xml_element_text(element):
    # returns all the text within element and its descendants
    # WITHOUT the TAIL.
    #
    # element is etree Element object
    #
    # '<r>t0<e1>t1<e2>t2</e2>t3</e1>t4</r>'
    # e = (xml.findall(el))[0]
    # e.text => t1
    # e.tail => t4 (! part of e1)
    # get_xml_element_text(element) => 't1t2t3'

    return ''.join(element.itertext())


def get_unicode_from_xml(xmltree, encoding='utf-8', text_only=False,
                         remove_root=False):
    import xml.etree.ElementTree as ET

    # if text_only = True => strip all XML tags
    # EXCLUDE the TAIL
    if text_only:
        return get_xml_element_text(xmltree)
    else:
        if hasattr(xmltree, 'getroot'):
            xmltree = xmltree.getroot()
        ret = ET.tostring(xmltree, encoding=encoding).decode('utf-8')
        if xmltree.tail is not None and ret[0] == '<':
            # remove the tail
            import re
            ret = re.sub(ur'[^>]+$', '', ret)

        if remove_root:
            ret = ret.replace('<root>', '').replace('</root>', '')

        return ret


def remove_xml_elements(xml, xpath):
    ret = 0
    '''Remove all the elements matching xpath (and all their content)'''
    items = xml.findall(xpath)
    parents = xml.findall(xpath + '/..')
    for i, item in enumerate(items):
        ret += 1
        parents[i].remove(item)
    return ret
