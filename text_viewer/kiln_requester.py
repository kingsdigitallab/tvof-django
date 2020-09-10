from requests.exceptions import ConnectionError
from django.conf import settings
import re
import os


class CachedRequesterKiln(object):
    '''
    A fast method to request documents from Kiln
    and cache the response on disk and in memory.

    Note that the memory cache is per request and it is recommended not to
    share instances of this class among threads.

    Note that we assume that the Kiln documents are made static

    Caching strategy:
    * if the response is in memory, returns it
    * if not, read from disk
    * convert response to unicode and load it in memory
    * return the response

    The disk cache is obviously shared among all threads and processes.
    '''

    def __init__(self, cache_name='kiln',
                 chunk_size=4 * 1024, encoding='utf-8'):
        # our memory cache (for this thread / request only)
        self.cache_mem = {}
        # self.chunk_size = chunk_size
        self.encoding = encoding
        # import requests
        # self.session = requests.Session()
        self.last_request_origin = 'NO LAST REQUEST'

    def request_data_content(self, url, force=False):
        '''Returns the html content only of the kiln doc at the given url.
        Without <?xml> or enclosing <data> element.
        '''
        ret = self.request(url, force)
        if ret:
            ret = re.sub(r'(?musi).*<data[^>]*>(.*)</data>', r'\1', ret)
        return ret

    def request(self, url, force=False):
        '''Returns a full kiln document from the given kiln url.

        Note that we no longer send http requests to kiln.
        Kiln output docs must be baked/generated in advanced.
        We just read them from disk / memory.

        force: no longer used.
        '''
        url = url.lstrip('/')

        import time
        t0 = time.time()
        ret = self._request(url, force=force)

        if ret is not None:
            d = time.time() - t0
            size_mb = len(ret) / 1024.0 / 1024
            self.dmsg('Request: %s from %s (%0.4f MB, %0.2f s.)' %
                      (url, self.last_request_origin, size_mb, d))

        return ret

    def _get_urlid_from_url(self, url):
        url = url.strip('/')
        return re.sub('[^a-z0-9-]', '',
                      url.lower().replace('?', '-').replace('/', '-'))

    def _request(self, url, force=False):
        self.last_request_origin = 'MEMORY'

        # create a unique key for this url
        urlid = self._get_urlid_from_url(url)

        # return response from memory if it's there
        ret = self.cache_mem.get(urlid, None)
        if ret:
            return ret

        self.last_request_origin = 'DISK CACHE'

        # read response from disk if it's there
        ret = self._load_response_from_disk_cache(url)

        if ret:
            ret = ret.decode(self.encoding)
            self.cache_mem[urlid] = ret

        return ret

    def dmsg(self, message):
        if settings.DEBUG:
            print('%s' % message)
            if 0:
                import _thread
                print('%s %s' % (_thread.get_ident(), message))

    def _load_response_from_disk_cache(self, url):
        ret = None
        urlid = self._get_urlid_from_url(url)
        path = os.path.join(settings.KILN_STATIC_PATH, urlid)
        if os.path.exists(path):
            with open(path, 'rb') as f:
                ret = f.read()
        else:
            self.dmsg('Request "%s" not found on disk "%s"' % (url, path))

        return ret

    def get_timestamp_from_url(self, url):
        '''returns the timestamp of the content for the given kiln url'''
        import os

        ret = 0

        urlid = self._get_urlid_from_url(url)
        path = os.path.join(settings.KILN_STATIC_PATH, urlid)
        if os.path.exists(path):
            ret = os.path.getmtime(path)

        return ret
