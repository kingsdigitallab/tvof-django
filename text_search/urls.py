from . import views
from django.conf.urls import url, include
from rest_framework import routers
from .views import AnnotatedTokenFacetSearchView

router = routers.DefaultRouter()
router.register(
    'tokens/search', AnnotatedTokenFacetSearchView,
    base_name='tokens-search'
)

urlpatterns = [
    url(r'^api/v1/', include(router.urls)),
    url(r'^search/$', views.search_view),
]
