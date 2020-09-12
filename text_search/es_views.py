# -*- coding: utf-8 -*-
from django.conf import settings

# todo: remove duplication
from django.http import JsonResponse

ITEMS_PER_PAGE = settings.SEARCH_PAGE_SIZES[0]
ORDER_BY_QUERY_STRING_PARAMETER_NAME = 'order'


def get_config(result_type):
    return settings.SEARCH_CONFIG[result_type]


def view_api_tokens_search_facets(request):
    '''
    ?format=json&result_type=tokens&page=1&text=le&selected_facets=lemma_exact%3Ale&page_size=10&order=form
    :param request:
    :return:
    '''

    # compatible schema with v1, which came from drf-haystack
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
    from elasticsearch_dsl import Search
    from elasticsearch_dsl import Q

    client = Elasticsearch()

    s = Search(using=client, index='tokens')
    if text:
        q = Q('multi_match', query=text, fields=['string', 'lemma'])
        s = s.query(q)
    s = s[(page-1)*page_size:(page)*page_size]
    r = s.execute()

    for hit in r:
        ret['objects']['results'].append(hit.to_dict())

    ret['objects']['count'] = r.hits.total.value

    return JsonResponse(ret)
