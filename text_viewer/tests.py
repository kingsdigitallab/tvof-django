from django.test import TestCase
from django.conf import settings

from .text_viewer_tvof import TextViewerAPITvof
from django.http.request import HttpRequest

# only when TEST_TEXT_VIEWER = True in your local.py
# because kiln api not available to Travis
if getattr(settings, 'TEST_TEXT_VIEWER', False):
    class TextViewerTests(TestCase):

        def test_request_documents(self):
            self._test_request()

        def _test_request_document_wrong(self):
            self._test_request('FRXYZ')

        def test_request_document(self):
            self._test_request('Fr20125')

        def test_request_section(self):
            self._test_request('Fr20125/interpretive/section/588')

        def test_request_whole(self):
            self._test_request('Fr20125/interpretive/whole/whole')

        def test_request_section_default(self):
            self._test_request('Fr20125/interpretive/section/default')

        def test_request_default_default(self):
            self._test_request('Fr20125/interpretive/default/default')

        def test_request_chunk_default_default_default(self):
            self._test_request('Fr20125/default/default/default')

        def _test_request(self, path=None, params=None):
            path = path or ''
            request = HttpRequest()

            tv = TextViewerAPITvof()
            tv.process_request(request, path)
            res = tv.get_response()

            # print res
            has_errors = bool(res.get('errors'))

            if has_errors:
                print(repr(path))
                print(repr(res.get('errors')))

            self.assertIs(has_errors, False)
