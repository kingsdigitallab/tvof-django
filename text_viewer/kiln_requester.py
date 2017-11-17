import thread
from django.core.cache import caches
from requests.exceptions import ConnectionError


class CachedRequesterKiln(object):
    '''
    A way to send http requests and cache the response on disk and in memory.

    This was written to make more efficient request to Kiln's documents.

    Note that the memory cache is per instance and it is recommended not to
    share instances among threads.

    Caching strategy:
    * if the response is in memory, return it
    * if not, read from disk and get response length from remote server
    * if lengths are different, stream the whole response to disk
    * convert response to unicode and it in memory
    * return the response

    If the connection to Kiln fails we fall back to the disk cache.

    The disk cache is obviously shared among all threads and processes.

    Author: GN, 2017
    '''

    def __init__(self, cache_name='kiln',
                 chunk_size=4 * 1024, encoding='utf-8'):
        self.cache_mem = {}
        self.cache = caches[cache_name]
        self.chunk_size = chunk_size
        self.encoding = encoding

    def request(self, url, force=False):
        import re
        # create a unique key for this url
        urlid = re.sub('[^a-z0-9-]', '',
                       url.lower().replace('?', '-').replace('/', '-'))

        # return response from memory if it's there
        ret = self.cache_mem.get(urlid, None)
        if ret:
            return ret

        # read response from disk if it's there
        ret = self._load_response(urlid)
        ret_len = len(ret) if ret else 0

        # request headers (to response length)
        stream = None
        stream_len = 0
        import requests
        try:
            stream = requests.get(url, stream=True)
            stream_len = stream.headers.get('content-length')
        except ConnectionError:
            print 'ERROR'
            pass

        # if length response from disk is != from response headers
        # we request from remote server and save directly to disk
        if stream:
            if force or str(stream_len) != str(ret_len):
                self.dmsg(str(stream_len) + ' <> ' + str(ret_len))
                # request
                self.dmsg('DOWNLOAD response')
                parts = []
                apply_vagrant_fix = '10.0.2.2' in url and self.chunk_size > 100
                for data in stream.iter_content(chunk_size=self.chunk_size):
                    # don't ask!!
                    if apply_vagrant_fix:
                        print '.'
                    parts.append(data)
                self.dmsg('WRITE to disk cache')

                ret = ''.join(parts)
                self.cache.set(urlid, ret)

            stream.close()

        # convert from utf-8 to Unicode string
        if ret and self.encoding:
            self.dmsg('DECODE')
            # ret = ret.decode(self.encoding)
            self.cache_mem[urlid] = ret

        return ret

    def dmsg(self, message):
        print '%s %s' % (thread.get_ident(), message)

    def clear_disk_cache(self):
        self.cache.clear()

    def _load_response(self, urlid):
        return self.cache.get(urlid, None)
