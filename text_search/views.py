# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from drf_haystack.serializers import HaystackSerializer
from drf_haystack.viewsets import HaystackViewSet
from .models import AnnotatedToken
from .search_indexes import AnnotatedTokenIndex
from rest_framework import pagination


def search_view(request):
    return render(request, 'text_search/search.html', {'poll': None})


class AnnotatedTokenSerializer(HaystackSerializer):
    class Meta:
        # The `index_classes` attribute is a list of which search indexes
        # we want to include in the search.
        index_classes = [AnnotatedTokenIndex]

        # The `fields` contains all the fields we want to include.
        # NOTE: Make sure you don't confuse these with model attributes.
        # ˓→These
        # fields belong to the search index!
        '''
            token = models.CharField(max_length=30)
    preceding = models.CharField(max_length=200)
    following = models.CharField(max_length=200)
    lemma = models.CharField(max_length=30)
    location = models.CharField(max_length=20)
    token_number = models.IntegerField(
        help_text='The sequential index of the token relative to the seg'
    )
    pos = models.CharField(max_length=30)

        '''

        fields = [
            'token', 'preceding', 'following', 'lemma', 'location',
            'token_number', 'pos'
        ]


class AnnotatedTokenSearchPagination(pagination.PageNumberPagination):
    page_size = 10


class AnnotatedTokenSearchView(HaystackViewSet):
    # `index_models` is an optional list of which models you would like to
    # ˓→include
    # in the search result. You might have several models indexed, and
    # ˓→this provides
    # a way to filter out those of no interest for this particular view.
    # (Translates to `SearchQuerySet().models(*index_models)` behind the
    # ˓→scenes.
    index_models = [AnnotatedToken]
    serializer_class = AnnotatedTokenSerializer

    pagination_class = AnnotatedTokenSearchPagination
