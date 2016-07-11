from django.conf.urls import patterns, url

urlpatterns = patterns('kiln.views',
                       url(r'^json/(?P<kiln_url>[^?]*)$', 'process_to_json',
                           {'template': 'process.html'}, name='kiln_to_json'),
                       url(r'^(?P<kiln_url>[^?]*)$', 'process',
                           {'template': 'process.html'}, name='kiln'),
                       )
