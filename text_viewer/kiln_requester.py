import _thread
from django.core.cache import caches
from requests.exceptions import ConnectionError
from django.conf import settings
import re
import os


class CachedRequesterKiln(object):
    '''
    A way to send http requests and cache the response on disk and in memory.

    This was written to make more efficient request to Kiln's documents.

    Note that the memory cache is per request and it is recommended not to
    share instances among threads.

    Caching strategy:
    * if the response is in memory, returns it
    * if not, read from disk and get response length from remote server
    * if lengths are different, stream the whole response to disk
    * convert response to unicode and load it in memory
    * return the response

    If the connection to Kiln fails we fall back to the disk cache.

    The disk cache is obviously shared among all threads and processes.

    Author: GN, 2017
    '''

    def __init__(self, cache_name='kiln',
                 chunk_size=4 * 1024, encoding='utf-8'):
        self.cache_mem = {}
        self.chunk_size = chunk_size
        self.encoding = encoding
        import requests
        self.session = requests.Session()
        self.last_request_origin = 'NO LAST REQUEST'

    def request(self, url, force=False):
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

    def __request_http(self, url, force=False, cached_response=None):
        # request headers (to response length)
        ret = cached_response

        cached_len = str(len(cached_response or ''))

        urlid = self._get_urlid_from_url(url)

        stream = None
        stream_len = 0
        try:
            kiln_base_url = settings.KILN_BASE_URL.rstrip('/')
            stream = self.session.get(kiln_base_url + '/' + url, stream=True)
            stream_len = stream.headers.get('content-length')
        except ConnectionError as e:
            print('ERROR (%s): %s' % (self.__class__.__name__, e))
            pass

        # if length response from disk is != from response headers
        # we request from remote server and save directly to disk
        if stream:
            if force or str(stream_len) != cached_len:
                self.last_request_origin = 'KILN'
                self.dmsg(str(stream_len) + ' <> ' + cached_len)
                # request
                self.dmsg('DOWNLOAD response')
                parts = []
                # ac-342: ! we don't use decode_unicode=True here.
                # We want to save exactly what we receive so the
                # comparison b/w content-length in header and size in cache
                # is valid.
                for data in stream.iter_content(chunk_size=self.chunk_size):
                    parts.append(data)
                self.dmsg('WRITE to disk cache')

                ret = b''.join(parts)
                self.cache.set(urlid, ret)

            stream.close()

        return ret

    def dmsg(self, message):
        if settings.DEBUG:
            print('%s' % message)
            if 0:
                print('%s %s' % (_thread.get_ident(), message))

    def __clear_disk_cache(self):
        self.cache.clear()

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
