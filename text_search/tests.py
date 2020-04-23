# -*- coding: utf-8 -*-
from django.test import TestCase
from text_search.models import AnnotatedToken, AutocompleteForm
from django.conf import settings
import os
from text_search.utils import normalise_lemma


class KwicTests(TestCase):
    '''
    ./manage.py test -k -v 2 text_search.tests.KwicTests.test_tokens_slices

    TODO: disable the unit tests which consume too much time or mem.
    '''

    def _test_parenthesis_in_lemma(self):
        for token in AnnotatedToken.from_kwic.all():
            # if token.lemma == ''
            pass

    def test_parenthesis_in_lemma(self):
        # ac-???
        cases = [
            ['porfitier',  'porfitier'],
            ['porfitier ',  'porfitier'],
            ['porfit(i)er',  'porfitier'],
            ['maintas (a) ', 'maintas, a'],
            ['rechief (de)', 'rechief, de'],
        ]

        for case in cases:
            res = normalise_lemma(case[0])
            self.assertEqual(res, case[1], case[0])

    def test_transform(self):
        from text_search import utils
        res = utils.write_kwic_index()

        self.assertTrue(os.path.exists(res))

    def test_tokens_fetchall(self):
        qs = AnnotatedToken.from_kwic.all()
        print(1)
        l1 = qs[5:10]
        print(2)
        l1 = list(l1)
        print(3)
        self.assertEqual(len(l1), 5)

    def test_tokens_slices(self):
        self._test_slices(AnnotatedToken.from_kwic.all())

    def _test_slices(self, qs):
        def lstr(l):
            return ''.join([repr(li) for li in l])

        print('=' * 4)
        l1 = list(qs[0:2])
        self.assertEquals(len(l1), 2)
        print('=' * 4)
        l2 = list(qs[2:4])
        self.assertEquals(len(l2), 2)
        print('=' * 4)
        l3 = list(qs[3:4])
        self.assertEquals(len(l3), 1)
        print('=' * 4)
        l4 = list(qs[0:3])
        self.assertEquals(len(l4), 3)
        print('=' * 4)
        l5 = list(qs[0:4])
        self.assertEquals(len(l5), 4)

        self.assertNotEquals(
            lstr(l1),
            lstr(l2),
            'l1 == l2'
        )
        self.assertEqual(
            lstr(l1) + lstr(l2),
            lstr(l5),
            'l1+l2 != l5'
        )
        self.assertEqual(
            lstr(l1) + lstr(l2),
            lstr(l4) + lstr(l3),
            'l1+l2 != l4+l3'
        )

    def test_tokens(self):
        for token in AnnotatedToken.from_kwic.all():
            if ' ' in token.lemma:
                print('{} [{}, {}] @ {} {}'.format(
                    token.string, token.lemma, token.pos,
                    token.location, token.n)
                )

    def test_tokens_count(self):
        cnt2 = len(AnnotatedToken.from_kwic.all())
        cnt = AnnotatedToken.from_kwic.count()
        self.assertEqual(cnt, cnt2)

    def test_autocomplete_slices(self):
        self._test_slices(AutocompleteForm.from_kwic.all())

    def test_autocomplete_count(self):
        cnt = AutocompleteForm.from_kwic.count()
        cnt2 = len(AutocompleteForm.from_kwic.all())
        self.assertEqual(cnt, cnt2)

    def test_autocomplete(self):
        for rec in AutocompleteForm.from_kwic.all():
            self.assertTrue(rec.lemma)
            self.assertTrue(rec.lemma == rec.lemma.strip())
            self.assertTrue(rec.form == rec.form.strip())
