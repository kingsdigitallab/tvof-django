from django.test import TestCase
from django.conf import settings

from .text_viewer_tvof import TextViewerAPITvof
from django.http.request import HttpRequest
from . import utils


class XMLTests(TestCase):

    def test_remove_xml_elements(self):
        cases = [
            [
                '''<r>head<a>text</a>tail</r>''',
                '''<r>headtail</r>''',
            ],
            [
                '''<r><a>text</a>tail</r>''',
                '''<r>tail</r>''',
            ],
            [
                '''<r>head<a>text</a></r>''',
                '''<r>head</r>''',
            ],
            [
                '''<r>head<a>text1</a>tail1<a>text2</a>tail2</r>''',
                '''<r>headtail1tail2</r>''',
            ],
            [
                '''<r><a>text2</a>tail1<a>text2</a>tail2</r>''',
                '''<r>tail1tail2</r>''',
            ],
            [
                '''<r><a>text</a></r>''',
                '''<r />''',
            ],
            [
                '''<r><r1>head<a>text1</a>tail2</r1><r2>head2<a>text2</a><b>text3</b><a>text4</a>tail4</r2></r>''',
                '''<r><r1>headtail2</r1><r2>head2<b>text3</b>tail4</r2></r>''',
            ],
        ]

        errors = []
        for case in cases:
            xmli = utils.get_xml_from_unicode(case[0])
            utils.remove_xml_elements(xmli, './/a')
            stro = utils.get_unicode_from_xml(xmli)
            self.assertEqual(stro, case[1], case[0])

        if errors:
            self.assertTrue(False, repr(errors))


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

if 0:
    xml_str = '''<r>
    <gp>
      <p>
        <e>e1.1</e>
        <e class="c1">e1.2</e>
      </p>
      <p>
        <e>e2.1</e>
        <e>e2.2</e>
      </p>
    </gp>
    </r>
    '''

    root = ET.fromstring(xml_str)
    for e in findall_from_xml(root, './/e[@class="c1"]'):
        print(e['el'].text)
