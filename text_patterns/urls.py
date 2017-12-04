from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^api/(?P<slug>\w+)/(?P<root>patterns|move_pattern|segunits)/'
        '(?P<path>.*?)/?$',
        views.patterns_api_view, name='patterns_api'),
    url(r'^api/(?P<slug>\w+)/?$',
        views.patterns_api_view, name='patterns_api_root'),
    url(r'^(?P<slug>\w+)/?$', views.pattern_set_view, name='pattern_set'),
    url(r'$', views.pattern_sets_view, name='pattern_sets'),
]
