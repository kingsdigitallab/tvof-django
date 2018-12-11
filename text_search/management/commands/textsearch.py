# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from text_search.models import AnnotatedToken


class Command(BaseCommand):
    help = 'Toolbox for the Text Viewer app'

    def add_arguments(self, parser):
        parser.add_argument('actions', nargs=1, type=str)
        parser.add_argument('args', nargs='*', type=str)

    def handle(self, *args, **options):

        self.options = options
        self.args = args
        actions = options.get('actions', [])
        action = actions[0]

        known_action = False

        if action == 'import':
            known_action = True
            self.action_import()

        if action == 'clear':
            known_action = True
            self.action_clear()

        if not known_action:
            print 'ERROR: unknown action "%s"' % action
        else:
            print 'done'

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

        for sublist in root.iter('sublist'):
            token = sublist.attrib.get('key')
            print(token)
            for item in sublist.iter('item'):
                AnnotatedToken.update_or_create_from_kwik_item(
                    item, token
                )
