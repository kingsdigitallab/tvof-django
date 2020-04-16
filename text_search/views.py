# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render
from drf_haystack.serializers import (
    HaystackSerializer, HaystackFacetSerializer
)
from drf_haystack.viewsets import HaystackViewSet
from .models import AnnotatedToken, AutocompleteForm
from .search_indexes import AnnotatedTokenIndex, AutocompleteFormIndex
from rest_framework import pagination
from drf_haystack.mixins import FacetMixin
from drf_haystack.filters import HaystackFacetFilter, HaystackFilter
from text_search.models import SearchFacet, Lemma
from drf_haystack.filters import HaystackAutocompleteFilter
from drf_haystack.serializers import HaystackSerializer
from drf_haystack.viewsets import HaystackViewSet
import re
from text_search.search_indexes import LemmaIndex


ITEMS_PER_PAGE = settings.SEARCH_PAGE_SIZES[0]
ORDER_BY_QUERY_STRING_PARAMETER_NAME = 'order'


def get_config(result_type):
    return settings.SEARCH_CONFIG[result_type]


def get_ordered_queryset(view, queryset, result_type):
    order_key = view.request.GET.get(
        ORDER_BY_QUERY_STRING_PARAMETER_NAME, ''
    )
    orders = get_config(result_type)['orders']
    order = orders.get(order_key, list(orders.items())[0][1])

    print(order['fields'])

    return queryset.order_by(*order['fields'])


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

# TODO: replace with ElastiSearch when migrating to cookie cutter


class AnnotatedTokenSerializer(HaystackSerializer):
    '''Description of the structure of a search result (hit)'''

    class Meta:
        # list of search indexes to search on
        index_classes = [AnnotatedTokenIndex]

        # fields to return for each hit
        fields = [
            # although we don't need to return it,
            # without 'text' any keyword search will return everything
            'text',
            'token', 'lemma', 'pos',
            'manuscript_number', 'para_number', 'seg_number', 'token_number',
            'preceding', 'following',
        ]


class AnnotatedTokenSearchPagination(pagination.PageNumberPagination):
    '''Pagination parameters for the searches'''
    page_size = ITEMS_PER_PAGE
    page_size_query_param = 'page_size'
    max_page_size = settings.SEARCH_PAGE_SIZES[-1]


class AnnotatedTokenSearchView(HaystackViewSet):
    '''
    UNUSED: Web API view for non-faceted search
    '''
    index_models = [AnnotatedToken]
    serializer_class = AnnotatedTokenSerializer

    pagination_class = AnnotatedTokenSearchPagination

# ----------------------------
#     Faceted search
# ----------------------------


'''
Facet search is on separate /search/facets/ url.
It returns facets and also the objects (hits).
'''

# field_options settings.SEARCH_FACETS


class AnnotatedTokenFacetSerializer(HaystackFacetSerializer):
    '''
    Description of the search facets
    '''
    # True to returns the tokens / hits with the facets
    serialize_objects = True

    class Meta:
        # list of search indexes to search on
        index_classes = [AnnotatedTokenIndex]

        field_options = {
            f['key']: {
                'limit': f.get('limit', settings.SEARCH_FACET_LIMIT_DEFAULT)
            }
            for f
            in settings.SEARCH_FACETS
        }
        # list of all faceted fields
        fields = list(field_options.keys())


class AnnotatedTokenFacetSearchView(FacetMixin, HaystackViewSet):
    '''
    Web API view for Faceted Search
    '''
    index_models = [AnnotatedToken]

    serializer_class = AnnotatedTokenSerializer

    facet_serializer_class = AnnotatedTokenFacetSerializer

    # HaystackFilter to filter by text/keywords
    # HaystackFacetFilter to filter by selected facets
    facet_filter_backends = [HaystackFilter, HaystackFacetFilter]

    pagination_class = AnnotatedTokenSearchPagination

    def get_queryset(self, *args, **kwargs):
        '''
        Apply order to the queryset.
        The queryset will be filter after that
        by facet_filter_backends[i].filter_queryset()
        '''
        ret = super(AnnotatedTokenFacetSearchView, self).get_queryset()

        return get_ordered_queryset(self, ret, 'tokens')


# AUTOCOMPLETE


class AutocompletePagination(pagination.PageNumberPagination):
    '''Pagination parameters for the autocomplete'''
    page_size = settings.AUTOCOMPLETE_PAGE_SIZES[0]
    page_size_query_param = 'page_size'
    max_page_size = settings.SEARCH_PAGE_SIZES[-1]


