# -*- coding: utf-8 -*-
import re

from django.conf import settings

# todo: remove duplication
from django.http import JsonResponse
from elasticsearch_dsl import FacetedSearch, TermsFacet, Search, Q

from .es_indexes import AnnotatedToken, LemmaDocument
from .utils import get_order_fields, get_ascii_from_unicode

'''
TODO
. normalise_lemma, make sure it's used everywhere (same with form)
. OPT: don't return fields we don't need to show
. OPT: don't index fields we don't search on (e.g. following)
'''

ORDER_BY_QUERY_STRING_PARAMETER_NAME = 'order'


def get_config(result_type):
    return settings.SEARCH_CONFIG[result_type]


def view_api_tokens_search_facets(request):
    '''
    ?format=json&result_type=tokens&page=1&text=le&selected_facets=lemma_exact%3Ale&page_size=10&order=form
    '''
    return _view_api_documents_search_facets(request, 'tokens', AnnotatedTokenSearch)


def view_api_lemma_search_facets(request):
    result_type = request.GET.get('result_type', 'lemmata')
    return _view_api_documents_search_facets(request, result_type, LemmaSearch)


def view_api_tokens_autocomplete(request):
    # ?format=json&page_size=50&q=a
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))
    q = get_ascii_from_unicode(request.GET.get('q', '').strip()).lower()

    search = Search(index='autocomplete')
    search = search.query('prefix', autocomplete=q)
    # search = search.query(Q("prefix", lemma=q) | Q("prefix", form=q))
    search = search[(page-1)*page_size:(page)*page_size]
    search = search.sort('autocomplete_sortable')
    res = search.execute()

    hit_counts = _get_hits_count_from_es_response(res)

    ret = {
        'count': hit_counts,
        'previous': _get_pagination_url(request, hit_counts, page, page_size, -1),
        'next': _get_pagination_url(request, hit_counts, page, page_size, 1),
        'results': [
            {
                'lemma': hit.lemma,
                'form': hit.form,
                'id': hit.meta.id,
            }
            for hit
            in res.hits
        ]
    }
    return JsonResponse(ret)


def _get_terms_facets(keys=None):
    '''Returns a dictionary of TermsFacets
    for the given facet keys.
    keys = a list of field slugs/keys
    If keys is None, returns all possible facets.
    '''
    return {
        facet['key']: TermsFacet(
            field=facet['key'],
            size=facet.get('limit', settings.ELASTICSEARCH_FACET_OPTIONS_LIMIT)
        )
        for facet
        in settings.SEARCH_FACETS
        if keys is None or facet['key'] in keys
    }


class TVOFFacetedSearch(FacetedSearch):
    def search(self, *args, **kwargs):
        s = super().search(*args, **kwargs)
        return s


class AnnotatedTokenSearch(TVOFFacetedSearch):
    doc_types = [AnnotatedToken]
    # todo search should be case insensitive
    fields = ['searchable']
    facets = _get_terms_facets()


class LemmaSearch(TVOFFacetedSearch):
    doc_types = [LemmaDocument]
    # todo search should be case insensitive
    fields = ['lemma.searchable']
    facets = _get_terms_facets(['name_type', 'pos'])


