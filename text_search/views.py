# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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


ITEMS_PER_PAGE = 10


def search_view(request):
    return render(request, 'text_search/search.html', {'title': 'Search'})


class AnnotatedTokenSerializer(HaystackSerializer):
    class Meta:
        # The `index_classes` attribute is a list of which search indexes
        # we want to include in the search.
        index_classes = [AnnotatedTokenIndex]

        fields = [
            'text',
            'token', 'preceding', 'following', 'lemma', 'location',
            'token_number', 'pos'
        ]


class AnnotatedTokenSearchPagination(pagination.PageNumberPagination):
    page_size = ITEMS_PER_PAGE


class AnnotatedTokenSearchView(HaystackViewSet):
    index_models = [AnnotatedToken]
    serializer_class = AnnotatedTokenSerializer

    pagination_class = AnnotatedTokenSearchPagination

# ----------------------------
#     Faceted search
# ----------------------------


if 1:

    '''
    Facet search is on separate /search/facets/ url.
    It returns facets and also the objects (hits).
    '''

    class AnnotatedTokenFacetSerializer(HaystackFacetSerializer):
        # True to returns the tokens / hits with the facets
        serialize_objects = True

        class Meta:
            # The `index_classes` attribute is a list of which search indexes
            # we want to include in the search.
            index_classes = [AnnotatedTokenIndex]

            field_options = {
                'token': {
                    # 'limit': 3,
                },
                'lemma': {},
                'pos': {},
                'manuscript': {},
                'section_name': {},
                'is_rubric': {},
            }
            fields = field_options.keys()

    class AnnotatedTokenFacetSearchView(FacetMixin, HaystackViewSet):
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
            ret = self.filter_queryset(
                ret.order_by('location', 'token_number'))
            return ret
