"""This is the URLS."""
from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin
# from django.core.urlresolvers import reverse
# from django.views.generic.base import RedirectView
from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtailcore import urls as wagtail_urls
# from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailsearch.signal_handlers import \
    register_signal_handlers as wagtailsearch_register_signal_handlers
from wagtail.wagtailsearch.urls import frontend as wagtailsearch_frontend_urls

wagtailsearch_register_signal_handlers()

admin.autodiscover()
urlpatterns = patterns('',
                       # url(r'^browse/', include(promrep_urls)),
                       # url(r'^grappelli/', include('grappelli.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url('^{path}'.format(path=settings.KILN_CONTEXT_PATH),
                           include('kiln.urls')),
                       )

try:
    if settings.DEBUG:
        import debug_toolbar
        urlpatterns += patterns('',
                                url(r'^__debug__/',
                                    include(debug_toolbar.urls)),
                                )

except ImportError:
    pass

urlpatterns += patterns('',
                        url(r'^search/', include(wagtailsearch_frontend_urls)),
                        url(r'^wagtail/', include(wagtailadmin_urls)),
                        url(r'', include(wagtail_urls)),
                        )

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    import os.path

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL + 'images/',
                          document_root=os.path.join(settings.MEDIA_ROOT,
                                                     'images'))
