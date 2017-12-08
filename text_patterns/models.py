# -*- coding: utf-8 -*-
from text_viewer.text_viewer_tvof import TextViewerAPITvof
from text_viewer.text_viewer import (get_unicode_from_xml)
from django.contrib.auth.models import User
from django.db import models
import utils
import xml.etree.ElementTree as ET
import utils as dputils


class TextPatternSet(models.Model):
    slug = models.SlugField(max_length=30, blank=False,
                            null=False, unique=True)
    patterns = models.TextField(blank=True, null=False, default=ur'')
    text_url = models.URLField(blank=True, null=False, default=ur'')

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    owner = models.ForeignKey(User, models.SET_NULL, blank=False, null=True)
    owner_sessionid = models.CharField(max_length=64, blank=False, null=True)

    def __unicode__(self):
        return ur'{}'.format(self.slug)

    def get_size(self):
        return len(self.get_dicts_from_patterns())

    def get_dicts_from_patterns(self):
        ret = dputils.json_loads(self.patterns or [])
        return ret

    def set_patterns_from_dicts(self, dicts):
        self.patterns = dputils.json_dumps(dicts)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('pattern_set', kwargs={'slug': self.slug})

# TODO: move this TVOF custom code to subclass


class TextUnitsCached(object):
    '''
    Drop-in replacement for TextUnits that uses a cache to avoid
    fecthing the doc, splitting into units, xml and plain text conversions.

    Caches:
        * the full list of plain content units for each (dov, view)
            into a single cache entry
        * the list of unitids for a given API address
    '''

    def get_units(self, address):
        from django.core.cache import caches

        cache = caches['text_patterns']

        # get the list of unitids for the given address
        address_key = address + '_unitids'
        unitids = cache.get(address_key)

        import json

        if not unitids:
            print 'Generate unitids for %s' % address
            unitids = [
                unit.unitid
                for unit in TextUnits().get_units(address)
            ]
            cache.set(address_key, json.dumps(unitids))
        else:
            print 'Get unitids for %s from cache' % address
            unitids = json.loads(unitids)

        # get the plain content of the desired units
        parts = address.strip('/').split('/')
        # e.g. Fr20125/interpretive
        doc_view = '/'.join(parts[:2])
        contents_key = doc_view + '_units'
        contents = cache.get(contents_key)

        if not contents:
            print 'Generate contents for %s' % address

            contents = {
                u.unitid: u.get_plain_dict()
                for u
                in TextUnits().get_units(doc_view + '/whole/default')
            }

            cache.set(contents_key, json.dumps(contents))
        else:
            print 'Get contents for %s from cache' % address
            contents = json.loads(contents)

        # now spits the desired units
        for unitid in unitids:
            yield TextUnit(**contents[unitid])


class TextUnits(object):
    '''
    Retieves units of text from the Text Viewer API.
    Returns instances of TextUnit.
    '''

    def get_units(self, address):
        '''
        address is a Text Viewer API web address,
        e.g. /Fr20125/interpretive/section/1
        '''
        # TODO: the text viewer and the pattern tool should use the same code
        # to chunk the text
        # http://192.168.33.1:9999/backend/texts/Fr20125/interpretive/
        # http://localhost:8000/lab/patterns/api/default/segunits/?ret=patterns,stats,segunits,segunits.patterns,segunits.unit&ulimit=1000&hilite=FeTKdBAQyA&ignore=other_patterns
        api = TextViewerAPITvof()

        # TODO: here we call the API using django, we should eventually have an
        # option to call a remote web api.

        if not address:
            address = 'Fr20125/interpretive/whole/default'

        # complete given address with default values
        parts = address.split('/')
        address = (['default'] * 4)
        address[0:len(parts)] = parts
        document, view = address[0:2]
        address = '/'.join(address)

        api.process_request(None, address)
        res = api.get_response()

        root = ET.fromstring(res['chunk'])

        # Get all the paragraphs
        for section in root.findall('.//div[@id]'):
            # In each para, get the rubric
            rubric = section.find('*[@class="tei-rubric"]')
            if rubric is not None:
                # Fr20125/interpretive/seg/edfr20125_00002_rubric
                unitid = '/'.join([document, view, 'seg',
                                   section.attrib.get('id') + '_rubric'])
                unit = TextUnit(unitid, rubric)
                yield unit

            # Get all the subsequent sentence (segs)
            for seg in section.findall('.//span[@id]'):
                # Fr20125/interpretive/seg/edfr20125_00002_02
                unitid = '/'.join([document, view, 'seg',
                                   seg.attrib.get('id')])
                unit = TextUnit(unitid, seg)
                yield unit


class TextUnit(object):
    '''
    Holds the content of a part (/unit) of a text.
    Either in XML or Text format.
    Text format if not supplied is derived from xml.
    If text format supplied, xml is not necessary.
    '''

    def __init__(self, unitid=None, xml=None, plain_content=None):
        # Fr20125/interpretive/seg/edfr20125_00002_02
        self.unitid = unitid
        self.xml = xml
        self.plain_content = plain_content

    def get_label_short(self):
        # Fr20125/interpretive/seg/edfr20125_00002_02
        # => Section 2: 2
        parts = self.unitid.split('_')
        ret = '_'.join(parts[-2:])
        return ret

    label_short = property(get_label_short)

    def get_plain_content(self):
        if self._plain_content is None:
            # TODO: move to TVOF subclass or, better, to the text viewer API
            if self.xml is None:
                raise Exception(
                    'TextUnit.get_plain_content() impossible since self.xml '
                    'and self.plain_content are not set.')

            import re
            for xpath in ['div[@data-reveal]', 'span[@class="tei-cb"]']:
                for reveal in self.xml.findall(xpath):
                    tail = reveal.tail
                    reveal.clear()
                    reveal.tail = tail

            ret = get_unicode_from_xml(self.xml, text_only=True)

            # ret = re.sub(ur'(?musi)\[\d*?[vrab]*?\]', '', ret)
            # [...] => nothing
            ret = re.sub(ur'(?musi)\[[^\]]*?\]', u'', ret)

            ret = utils.remove_accents(ret)
            ret = ret.lower()

            ret = ret.replace(u'v', u'u')
            # punctuation => ' '
            ret = re.sub(u'[·؛\u00A7,.;]', u' ', ret)

            ret = re.sub(ur'(?musi)\s+', u' ', ret)

            ret = ret.strip()
            self._plain_content = ret

        return self._plain_content

    def set_plain_content(self, plain_content):
        self._plain_content = plain_content

    plain_content = property(get_plain_content, set_plain_content)

    def get_plain_dict(self):
        return {
            'unitid': self.unitid,
            'plain_content': self.plain_content,
        }
