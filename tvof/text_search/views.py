# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render
from .models import SearchFacet
import re
from .utils import get_search_config, get_order_fields

ITEMS_PER_PAGE = settings.SEARCH_PAGE_SIZES[0]


def get_ordered_queryset(view, queryset, result_type):
    fields = get_order_fields(view.request, result_type)
    return queryset.order_by(*fields)


def transform_search_facets(content):
    '''
    {{search_facets}} in a wagtail page content
    will be expanded into a list of facet definitions
    as described in the database (see SearchFacet)
    '''

    def replace(match):
        ret = ''
        for f in SearchFacet.objects.all():
            if f.description:
                # TODO: the id shoudl be asssigned to first heading instead...
                ret += '<span id="{}">&nbsp;</span>'.format(f.key)
                ret += f.description

        return ret

    content = re.sub(
        r'<p>\s*\{\{\s*search_facets\s*\}\}\s*</p>', replace, content
    )

    return content


def search_view(request):
    ''' returns initial search view
    with context for the vuejs app
    context contains all facet definitions
    definitions first comes from settings.SEARCH_FACETS
    but can be overwritten by the database facet records
    '''

    facets = {
        f.key: f
        for f
        in SearchFacet.objects.all()
    }

    search_facets = []
    for f in settings.SEARCH_FACETS:
        fdb = facets.get(f['key'], None)
        search_facet = {
            'key': f['key'],
            'label': f['label'],
            'href': '#',
        }

        if fdb:
            whitelist = fdb.get_white_list()
            if whitelist:
                search_facet['whitelist'] = whitelist
            if fdb.is_hidden:
                search_facet['is_hidden'] = True
            if fdb.label:
                search_facet['label'] = fdb.label
            if fdb.limit != -2:
                search_facet['limit'] = fdb.limit
            if fdb.tooltip:
                search_facet['tooltip'] = fdb.tooltip
            if fdb.description:
                search_facet['href'] = settings.SEARCH_FACETS_INFO_PATH + \
                    '#' + f['key']
                if not search_facet.get('tooltip', None):
                    search_facet['tooltip'] = 'Search help'

        search_facets.append(search_facet)

    context = {
        'title': 'Search',
        'search_facets': search_facets,
    }
    return render(request, 'text_search/search.html', context)

