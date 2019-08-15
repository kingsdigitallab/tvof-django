# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from text_search.models import AnnotatedToken
from argparse import RawTextHelpFormatter


class Command(BaseCommand):
    help = '''Toolbox for the Text Viewer app

action:
  import PATH_TO_KWIC.XML
    insert / update data from kwic.xml into AnnotatedToken table
    PATH_TO_KWIC.XML is the output from Lemming lemmatiser
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
            known_action = True
            self.action_import()

        if action == 'clear':
            known_action = True
            self.action_clear()

        if not known_action:
            print('ERROR: unknown action "%s"' % action)
            print(self.help)
        else:
            print('done')

    def get_args(self):
        return self.args

    def action_clear(self):
        AnnotatedToken.objects.all().delete()

    def action_import(self):
        args = self.get_args()
        if len(args) < 1:
            print('ERROR: please provide path to kwic.xml file')
            return
        input_path = args[0]

        import os
        if not os.path.exists(input_path):
            print('ERROR: input file not found, please check the path')
            return

        '''
        <?xml version="1.0" encoding="UTF-8"?>
        <kwiclist>
          <sublist key="·c·">
            <item type="seg_item" location="edfr20125_00598_08" n="23"
                preceding="chargees , ele lor envoia ·xx· bues et"
                following="pors et ·c· moutons cras et autant"
                lemma="cent">
              <string>·c·</string>
            </item>
        '''

        # TODO: avoid reading the whole file at once, use a lot of memory
        import xml.etree.ElementTree as ET
        tree = ET.parse(input_path)
        root = tree.getroot()

        from tqdm import tqdm
        import logging
        logger = logging.getLogger('kwic')
        logger.info('-'*20)
        logger.info('import {}'.format(input_path))

        stats = {
            'forms': 0,
            'tokens': 0,
            'skipped': 0,
        }
        for sublist in tqdm(root.findall('sublist')):
            token = sublist.attrib.get('key')
            stats['forms'] += 1
            for item in sublist.iter('item'):
                string = item.find('string')
                if string is not None:
                    string = (string.text or '').strip()
                if not item.attrib.get('lemma', None):
                    logger.warning('missing lemma {} {}'.format(string or token, repr(item.attrib)))
                    stats['skipped'] += 1
                    continue
                AnnotatedToken.update_or_create_from_kwik_item(
                    item, string or token
                )
                stats['tokens'] += 1

        logger.info('imported {} forms, {} tokens; skipped {} tokens (due to missing lemma).'.format(
            stats['forms'], stats['tokens'], stats['skipped']
        ))
        logger.info('done')
        print('done. check the logs for details.')
