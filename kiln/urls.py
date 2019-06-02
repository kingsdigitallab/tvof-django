from django.urls import re_path

from .views import process

urlpatterns = [
    re_path(
        r'bibliography/?$', process,
        {'kiln_url': 'bibliography', 'page_title': 'Bibliography'},
        name='bibliography'
    ),
]