class AutocompleteSerializer(HaystackSerializer):

    class Meta:
        index_classes = [AutocompleteFormIndex]
        fields = ['form', 'lemma', 'autocomplete']
        ignore_fields = ['autocomplete']

        # The `field_aliases` attribute can be used in order to alias a
        # query parameter to a field attribute. In this case a query like
        # /search/?q=oslo would alias the `q` parameter to the `autocomplete`
        # field on the index.
        field_aliases = {
            'q': 'autocomplete'
        }


class AutocompleteFilter(HaystackAutocompleteFilter):
    """
    Customisation to allow autocomplete queries with a single letter.

    autocomplete:a will not work woth solr
    because the ngram field needs at least two characters.

    So we turn that type of queries into form__startswith:a

    Assumes that we have a single search term.
    """

    def process_filters(self, filters, queryset, view):
        if not filters:
            return filters

        for i, child in enumerate(filters.children):
            field_name, query = child
            for word in query.split(' '):
                if field_name == 'autocomplete' and len(word) == 1:
                    filters.children[i] = ('form__startswith', query)

        ret = super(AutocompleteFilter, self).process_filters(
            filters, queryset, view
        )
        return ret


class AutocompleteSearchViewSet(HaystackViewSet):

    index_models = [AutocompleteForm]
    serializer_class = AutocompleteSerializer
    filter_backends = [AutocompleteFilter]

    pagination_class = AutocompletePagination

    def get_queryset(self, *args, **kwargs):
        '''
        Apply order to the queryset.
        The queryset will be filter after that
        by facet_filter_backends[i].filter_queryset()
        '''
        ret = super(AutocompleteSearchViewSet, self).get_queryset()

        return ret

# LEMMATA


class LemmaSerializer(HaystackSerializer):
    '''Description of the structure of a search result (hit)'''

    class Meta:
        # list of search indexes to search on
        index_classes = [LemmaIndex]

        # fields to return for each hit
        fields = [
            # although we don't need to return it,
            # without 'text' any keyword search will return everything
            'text',
            'forms', 'lemma', 'pos', 'name_type',
        ]


class LemmaSearchPagination(pagination.PageNumberPagination):
    '''Pagination parameters for the searches'''
    page_size = ITEMS_PER_PAGE
    page_size_query_param = 'page_size'
    max_page_size = settings.SEARCH_PAGE_SIZES[-1]


class LemmaSearchView(HaystackViewSet):
    '''
    UNUSED: Web API view for non-faceted search
    '''
    index_models = [Lemma]
    serializer_class = LemmaSerializer

    pagination_class = LemmaSearchPagination

# ----------------------------
#     Faceted search
# ----------------------------


'''
Facet search is on separate /search/facets/ url.
It returns facets and also the objects (hits).
'''

# field_options settings.SEARCH_FACETS


class LemmaFacetSerializer(HaystackFacetSerializer):
    '''
    Description of the search facets
    '''
    # True to returns the tokens / hits with the facets
    serialize_objects = True

    class Meta:
        # list of search indexes to search on
        index_classes = [LemmaIndex]

        field_options = {
            f['key']: {
                'limit': f.get('limit', settings.SEARCH_FACET_LIMIT_DEFAULT)
            }
            for f
            in settings.SEARCH_FACETS
            # TODO: port that to annotatedtoken class
            if hasattr(LemmaIndex, f['key']) and f['key'] not in ['lemma']
        }
        # list of all faceted fields
        fields = list(field_options.keys())


class LemmaFacetSearchView(FacetMixin, HaystackViewSet):
    '''
    Web API view for Faceted Search
    '''
    index_models = [Lemma]

    serializer_class = LemmaSerializer

    facet_serializer_class = LemmaFacetSerializer

    # HaystackFilter to filter by text/keywords
    # HaystackFacetFilter to filter by selected facets
    facet_filter_backends = [HaystackFilter, HaystackFacetFilter]

    pagination_class = LemmaSearchPagination

    def get_queryset(self, *args, **kwargs):
        '''
        Apply order to the queryset.
        The queryset will be filter after that
        by facet_filter_backends[i].filter_queryset()
        '''
        ret = super(LemmaFacetSearchView, self).get_queryset()

        print(type(ret))

        return get_ordered_queryset(self, ret, 'lemmata')
