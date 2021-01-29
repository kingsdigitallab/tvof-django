from . import views
from django.urls import path, include, re_path
from rest_framework import routers
from . import es_views

urlpatterns = [
    # re_path(r'^api/v1/', include(router.urls)),
    re_path(r'^api/v2/tokens/search/facets/', es_views.view_api_tokens_search_facets),
    re_path(r'^api/v2/lemma/search/facets/', es_views.view_api_lemma_search_facets),
    re_path(r'^api/v2/tokens/autocomplete/', es_views.view_api_tokens_autocomplete),
    re_path(r'^search/?$', views.search_view),
]