def _view_api_documents_search_facets(request, result_type, search_class):
    '''
    ?format=json&result_type=tokens&page=1&text=le&selected_facets=lemma_exact%3Ale&page_size=10&order=form
    '''

    # TODO: optimisation, only fetch the fields we need
    # s.source(['title', 'body'])

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
    page_size = int(request.GET.get(
        'page_size', settings.SEARCH_PAGE_SIZE_DEFAULT
    ))

    # search for lemma or form
    text = request.GET.get('text', '')

    selected_facets = {}
    # {'manuscript_number': ['1'], 'lemma': ['et']}
    for f in request.GET.getlist('selected_facets', []):
        parts = f.split(':')
        if len(parts) == 2:
            facet_key = parts[0].replace('_exact', '')
            if facet_key in search_class.facets:
                if facet_key not in selected_facets:
                    selected_facets[facet_key] = []

                selected_facets[facet_key].append(
                    _cast_facet_option(facet_key, parts[1])
                )

    # actual search
    search = search_class(
        text,
        filters=selected_facets,
        sort=get_order_fields(request, result_type, True),
    )
    search = search[(page-1)*page_size:(page)*page_size]
    res = search.execute()

    # hits
    for hit in res:
        ret['objects']['results'].append(hit.to_dict())

    hits_count = _get_hits_count_from_es_response(res)

    # facets
    # if len(selected_facets) == 1 and len(list(selected_facets.values())[0]) == 1:
    truncated_option_count = hits_count
    for facet_key, options in res.facets.to_dict().items():
        ret['fields'][facet_key] = [
            {
                'text': option[0],
                'count': option[1],
            }
            for option
            in options
        ]
        # Add the option we are filtering on in case it has been truncated.
        # Facets options are sorted by frequency and truncated.
        # e.g. filter by an rare lemma, like quem
        for option in selected_facets.get(facet_key, []):
            if option not in [o[0] for o in options]:
                ret['fields'][facet_key].append({
                    'text': option,
                    'count': truncated_option_count,
                })

    ret['objects']['count'] = hits_count
    ret['objects']['previous'] = _get_pagination_url(request, hits_count, page, page_size, -1)
    ret['objects']['next'] = _get_pagination_url(request, hits_count, page, page_size, 1)

    return JsonResponse(ret)


def _cast_facet_option(facet_key, option):
    '''converts the given option into the right type
    for the given facet.
    Why?
    elasticsearch_dsl won't set the selected options to True
    in the search response if the filter option is not the right type.
    E.g. faceted field is Integer but we use an str in the filters
    that we pass to the search function => correct results and filtering
    but selected entry remains False.
    '''
    ret = option
    for facet_info in settings.SEARCH_FACETS:
        if facet_info['key'] == facet_key:
            facet_type = facet_info.get('type', None)
            if facet_type is not None:
                try:
                    ret = facet_type(option)
                except:
                    # TODO: why are we silencing exception here?
                    pass

            break

    return ret


def _get_hits_count_from_es_response(res):
    '''Returns the total number of hits from a ES response object.
    By default the total is capped at 10000.
    A more exact number can be derived from res.facets.

    ES won't return exact number > 10000
    res.hits.total = {'relation': 'gte', 'value': 10000}

    Note that one or more facet options can be selected.
    If none selected: we sum them up.
    Otherwise we only sum the selected ones.

    For this algorithm to work, we need to make sure that:
        1. ALL options > 0 in that facet are always returned.
            I.e. no truncation of options.
        2. ALL options are mutually exclusive.
    '''
    ret = res.hits.total.value

    if res.hits.total.relation != 'eq':
        facets = getattr(res, 'facets', None)
        if facets:
            for meta in settings.SEARCH_FACETS:
                if meta.get('use_for_count', False):
                    facet = getattr(facets, meta['key'], None)
                    if facet:
                        # facet = [(0, 195644, False), (1, 168412, False)]
                        ret = sum([o[1] for o in facet if o[2]])
                        if ret == 0:
                            # no option selected => we add all options
                            ret = sum([o[1] for o in facet])
                        break

    return ret


def _get_pagination_url(request, hits_count, page, page_size, diff):
    qs = request.META['QUERY_STRING'].lstrip('?')
    qs = re.sub(r'\bpage=\d+', '', qs).rstrip('&')

    if page+diff < 1 or (page+diff-1)*page_size >= min(hits_count, settings.SEARCH_RESULT_MAX_SIZE):
        url = None
    else:
        url = '{}://{}{}?{}'.format(
            request.scheme,
            request.META['HTTP_HOST'],
            request.path,
            qs+'&page={}'.format(page+diff)
        )

    return url
