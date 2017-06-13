from text_viewer.text_viewer_tvof import TextViewerAPITvof
from text_viewer.text_viewer import (get_unicode_from_xml)
from django.db import models
import utils
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


# TODO: move this TVOF custom code to subclass
class TextUnits(object):

    def get_units(self):
        # TODO: the text viewer and the pattern tool should use the same code
        # to chunk the text
        # http://192.168.33.1:9999/backend/texts/Fr20125/interpretive/
        # http://localhost:8000/lab/patterns/api/default/segunits/?ret=patterns,stats,segunits,segunits.patterns,segunits.unit&ulimit=1000&hilite=FeTKdBAQyA&ignore=other_patterns
        api = TextViewerAPITvof()

        # TODO: parametrise
        doc_slug = 'Fr20125'
        view = 'interpretive'

        api.process_request(None, '/'.join([doc_slug, view, 'whole', '0']))
        res = api.get_response()

        root = ET.fromstring(res['chunk'])
        for section in root.findall('.//div[@id]'):
            rubric = section.find('*[@class="tei-rubric"]')
            if rubric is not None:
                unit = TextUnit(section.attrib.get('id') + '_rubric', rubric)
                yield unit
            for seg in section.findall('.//span[@id]'):
                unit = TextUnit(seg.attrib.get('id'), seg)
                yield unit


class TextUnit(object):

    def __init__(self, unitid=None, xml=None):
        self.unitid = unitid
        self.xml = xml

    def get_plain_content(self):
        # TODO: move to TVOF subclass or, better, to the text viewer API
        for xpath in ['div[@data-reveal]', 'span[@class="tei-cb"]']:
            for reveal in self.xml.findall(xpath):
                tail = reveal.tail
                reveal.clear()
                reveal.tail = tail
        ret = get_unicode_from_xml(self.xml, text_only=True)
        ret = ret.replace('v', 'u')

        ret = utils.remove_accents(ret)
        ret = ret.lower()

        return ret
