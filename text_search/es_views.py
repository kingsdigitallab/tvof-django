# -*- coding: utf-8 -*-
import re

from django.conf import settings

# todo: remove duplication
from django.http import JsonResponse
from elasticsearch import Elasticsearch
from elasticsearch_dsl import FacetedSearch, TermsFacet, Search
from elasticsearch_dsl.connections import connections

from text_search.es_indexes import AnnotatedToken, LemmaDocument
from text_search.utils import get_order_fields

'''
TODO:
1 Names
1 Lemmata
. auto-complete
1 pagination

. text search should be case insensitive
1 sort by
. number of options per facet
. speech_cat & verse_cat
. exact number of hits
. test grouping of tokens for names
'''

ITEMS_PER_PAGE = settings.SEARCH_PAGE_SIZES[0]
ORDER_BY_QUERY_STRING_PARAMETER_NAME = 'order'

connections.create_connection(hosts=['localhost'])


def get_config(result_type):
    return settings.SEARCH_CONFIG[result_type]

def view_api_tokens_search_facets(request):
    '''
    ?format=json&result_type=tokens&page=1&text=le&selected_facets=lemma_exact%3Ale&page_size=10&order=form
    '''
    return _view_api_documents_search_facets(request, 'tokens', AnnotatedTokenSearch)

def view_api_lemma_search_facets(request):
    return _view_api_documents_search_facets(request, 'lemmata', LemmaSearch)

def view_api_tokens_autocomplete(request):
    # ?format=json&page_size=50&q=a
    client = Elasticsearch()
    s = Search(using=client, index='tokens')
    s = s.suggest('abc', request.GET.get('q' , ''), completion={'field': 'preceding'})
    r = s.execute()
    print(r)
    ret = {}
    return JsonResponse(ret)


class AnnotatedTokenSearch(FacetedSearch):
    doc_types = [AnnotatedToken]
    # todo search should be case insensitive
    fields = ['form', 'lemma']

    facets = {
        facet['key']: TermsFacet(field=facet['key'])
        for facet
        in settings.SEARCH_FACETS
    }

    def search(self, *args, **kwargs):
        s = super().search(*args, **kwargs)
        return s

class LemmaSearch(FacetedSearch):
    doc_types = [LemmaDocument]
    # todo search should be case insensitive
    fields = ['lemma_sort']

    facets = {
        facet['key']: TermsFacet(field=facet['key'])
        for facet
        in settings.SEARCH_FACETS
    }

    def search(self, *args, **kwargs):
        s = super().search(*args, **kwargs)
        return s

def _view_api_documents_search_facets(request, index_name, search_class):
    '''
    ?format=json&result_type=tokens&page=1&text=le&selected_facets=lemma_exact%3Ale&page_size=10&order=form
    '''

    # compatible schema with API v1, which came from drf-haystack.
    # so we don't have to change the UI at all; drop in replacement.
    ret = {
        'fields': {},
        'objects': {
            'count': 0,
            'next': None,
            'previous': None,
            'results': [],
        },
    }

    # todo: error management

    # parse the request
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))
    # search for lemma or form
    text = request.GET.get('text', '')
    selected_facets = {}
    # {'manuscript_number': '1', 'lemma': 'et'}
    for f in request.GET.getlist('selected_facets', []):
        parts = f.split(':')
        if len(parts) == 2:
            facet_key = parts[0].replace('_exact', '')
            if facet_key not in selected_facets:
                selected_facets[facet_key] = []
            selected_facets[facet_key].append(parts[1])

    # actual search
    search = search_class(
        text,
        filters=selected_facets,
        sort=get_order_fields(request, index_name, True),
    )
    search = search[(page-1)*page_size:(page)*page_size]
    res = search.execute()

    # facets
    for facet_key, options in res.facets.to_dict().items():
        ret['fields'][facet_key] = [
            {
                'text': option[0],
                'count': option[1],
            }
            for option
            in options
        ]

    # hits
    for hit in res:
        ret['objects']['results'].append(hit.to_dict())

    ret['objects']['count'] = res.hits.total.value

    _add_pagination_to_response(request, ret, res, page, page_size, 1)
    _add_pagination_to_response(request, ret, res, page, page_size, -1)

    return JsonResponse(ret)



def _add_pagination_to_response(request, response, results, page, page_size, diff):
    qs = request.META['QUERY_STRING'].lstrip('?')
    qs = re.sub(r'\bpage=\d+', '', qs)
    key = 'previous'
    if diff > 0:
        key = 'next'

    if page+diff < 1 or (page+diff-1)*page_size >= results.hits.total.value:
        url = None
    else:
        url = '{}://{}{}?{}'.format(
            request.scheme,
            request.META['HTTP_HOST'],
            request.path,
            qs+'&page={}'.format(page+diff)
        )

    response['objects'][key] = url




