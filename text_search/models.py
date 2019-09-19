# -*- coding: utf-8 -*-

from django.db import models
from django.db.models.query import BaseIterable
from xml.etree import ElementTree as ET

kwic_file_path = 'kwic-out.xml'


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
        next_mark = 0
        # print('iterparse', id(self))
        for event, elem in ET.iterparse(kwic_file_path, events=['start']):
            if elem.tag == 'item':
                item = elem
            if elem.tag == 'string':
                token = AnnotatedToken.new_from_kwik_item(item, elem)
                next_mark += 1
                # print(token.location, next_mark)
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
        if self._count is None:
            self._count = 0
            for event, elem in ET.iterparse(kwic_file_path, events=['start']):
                if elem.tag == 'string':
                    self._count += 1
            self._count = 1000

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
    lemma = models.CharField(max_length=30)
    pos = models.CharField(max_length=30)
    location = models.CharField(max_length=30)
    n = models.SmallIntegerField(default=0)
    preceding = models.CharField(max_length=300)
    following = models.CharField(max_length=300)

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
    def new_from_kwik_item(cls, item, string):
        return cls(**cls._get_data_from_kwik_item(item, string))

    @classmethod
    def _get_data_from_kwik_item(cls, item, string):
        ret = {
            k.lower().strip(): (v or '').strip()
            for k, v
            in list(item.attrib.items())
            if hasattr(cls, k)
        }
        ret['string'] = (string.text or '').strip()

        return ret
