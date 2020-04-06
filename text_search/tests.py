# -*- coding: utf-8 -*-
from django.test import TestCase
from text_search.models import AnnotatedToken


class KwicTests(TestCase):
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
            res = AnnotatedToken._normalise_lemma(case[0])
            self.assertEqual(res, case[1], case[0])
