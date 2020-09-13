# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from text_search import utils
from text_search.models import AnnotatedToken
from argparse import RawTextHelpFormatter
import os

from text_search.utils import read_tokenised_name_types


class Command(BaseCommand):
    help = '''Text Search toolbox. Mainly about ElasticSearch indexing.

action:
  rebuild_index (ri)
    rebuild the index
    (transform the kwic first if needed)
  clear_index (ci)
    delete the index
  transform_kwic (tk)
    tranform the kwic-out XML file exported from Lemming
    into another XML file that can be directly indexed

deprecated actions:
  clear
    remove all records in AnnotatedToken table
  import
    '''

    def create_parser(self, *args, **kwargs):
        parser = super(Command, self).create_parser(*args, **kwargs)
        parser.formatter_class = RawTextHelpFormatter
        return parser

    def add_arguments(self, parser):
        parser.add_argument('action', nargs=1, type=str)
        parser.add_argument('args', nargs='*', type=str)

    def handle(self, *args, **options):

        self.options = options
        self.args = args
        actions = options.get('action', [])
        action = actions[0]

        known_action = False

        from time import time
        t0 = time()

        from text_search.es_indexes import Indexer
        self.indexer = Indexer()

        if action in ['rebuild_index', 'ri']:
            known_action = True
            self.action_rebuild_index()

        if action in ['clear_index', 'ci']:
            known_action = True
            self.action_clear_index()

        if action in ['transform_kwic', 'tk']:
            known_action = True
            self.action_transform_kwic()

        if action == 'import':
            print('ERROR: Deprecated, use rebuild_index command instead.')

        if action == 'clear':
            print('ERROR: Deprecated, use clear_index command instead.')

        if action == 'test_names':
            known_action = True
            read_tokenised_name_types()

        if not known_action:
            print('ERROR: unknown action "%s"' % action)
            print(self.help)
            exit(1)
        else:
            d = time() - t0
            print('done ("textsearch {}" in {:.0f} s.)'.format(action, d))

    def get_args(self):
        return self.args

    def action_rebuild_index(self):
        self.indexer.rebuild()

    def action_clear_index(self):
        self.indexer.clear()

    def action_transform_kwic(self):
        utils.write_kwic_index(True)
