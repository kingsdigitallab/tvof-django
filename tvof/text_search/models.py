# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from . import utils
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel


POS_NAME = 'nom propre'


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
        # app_label = 'text_search'

    def __str__(self):
        return self.label

    def get_white_list(self):
        return [
            l.lower().strip()
            for l
            in self.whitelist.split('\n') if l.strip()
        ]

