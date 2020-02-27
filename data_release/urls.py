from django.urls import path

from . import views

urlpatterns = [
    path(
        'data_release',
        views.DataReleaseView.as_view(),
        name='data_release'
    ),
    path(
        'data_release/<slug:site>/<slug:job>',
        views.DataReleaseJobView.as_view(),
        name='data_release_job'
    ),
]
