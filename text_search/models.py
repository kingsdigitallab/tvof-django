# -*- coding: utf-8 -*-

from django.db import models
from text_viewer.text_viewer_tvof import TextViewerAPITvof
from django.conf import settings
from . import utils
import re

from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from builtins import super

# ./manage.py rebuild_index -b 10000 --noinput


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


# ----------------------------------------------------------------------
# pseudo Django Model for the kwic / annotated token index
# ----------------------------------------------------------------------


class KwicQuerySet(models.QuerySet):
    '''
    A virtual QuerySet
    that always returns all the entries
    read from a kwic XML file (exported from Lemming).

    The purpose is to avoid storing all the kwic data in the database.

    To directly move the entries from the kwic file into the search engine:

    ./manage.py rebuild_index --noinput

    SAVES TIME, MEMORY AND DISK SPACE.

    Support only: all(), count(), len() and slicing of results.
    NO support for any filter, exclude, order_by, etc.

    TODO: simplify or rewrite entirely.
    Perhaps as part of dockerisation we can switch to native ES indexing
    without going through Haystack and this virtual QuerySet.
    The code was very simple and elegant at the beginning
    but it has now become way too complex and very hard to maintain.

    We use self._result_cache defined in QuerySet to populate results.
    '''

    max_count = settings.SEARCH_INDEX_LIMIT

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._count = None
        # will be shared with sub-querysets, leave it {}
        self.mss_sections = {}
        self.tokenised_data = {}
        # We need a default parser here so it can be shared with sub-queryset
        self.set_parser()

    def _clone(self, *args, **kwargs):
        ret = super()._clone(*args, **kwargs)
        ret._count = self._count
        ret.parser = self.parser
        ret.mss_sections = self.mss_sections
        ret.tokenised_data = self.tokenised_data

        return ret

    def set_parser(self, from_mark=0):
        '''
        set self.parser with a new KwicParser.
        Keep existing one if it can be reused for parsing from from_mark.

        Returns True only if a new parser was set.
        '''
        parser = getattr(self, 'parser', None)
        if parser and from_mark >= self.parser.next_mark:
            # we can reuse the existing parser and its generator
            return False

        self.parser = self._new_parser()

        return True

    def _new_parser(self):
        def callback(item):
            if not self.mss_sections:
                # print('  REQUEST')
                tvof_viewer = TextViewerAPITvof()
                self.mss_sections.update(tvof_viewer.read_all_sections_data())

            if not self.tokenised_data:
                self.tokenised_data.update(utils.read_tokenised_data())

            token = AnnotatedToken.new_from_kwik_item(
                item,
                self.mss_sections,
                self.tokenised_data,
            )

            return [token]

        return utils.KwicParser(callback)

    def _fetch_all(self):
        '''Fetch the result of this QuerySet (it could just be a slice).
        Needed for many QuerySet methods like.
        len(), count(), [:], __iter__'''

        # return cached result
        if self._result_cache:
            return self._result_cache

        # reset the generator if it's ahead of the query lower bound
        self.set_parser(self.query.low_mark)

        _result_cache = []

        generator = self.parser.get_generator(self.query.low_mark)

        while self.query.high_mark is None or self.query.high_mark > self.parser.next_mark:
            token = next(generator, None)
            if token is None:
                break
            if self.query.low_mark < self.parser.next_mark:
                _result_cache.append(token)

        self._result_cache = _result_cache
        if len(self._result_cache) > 1000:
            print('WARNING large cached result {}'.format(
                len(self._result_cache))
            )

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

            def callback(item):
                if save:
                    AnnotatedToken(
                        lemma=item.attrib('lemma', ''),
                        string=item.text
                    ).save()
                return [1]

            for _ in utils.KwicParser(callback):
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

    # this manager will read entries from the XML file, not the DB
    from_kwic = KwicQuerySet.as_manager()

    type = models.CharField(max_length=30, default='')
    string = models.CharField(max_length=30)

    # most of these field SHOULD match
    # the name of the related attributes in the kwic.xml file
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
    def update_or_create_from_kwik_item(cls, item):
        data = cls._get_data_from_kwik_item(item)

        ret, _ = cls.objects.update_or_create(
            location=data['location'],
            token_number=data['token_number'],
            defaults=data
        )

        return ret

    def __str__(self):
        return '{} [{}]'.format(self.string, self.lemma)

    @classmethod
    def create_from_kwik_item(cls, item, string):
        ret = cls.new_from_kwik_item(item, string)
        ret.save()

        return ret

    @classmethod
    def new_from_kwik_item(cls, item, mss_sections=None, tokenised_data=None):
        return cls(**cls._get_data_from_kwik_item(
            item, mss_sections, tokenised_data
        ))

    @classmethod
    def _normalise_lemma(cls, lemma):
        ret = lemma
        # porfit(i)er => porfitier
        ret = re.sub(r'(\w)\(([^\)]+)\)', r'\1\2', ret)
        # maintas (a) => maintas, a
        # rechief (de) => rechief, de
        ret = re.sub(r'^(.*) \(([^\)]+)\)', r'\1, \2', ret)

        ret = ret.strip()

        return ret

    @classmethod
    def _get_data_from_kwik_item(cls, item, mss_sections=None,
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
        ret['string'] = (item.text or '').strip()

        ret['lemma'] = cls._normalise_lemma(ret.get('lemma', ''))

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

    def _new_parser(self):
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

        def callback(item):
            lemma = normalise(item.attrib.get('lemma', ''))
            nom_propre = item.attrib.get('pos', '') == 'nom propre'
            form = normalise(item.text, True)
            if nom_propre:
                form = form.title()

            return [
                r
                for r
                in [get_new_doc(lemma), get_new_doc(lemma, form)]
                if r
            ]

        return utils.KwicParser(callback)

    def count(self):
        return sum(1 for _ in self._new_parser())


class AutocompleteForm(models.Model):
    from_kwic = AutocompleteFormQuerySet.as_manager()

    form = models.CharField(max_length=30, default='', blank=True)
    lemma = models.CharField(max_length=30, default='')

    def get_unique_id(self):
        ret = '{}_{}'.format(self.lemma, self.form)
        return ret

    def __str__(self):
        return '{} [{}]'.format(self.form, self.lemma)
