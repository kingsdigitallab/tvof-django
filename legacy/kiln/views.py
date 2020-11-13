from django.views.decorators.gzip import gzip_page
from django.shortcuts import render
from text_viewer.kiln_requester import CachedRequesterKiln


@gzip_page
def process(request, kiln_url, template='kiln_page.html', page_title=''):
    '''Render a kiln html output document directly as a web page.
    template: which template to use for rendering'''
    params = {'title': page_title}

    query_string = request.META.get('QUERY_STRING')
    query_string = '?' + query_string if query_string else ''
    url = 'backend/' + kiln_url + query_string

    requester = CachedRequesterKiln()

    res = requester.request_data_content(url)

    # TODO: send email / log if not found
    status = 404
    if res:
        status = 200

    params['content'] = res

    return render(request, template, params, status=status)
