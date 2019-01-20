"""This is the URLS."""
from django.urls import path, include
from django.conf import settings
from django.contrib import admin
from wagtail.admin import urls as wagtailadmin_urls
# from wagtail.documents import urls as wagtaildocs_urls
from wagtail.core import urls as wagtail_urls
from wagtail.search.signal_handlers import \
    register_signal_handlers as wagtailsearch_register_signal_handlers
from . import views as tvof_views
from django.conf.urls.i18n import i18n_patterns
from django.urls.conf import re_path

admin.autodiscover()
wagtailsearch_register_signal_handlers()

kiln_root = settings.KILN_CONTEXT_PATH

urlpatterns = [
    path(r'admin/', admin.site.urls),

    path(r'digger/', include('activecollab_digger.urls')),
    path(r'{path}'.format(path=kiln_root), include('kiln.urls')),

    path(r'textviewer/', include('text_viewer.urls'), name='textviewer'),
    path(r'lab/alignment/', include('text_alignment.urls'),
        name='textalignment'),
    path(r'lab/patterns/', include('text_patterns.urls'), name='patterns'),

    re_path(r'^documents/(\d+)/(.*)$',
        tvof_views.serve_wagtail_doc, name='wagtaildocs_serve'),

    path(r'', include('text_search.urls')),
]

urlpatterns += i18n_patterns(
    path(r'wagtail/', include(wagtailadmin_urls)),
    path(r'', include(wagtail_urls)),
    prefix_default_language=False
)

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    import os.path

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL + 'images/',
                          document_root=os.path.join(settings.MEDIA_ROOT,
                                                     'images'))
