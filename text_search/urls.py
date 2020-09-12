from . import views
from django.urls import path, include, re_path
from rest_framework import routers
from .views import (
    AnnotatedTokenFacetSearchView,
    AutocompleteSearchViewSet,
    LemmaFacetSearchView
)
from . import es_views

router = routers.DefaultRouter()
router.register(
    'tokens/search', AnnotatedTokenFacetSearchView,
    base_name='tokens-search'
)
router.register(
    'lemma/search', LemmaFacetSearchView,
    base_name='lemma-search'
)
router.register(
    'tokens/autocomplete', AutocompleteSearchViewSet,
    base_name='tokens-autocomplete'
)

urlpatterns = [
    re_path(r'^api/v1/', include(router.urls)),
    re_path(r'^api/v2/tokens/search/facets/', es_views.view_api_tokens_search_facets),
    re_path(r'^search/?$', views.search_view),
]
