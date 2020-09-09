# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from text_search.models import AnnotatedToken
from argparse import RawTextHelpFormatter
import os

from text_search.utils import read_tokenised_name_types


class Command(BaseCommand):
    help = '''Toolbox for the Text Viewer app

action:
  clear
    remove all records in AnnotatedToken table
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

        if action == 'import':
            print('ERROR: Deprecated, use rebuild_index command instead.')
            known_action = True

        if action == 'clear':
            known_action = True
            self.action_clear()

        if action == 'test_names':
            known_action = True
            read_tokenised_name_types()

        if action == 'index':
            known_action = True
            self.action_index()

        if not known_action:
            print('ERROR: unknown action "%s"' % action)
            print(self.help)
        else:
            print('done')

    def get_args(self):
        return self.args

    def action_clear(self):
        AnnotatedToken.objects.all().delete()

    def action_index(self):
        '''indexing with ES'''

        pass
