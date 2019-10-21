# -*- coding: utf-8 -*-

from django.db import models
from xml.etree import ElementTree as ET
from text_viewer.text_viewer_tvof import TextViewerAPITvof
from django.conf import settings
import re

from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel


class SearchFacet(models.Model):
    key = models.CharField(max_length=32, unique=True, choices=[
        (f['key'], f['key'])
        for f
        in settings.SEARCH_FACETS
    ])
    label = models.CharField(max_length=32, help_text='')
    tooltip = models.CharField(max_length=255, blank=True)
    description = RichTextField(blank=True)
    whitelist = models.TextField(blank=True, default='')
    display_rank = models.IntegerField(default=0)

    panels = [
        FieldPanel('key'),
        FieldPanel('label'),
        FieldPanel('tooltip'),
        FieldPanel('description'),
        FieldPanel('whitelist'),
        FieldPanel('display_rank'),
    ]

    class Meta:
        ordering = ['display_rank']

    def __str__(self):
        return self.label

    def get_white_list(self):
        return [l.lower().strip() for l in self.whitelist.split('\n') if l.strip()]


def read_tokenised_data():
    '''
    <seg type="6" xml:id="edfr20125_00910_07"><lg type="octo_coup">
        <lg type="lineated">
            <l n="001"><w n="1">Q[ua]r</w> <w n="2">ele</w> <w n="3">fu</w> <w n="4">si</w> <w n="5">bien</w> <w n="6">plantee<pc rend="1" /></w></l>
    '''

    lg_types = {'lineated': 2, 'cont': 3, 'unspecified': 4}
    sc_types = {'true': 2, 'false': 3, 'unspecified': 4}

    ret = {}

    for key, path in settings.TOKENISED_FILES.items():
        with open(path, 'rt') as f:
            content = f.read()
            content = re.sub(r'\sxmlns="[^"]+"', '', content, count=1)

        root = ET.fromstring(content)
        xmlns = 'http://www.w3.org/XML/1998/namespace'

        # lt = language_type/verse_cat
        for seg in root.findall('.//seg[@type="6"]'):
            seg_id = seg.attrib.get('{%s}id' % xmlns)
            ret[seg_id] = {'verse_cat': 4}
            for lg in seg.findall('.//lg'):
                ret[seg_id]['verse_cat'] = lg_types.get(
                    lg.attrib.get('type'), 4)

        # sc = speech_cat
        for seg in root.findall('.//seg'):
            seg_id = seg.attrib.get('{%s}id' % xmlns)
            for said in seg.findall('.//said'):
                said_type = said.attrib.get(
                    'direct', 'unspecified'
                ).strip().lower()
                for word in said.findall('.//w'):
                    seg_id_n = seg_id + '.' + word.attrib.get('n')
                    ret[seg_id_n] = {
                        'speech_cat': sc_types.get(said_type, 4)
                    }

    return ret


class KwicQuerySet(models.QuerySet):
    '''
    A virtual QuerySet
    that always returns all the entries
    read from a kwic XML file (exported from Lemming).

    The purpose is avoid storing all the kwic data in the database.

    To directly move the entries from the kwic file into the search engine:

    ./manage.py rebuild_index --noinput

    Saves time and disk space.

    Support for slicing results.
    NO support for any filter, exlcude, order_by, etc.
    '''

    max_count = settings.SEARCH_INDEX_LIMIT

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._count = None
        self.next_mark = 0
        self.generator = self.get_generator()

    def _clone(self, *args, **kwargs):
        ret = super()._clone(*args, **kwargs)
        ret._count = self._count
        ret.generator = self.generator
        return ret

    def get_generator(self):
        tvof_viewer = TextViewerAPITvof()
        mss_sections = tvof_viewer.read_all_sections_data()

        tokenised_data = read_tokenised_data()

        next_mark = 0
        for event, elem in ET.iterparse(
            settings.KWIC_FILE_PATH, events=['start']
        ):
            if elem.tag == 'item':
                item = elem
            if elem.tag == 'string':
                token = AnnotatedToken.new_from_kwik_item(
                    item,
                    elem,
                    mss_sections,
                    tokenised_data
                )
                next_mark += 1

                yield next_mark, token

    def __iter__(self):
        return self._read_from_kwic()

    def _read_from_kwic(self):
        # print('-' * 40)
        # print('here', self.query.low_mark, self.query.high_mark)

        if self.query.low_mark < self.next_mark:
            # print('NEW', self.query.low_mark, self.next_mark)
            self.generator = self.get_generator()
            self.next_mark = 0

        while self.query.high_mark > self.next_mark:
            g = next(self.generator)
            # print(g)
            self.next_mark, token = g
            # print(token, self.next_mark, self.query.low_mark)
            if self.query.low_mark < self.next_mark:
                # print(token.location)
                yield token

        # print('end', '#' * 40)

    def count(self):
        if self._count is not None:
            return self._count

        self._count = 0
        if self.max_count != 0:
            for _, elem in ET.iterparse(
                settings.KWIC_FILE_PATH, events=['start']
            ):
                if elem.tag == 'string':
                    self._count += 1
                    if (self.max_count > -1) and (self._count >= self.max_count):
                        break

        return self._count


