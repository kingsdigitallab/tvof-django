# -*- coding: utf-8 -*-
from django.conf import settings

# todo: remove duplication
from django.http import JsonResponse
from elasticsearch_dsl import FacetedSearch, TermsFacet
from elasticsearch_dsl.connections import connections

from text_search.es_indexes import AnnotatedToken

ITEMS_PER_PAGE = settings.SEARCH_PAGE_SIZES[0]
ORDER_BY_QUERY_STRING_PARAMETER_NAME = 'order'

connections.create_connection(hosts=['localhost'])

def get_config(result_type):
    return settings.SEARCH_CONFIG[result_type]


def view_api_tokens_search_facets(request):
    '''
    ?format=json&result_type=tokens&page=1&text=le&selected_facets=lemma_exact%3Ale&page_size=10&order=form
    :param request:
    :return:
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
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))
    # search for lemma or form
    text = request.GET.get('text', '')

    from elasticsearch import Elasticsearch
    client = Elasticsearch()

    search = AnnotatedTokenSearch(text)
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

    return JsonResponse(ret)


class AnnotatedTokenSearch(FacetedSearch):
    doc_types = [AnnotatedToken, ]
    fields = ['form', 'lemma']

    facets = {
        'lemma': TermsFacet(field='lemma'),
    }
