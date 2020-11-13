from django.conf.urls import url

from .views import view_alignment

urlpatterns = [
    url(r'^(.*)$', view_alignment, name='view_alignment'),
]
