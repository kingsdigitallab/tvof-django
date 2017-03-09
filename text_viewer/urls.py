from django.conf.urls import url

from .views import view_text_viewer, view_text_viewer_api

urlpatterns = [
    url(r'^api/(.*)$', view_text_viewer_api, name='text_viewer_api'),
    url(r'^(.*)$', view_text_viewer, name='text_viewer'),
]
