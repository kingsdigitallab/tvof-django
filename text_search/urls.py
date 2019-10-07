from . import views
from django.urls import path, include, re_path
from rest_framework import routers
from .views import AnnotatedTokenFacetSearchView

router = routers.DefaultRouter()
router.register(
    'tokens/search', AnnotatedTokenFacetSearchView,
    base_name='tokens-search'
)

urlpatterns = [
    re_path(r'^api/v1/', include(router.urls)),
    re_path(r'^search/?$', views.search_view),
]
