# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from ... import utils
from argparse import RawTextHelpFormatter


class Command(BaseCommand):
    help = '''Text Search toolbox. Mainly about ElasticSearch indexing.

action:
  list (ls)
    list the indexes
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
        parser.add_argument('-idx', nargs='?', type=str, help='comma separated list of index names the action applies to. All if not specified.')
        parser.add_argument('-cap', nargs='?', type=int, default=-1, help='maximum number of item to index. All if -1 or not specified.')
        parser.add_argument('args', nargs='*', type=str)

    def handle(self, *args, **options):

        self.options = options
        self.args = args
        actions = options.get('action', [])
        action = actions[0]

        self.indexes = []
        index_names = (options.get('idx', '') or '')
        if index_names:
            self.indexes = [
                idx.strip()
                for idx in index_names.split(',')
            ]

        self.cap = options.get('cap', -1)

        known_action = False

        from time import time
        t0 = time()

        from tvof.text_search.es_indexes import Indexer
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

        if action in ['list', 'ls']:
            known_action = True
            self.action_list_index()

        if action == 'import':
            print('ERROR: Deprecated, use rebuild_index command instead.')

        if action == 'clear':
            print('ERROR: Deprecated, use clear_index command instead.')

        if action == 'test_names':
            known_action = True
            utils.read_tokenised_name_types()

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
        self.indexer.rebuild(self.indexes, self.cap)

    def action_clear_index(self):
        self.indexer.clear(self.indexes)

    def action_list_index(self):
        self.indexer.list(self.indexes)

    def action_transform_kwic(self):
        utils.write_kwic_index(True)
