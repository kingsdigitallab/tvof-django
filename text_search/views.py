# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render
from drf_haystack.serializers import (
    HaystackSerializer, HaystackFacetSerializer
)
from drf_haystack.viewsets import HaystackViewSet
from .models import AnnotatedToken
from .search_indexes import AnnotatedTokenIndex
from rest_framework import pagination
from drf_haystack.mixins import FacetMixin
from drf_haystack.filters import HaystackFacetFilter


ITEMS_PER_PAGE = settings.SEARCH_PAGE_SIZES[0]
ORDER_BY_QUERY_STRING_PARAMETER_NAME = 'order'


def search_view(request):
    return render(request, 'text_search/search.html', {'title': 'Search'})


class AnnotatedTokenSerializer(HaystackSerializer):
    '''Description of the structure of a search result (hit)'''

    class Meta:
        # list of search indexes to search on
        index_classes = [AnnotatedTokenIndex]

        # fields to return for each hit
        fields = [
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
            'token': {
                'limit': 10,
            },
            'lemma': {
                'limit': 10,
            },
            'pos': {},
            'speech_cat': {},
            'verse_cat': {},
            'manuscript_number': {},
            'section_number': {},
            'is_rubric': {},
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

    facet_filter_backends = [HaystackFacetFilter]

    pagination_class = AnnotatedTokenSearchPagination

    def get_queryset(self, *args, **kwargs):
        '''
        See https://github.com/inonit/drf-haystack/issues/114
        We apply the normal search before faceting.
        By default FacetMixin disables the normal search.
        '''
        ret = super(AnnotatedTokenFacetSearchView, self).get_queryset()

        # order by

        order_key = self.request.GET.get(
            ORDER_BY_QUERY_STRING_PARAMETER_NAME, ''
        )
        order_keys = list(settings.SEARCH_PAGE_ORDERS.keys())
        if order_key not in order_keys:
            order_key = order_keys[0]
        order = settings.SEARCH_PAGE_ORDERS[order_key]
        ret = ret.order_by(*order['fields'])

        return ret
