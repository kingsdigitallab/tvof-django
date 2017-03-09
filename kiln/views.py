import xml.etree.ElementTree as ET

import requests

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.gzip import gzip_page


@gzip_page
def process_to_json(request, kiln_url, template):
    """Processes a request that needs to be sent to Kiln and returns a JSON
    response."""
    params = _send_to_kiln_and_process_response(request, kiln_url)

    return JsonResponse(params)


@gzip_page
def process(request, kiln_url, template):
    """Processes a request that needs to be sent to Kiln."""
    params = _send_to_kiln_and_process_response(request, kiln_url)

    # TODO: temporary hack, will find a more general way to branch processing
    # later
    if 'texts/' not in kiln_url:
        template = 'kiln_page.html'

    return render_to_response(template, params,
                              context_instance=RequestContext(request))


def _send_to_kiln_and_process_response(request, kiln_url):
    # Construct the URL for the request to the Kiln server.
    query_string = request.META.get('QUERY_STRING')
    query_string = '?' + query_string if query_string else ''
    kiln_base_url = settings.KILN_BASE_URL
    if kiln_base_url[-1] != '/':
        kiln_base_url = kiln_base_url + '/'
    url = kiln_base_url + 'backend/' + kiln_url + query_string

    # Send the request to Kiln.
    print url
    r = requests.get(url)

    response = r.text

    # Create a new XML tree from the response.
    root = ET.fromstring(response.encode('utf-8'))

    # Parameters to be passed to the template.
    params = {}

    if 'texts/' not in kiln_url:
        params['title'] = 'Bibliography'
        # params['content'] = root.findall('.//div[@id="bibliography"]')[0]
        if root.tag == 'data':
            root.tag = 'div'
        params['content'] = root
        params['content'] = ET.tostring(params['content'])
        return params

    text_els = root.findall('texts/text')
    number_of_texts = len(text_els)

    params['number_of_texts'] = number_of_texts
    params['number_of_columns'] = 12 / number_of_texts
    params['texts'] = []

    for idx, text_el in enumerate(text_els):
        current_url = kiln_url.split('/')
        current_url = current_url[:-1]
        current_url.insert(0, settings.KILN_CONTEXT_PATH.strip('/'))

        url_offset = 2

        if number_of_texts == 1:
            url_offset = 4
            current_url.append('manuscript to compare')
            current_url.append('version to compare')

        if len(text_el):
            params['texts'].append({})

            name = text_el.get('name')
            params['texts'][idx]['name'] = name
            params['texts'][idx]['title'] = text_el.find('title').text
            params['texts'][idx]['version'] = text_el.find('version').text
            params['texts'][idx]['content'] = ET.tostring(
                text_el.find('content'))

            params['texts'][idx]['toc'] = []
            toc_els = text_el.findall('toc/item')
            for item_el in toc_els:
                params['texts'][idx]['toc'].append({
                    'name': ET.tostring(item_el.find('*')),
                    'id': item_el.get('id')
                })

            params['texts'][idx]['manuscripts'] = []
            manuscript_els = text_el.findall('manuscripts/manuscript')
            for manuscript_el in manuscript_els:
                manuscript_name = manuscript_el.get('name')

                version_els = manuscript_el.findall('versions/version')
                for version_el in version_els:
                    version_name = version_el.get('name')

                    current_url[idx * 2 + url_offset] = manuscript_name
                    current_url[idx * 2 + url_offset + 1] = version_name

                    params['texts'][idx]['manuscripts'].append({
                        'name': manuscript_name + ': ' + version_name,
                        'active': version_el.get('active', False),
                        'url': '/' + '/'.join(current_url) + '/'
                    })

    return params
