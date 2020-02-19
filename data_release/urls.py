from django.urls import path

from . import views

urlpatterns = [
    path(
        'data_release',
        views.DataReleaseView.as_view(),
        name='data_release'
    ),
]
