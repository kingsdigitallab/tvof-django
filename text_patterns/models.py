from text_viewer.text_viewer_tvof import TextViewerAPITvof
from text_viewer.text_viewer import (get_unicode_from_xml)
from django.db import models
import xml.etree.ElementTree as ET


class TextPatternSet(models.Model):
    slug = models.SlugField(max_length=30, blank=False,
                            null=False, unique=True)
    patterns = models.TextField(blank=True, null=False, default=ur'')
    text_url = models.URLField(blank=True, null=False, default=ur'')

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    def __unicode__(self):
        return ur'{}'.format(self.slug)


class TextUnits(object):

    def get_units(self):
        api = TextViewerAPITvof()

        doc_slug = 'Fr20125'
        view = 'interpretive'

        api.process_request(None, '/'.join([doc_slug, view, 'whole', '0']))
        res = api.get_response()

        root = ET.fromstring(res['chunk'])
        for span in root.findall('.//span[@id]'):
            unit = TextUnit(span.attrib.get('id'))
            unit.content = get_unicode_from_xml(span, text_only=True)
            yield unit


class TextUnit(object):

    def __init__(self, unitid=None):
        self.unitid = unitid

    def get_plain_content(self):
        return self.content
        return 'This is a test %s' % self.unitid
        return self.content
