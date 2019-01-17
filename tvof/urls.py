"""This is the URLS."""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from wagtail.wagtailadmin import urls as wagtailadmin_urls
# from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtailsearch.signal_handlers import \
    register_signal_handlers as wagtailsearch_register_signal_handlers
from wagtail.wagtailsearch.urls import frontend as wagtailsearch_frontend_urls
from text_viewer import urls as text_viewer_urls
from text_patterns import urls as text_patterns_urls
from text_alignment import urls as text_alignment_urls
from text_search import urls as text_search_urls
from . import views as tvof_views
from django.conf.urls.i18n import i18n_patterns

admin.autodiscover()
wagtailsearch_register_signal_handlers()

kiln_root = settings.KILN_CONTEXT_PATH

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^digger/', include('activecollab_digger.urls')),
    url('^{path}'.format(path=kiln_root),
        include('kiln.urls')),
]

if 0:
    try:
        if settings.DEBUG:
            import debug_toolbar
            urlpatterns += [
                url(r'^__debug__/',
                    include(debug_toolbar.urls)),
            ]

    except ImportError:
        pass

urlpatterns += [
    url(r'^textviewer/', include(text_viewer_urls), name='textviewer'),
]

urlpatterns += [
    url(r'^lab/alignment/', include(text_alignment_urls),
        name='textalignment'),
]

urlpatterns += [
    url(r'^lab/patterns/', include(text_patterns_urls), name='patterns'),
]

urlpatterns += [
    url(r'', include(text_search_urls)),
]

urlpatterns += [
    # url(r'^documents/', include(wagtaildocs_urls)),
    # TVOF
    url(r'^documents/(\d+)/(.*)$',
        tvof_views.serve_wagtail_doc, name='wagtaildocs_serve'),
]

urlpatterns += i18n_patterns(
    url(r'^search/', include(wagtailsearch_frontend_urls)),
    url(r'^wagtail/', include(wagtailadmin_urls)),
    url(r'', include(wagtail_urls)),
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
