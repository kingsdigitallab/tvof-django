from django.conf.urls import url

from .views import process, process_to_json

urlpatterns = [
    url(r'^json/(?P<kiln_url>[^?]*)$', process_to_json,
        {'template': 'process.html'}, name='kiln_to_json'),
    url(r'^(?P<kiln_url>[^?]*)$', process,
        {'template': 'process.html'}, name='kiln'),
]
