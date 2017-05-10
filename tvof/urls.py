"""This is the URLS."""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtailsearch.signal_handlers import \
    register_signal_handlers as wagtailsearch_register_signal_handlers
from wagtail.wagtailsearch.urls import frontend as wagtailsearch_frontend_urls
from django.views.generic import RedirectView
from text_viewer import urls as text_viewer_urls

admin.autodiscover()
wagtailsearch_register_signal_handlers()

kiln_root = settings.KILN_CONTEXT_PATH

urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url('^{path}'.format(path=kiln_root),
        include('kiln.urls')),
]

try:
    if settings.DEBUG:
        import debug_toolbar
        urlpatterns += [
            url(r'^__debug__/',
                include(debug_toolbar.urls)),
        ]

except ImportError:
    pass

# GN: redirects to texts from menu.
# we do it here because Wagtail doesn't allow menu items to link to arbitrary
# url this is a temporary setting.
# TODO: use a more general mapping in the future
urlpatterns += [
    url(r'^{}/?$'.format(wagtail_path),
        RedirectView.as_view(
            url='/{}{}'.format(
                kiln_root, kiln_path),
            permanent=False
    )
    )
    for wagtail_path, kiln_path in settings.TVOF_WEBPATH_TO_KILN.iteritems()
]

urlpatterns += [
    url(r'^textviewer/', include(text_viewer_urls)),
]

urlpatterns += [
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^search/', include(wagtailsearch_frontend_urls)),
    url(r'^wagtail/', include(wagtailadmin_urls)),
    url(r'', include(wagtail_urls)),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    import os.path

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL + 'images/',
                          document_root=os.path.join(settings.MEDIA_ROOT,
                                                     'images'))