class AutocompleteFormQuerySet(KwicQuerySet):

    def get_generator(self):
        found = {}
        next_mark = 0

        def normalise(string):
            return (string or '').strip().lower()

        def get_new_doc(form, lemma):
            '''
            Returns a AutocompleteForm for the given (form, lemma) pair.
            Returns None if that pair was seen before (see found).
            '''
            ret = None

            if lemma:
                key = '{}_{}'.format(lemma, form)
                if key not in found:
                    found[key] = 1
                    ret = AutocompleteForm(lemma=lemma, form=form)

            return ret

        # parse the kwic file for pairs of (token, lemma)
        # Note: kwic contains tokens,
        # but we normalise them into forms (lowercase).
        file_path = settings.KWIC_FILE_PATH
        for _, elem in ET.iterparse(file_path, events=['start']):
            doc = None
            if elem.tag == 'item':
                lemma = normalise(elem.attrib.get('lemma', ''))
                # we issue one doc for the lemma itself
                doc = get_new_doc('', lemma)
            if elem.tag == 'string':
                form = normalise(elem.text)
                doc = get_new_doc(form, lemma)

            if doc:
                next_mark += 1
                yield next_mark, doc

    def count(self):
        return sum(1 for _ in self.get_generator())


class AutocompleteForm(models.Model):
    from_kwic = AutocompleteFormQuerySet.as_manager()

    form = models.CharField(max_length=30, default='', blank=True)
    lemma = models.CharField(max_length=30, default='')

    def get_unique_id(self):
        ret = '{}_{}'.format(self.lemma, self.form)
        return ret


class AnnotatedToken(models.Model):
    '''
    Model for an entry in a Kwic received from Lemmings.
    The only reason for this model is to feed django-haystack indexing.
    Does NOT store anything, see KwicQuerySet.

    <kwiclist>
      <sublist key="·c·">
        <item type="seg_item" location="edfr20125_00598_08" n="23"
            preceding="chargees , ele lor envoia ·xx· bues et"
            following="pors et ·c· moutons cras et autant"
            lemma="cent">
          <string>·c·</string>
        </item>

    13MB for 45427 records, 5% of the total.
    => 260MB for 1M tokens.
    '''
    from_kwic = KwicQuerySet.as_manager()

    type = models.CharField(max_length=30, default='')
    string = models.CharField(max_length=30)
    lemma = models.CharField(max_length=30)
    pos = models.CharField(max_length=30)
    location = models.CharField(max_length=30)
    n = models.SmallIntegerField(default=0)
    preceding = models.CharField(max_length=300)
    following = models.CharField(max_length=300)
    section_number = models.CharField(max_length=10)
    # 0: non-speech, 1: speech, 2: direct, 3: indirect
    speech_cat = models.SmallIntegerField(default=0)
    # 0: prose, 2: lineated, 3: continuous
    verse_cat = models.SmallIntegerField(default=0)

    @classmethod
    def update_or_create_from_kwik_item(cls, item, token):
        data = cls._get_data_from_kwik_item(item, token)

        ret, _ = cls.objects.update_or_create(
            location=data['location'],
            token_number=data['token_number'],
            defaults=data
        )

        return ret

    @classmethod
    def create_from_kwik_item(cls, item, string):
        ret = cls.new_from_kwik_item(item, string)
        ret.save()

        return ret

    @classmethod
    def new_from_kwik_item(cls, item, string, mss_sections=None,
                           tokenised_data=None):
        return cls(**cls._get_data_from_kwik_item(
            item, string, mss_sections, tokenised_data
        ))

    @classmethod
    def _get_data_from_kwik_item(cls, item, string, mss_sections=None,
                                 tokenised_data=None):
        ret = {
            k.lower().strip(): (v or '').strip()
            for k, v
            in list(item.attrib.items())
            if hasattr(cls, k)
        }
        ret['string'] = (string.text or '').strip()

        if mss_sections:
            ms = 'Royal'
            if 'edfr' in ret['location']:
                ms = 'Fr20125'
            for section in mss_sections[ms]:
                if section['para'] > ret['location']:
                    break
                ret['section_number'] = section['number']

        if tokenised_data:
            verse_cat_index = tokenised_data.get(
                ret['location'], {}
            ).get('verse_cat', 0)
            ret['verse_cat'] = verse_cat_index

            speech_cat_index = tokenised_data.get(
                ret['location'] + '.' + ret['n'], {}
            ).get('speech_cat', 0)
            ret['speech_cat'] = speech_cat_index

        return ret

    def get_unique_id(self):
        ret = '{}.{:03d}'.format(self.location, int(self.n))
        return ret
