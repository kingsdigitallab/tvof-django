# -*- coding: utf-8 -*-

from django.db import models
from xml.etree import ElementTree as ET
from text_viewer.text_viewer_tvof import TextViewerAPITvof
from django.conf import settings
from . import utils
import re

from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel


class SearchFacet(models.Model):
    '''
    Represents editable settings for a search facet.
    Editable in Wagtail admin interface.
    '''
    # see setting.base.SEARCH_FACETS
    key = models.CharField(max_length=32, unique=True, choices=[
        (f['key'], f['key'])
        for f
        in settings.SEARCH_FACETS
    ])
    label = models.CharField(
        max_length=32,
        help_text='The heading for this facet on the search page'
    )

    tooltip = models.CharField(
        max_length=255, blank=True,
        help_text='One short sentence to describe this facet to the users.'
    )
    description = RichTextField(
        blank=True,
        help_text='a more verbose description of the facet'
        ' to appear on a separate help page.'
    )
    whitelist = models.TextField(
        blank=True,
        default='',
        help_text='one facet option per line. If empty all options are visible'
        ', otherwise only the supplied options are visible.'
    )
    display_rank = models.IntegerField(
        default=0,
        help_text='the display order of this facet on the search page, '
        'lower numbers appear on top. NOT YET IMPLEMENTED.'
    )
    is_hidden = models.BooleanField(
        default=False,
        help_text='tick this to hide the facet from the search page'
    )
    limit = models.IntegerField(
        default=-2,
        help_text='maximum number of options to show under this facet. '
        'Special numbers: -1 unlimited, -2 default preset.'
    )

    panels = [
        FieldPanel('key'),
        FieldPanel('label'),
        FieldPanel('is_hidden'),
        FieldPanel('tooltip'),
        FieldPanel('description'),
        FieldPanel('whitelist'),
        # Hidden as it would be slow to make a DB request before each API call
        # FieldPanel('limit'),
        # FieldPanel('display_rank'),
    ]

    class Meta:
        ordering = ['display_rank']

    def __str__(self):
        return self.label

    def get_white_list(self):
        return [
            l.lower().strip()
            for l
            in self.whitelist.split('\n') if l.strip()
        ]


def read_tokenised_data():
    '''
    Read XML file of tokenised texts (Fr & Royal).
    Return a dictionary with information about all the
        <said> elements
        <seg type="6"> verses elements

    That dictionary key is the location of the element and the value
    is a categorisation of the element.

    The output is meant to be combined with a kwic file to build the
    search index.

    <seg type="6" xml:id="edfr20125_00910_07"><lg type="octo_coup">
        <lg type="lineated">
            <l n="001">
                <w n="1">Q[ua]r</w> <w n="2">ele</w> <w n="3">fu</w>
                <w n="4">si</w> <w n="5">bien</w>
                <w n="6">plantee<pc rend="1" /></w>
            </l>
    '''

    lg_types = {'lineated': 2, 'cont': 3, 'unspecified': 4}
    sc_types = {'true': 2, 'false': 3, 'unspecified': 4}

    ret = {}

    for _, path in settings.TOKENISED_FILES.items():
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
                    if seg_id_n not in ret:
                        # we ignore nested <said>
                        ret[seg_id_n] = {
                            'speech_cat': sc_types.get(said_type, 4)
                        }
                    else:
                        # print('Nested {}'.format(seg_id_n))
                        pass

    return ret

# ----------------------------------------------------------------------
# virtual model for kwic / annotated token index
# ----------------------------------------------------------------------


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

        def callback(item, elem):
            if elem is not None:
                token = AnnotatedToken.new_from_kwik_item(
                    item,
                    elem,
                    mss_sections,
                    tokenised_data
                )

                return token

        for res in utils.parse_kwic(settings.KWIC_FILE_PATH, callback):
            yield res

    def __iter__(self):
        return self._read_from_kwic()

    def _read_from_kwic(self):
        '''
        An generator for a given slice of the query result.
        See Django QuerySet
        '''
        if self.query.low_mark < self.next_mark:
            # print('NEW', self.query.low_mark, self.next_mark)
            self.generator = self.get_generator()
            self.next_mark = 0

        while self.query.high_mark > self.next_mark:
            g = next(self.generator)
            self.next_mark, token = g
            if self.query.low_mark < self.next_mark:
                yield token

    def count(self):
        return self._count_or_save()

    def _count_or_save(self, save=False):
        '''
        return the number of tokens in the kwic file.
        if save = True, save those token in the database
        (for debugging or research purpose only).
        '''

        if not (save or self._count is None):
            return self._count

        self._count = 0
        if self.max_count != 0:

            def callback(item, elem):
                if elem is not None:
                    if save:
                        AnnotatedToken(
                            lemma=item.attrib('lemma', ''),
                            string=item.text
                        ).save()
                    return 1

            for _ in utils.parse_kwic(settings.KWIC_FILE_PATH, callback):
                self._count += 1
                if (self.max_count > -1) and (self._count >= self.max_count):
                    break

        return self._count


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

    # most of these field SHOULD match
    # the name of the related attrbutes in the kwic.xml file
    lemma = models.CharField(max_length=30)
    pos = models.CharField(max_length=30)
    lemmapos = models.CharField(max_length=30, default='')
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
        # for each attribute in kwic <item>
        # copy the value in the field with the same name
        # in the model instance
        ret = {
            k.lower().strip(): (v or '').strip()
            for k, v
            in list(item.attrib.items())
            if hasattr(cls, k.lower())
        }
        # print(ret, string.text)
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

# ----------------------------------------------------------------------
# virtual model for Forms and Lemmas autocomplete index
# ----------------------------------------------------------------------


class AutocompleteFormQuerySet(KwicQuerySet):

    def get_generator(self):
        found = {}

        def normalise(string, lower=False):
            ret = (string or '').strip()
            if lower:
                ret = ret.lower()
            return ret

        def get_new_doc(lemma, form=''):
            '''
            Returns a AutocompleteForm for the given (lemma, form) pair.
            Returns None if that pair was seen before (see found).
            '''
            ret = None

            if lemma:
                key = '{}_{}'.format(lemma, form)
                if key not in found:
                    found[key] = 1
                    ret = AutocompleteForm(lemma=lemma, form=form)

            return ret

        def callback(item, elem):
            lemma = normalise(item.attrib.get('lemma', ''))
            form = ''
            if elem is not None:
                nom_propre = item.attrib.get('pos', '') == 'nom propre'
                form = normalise(elem.text, True)
                if nom_propre:
                    form = form.title()

            doc = get_new_doc(lemma, form)

            if doc:
                return doc

        # parse the kwic file for pairs of (token, lemma)
        # Note: kwic contains tokens,
        # but we normalise them into forms (lowercase).
        for res in utils.parse_kwic(settings.KWIC_FILE_PATH, callback):
            yield res

    def count(self):
        return sum(1 for _ in self.get_generator())


class AutocompleteForm(models.Model):
    from_kwic = AutocompleteFormQuerySet.as_manager()

    form = models.CharField(max_length=30, default='', blank=True)
    lemma = models.CharField(max_length=30, default='')

    def get_unique_id(self):
        ret = '{}_{}'.format(self.lemma, self.form)
        return ret
