import xml.etree.ElementTree as ET

import requests

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.gzip import gzip_page


@gzip_page
def process_to_json(request, kiln_url, template):
    """Processes a request that needs to be sent to Kiln."""
    # Construct the URL for the request to the Kiln server.
    query_string = request.META.get('QUERY_STRING')
    query_string = '?' + query_string if query_string else ''
    kiln_base_url = settings.KILN_BASE_URL
    if kiln_base_url[-1] != '/':
        kiln_base_url = kiln_base_url + '/'
    url = kiln_base_url + kiln_url + query_string

    # Send the request to Kiln.
    r = requests.get(url)
    response = r.text.encode('utf-8')

    # Create a new XML tree from the response.
    root = ET.fromstring(response)

    # Element names that are expected in the response.
    element_names = ['title', 'metadata', 'content']

    # Parameters to be passed to the template.
    params = {}

    for element_name in element_names:
        params[element_name] = ''
        element = root.find(element_name)

        if element is not None:
            if element_name == 'metadata':
                params[element_name] = {}
                texts_el = element[0]
                params[element_name]['current'] = texts_el.get('current')
                params[element_name]['texts'] = []

                for child in texts_el:
                    params[element_name]['texts'].append(child.get('name'))
            elif len(element):
                for child in element:
                    params[element_name] += ET.tostring(child,
                                                        encoding='utf-8')
            elif element.text:
                params[element_name] = element.text

    return JsonResponse(params)


@gzip_page
def process(request, kiln_url, template):
    """Processes a request that needs to be sent to Kiln."""
    # Construct the URL for the request to the Kiln server.
    query_string = request.META.get('QUERY_STRING')
    query_string = '?' + query_string if query_string else ''
    kiln_base_url = settings.KILN_BASE_URL
    if kiln_base_url[-1] != '/':
        kiln_base_url = kiln_base_url + '/'
    url = kiln_base_url + kiln_url + query_string

    # Send the request to Kiln.
    r = requests.get(url)
    response = r.text.encode('utf-8')
    # Create a new XML tree from the response.
    root = ET.fromstring(response)

    # Element names that are expected in the response.
    element_names = ['title', 'css', 'js', 'header', 'breadcrumbs', 'content']

    # Parameters to be passed to the template.
    params = {}

    for element_name in element_names:
        params[element_name] = ''
        element = root.find(element_name)

        if element:
            if len(element):
                for child in element:
                    params[element_name] += ET.tostring(child,
                                                        encoding='utf-8')
            elif element.text:
                params[element_name] = element.text

    return render_to_response(template, params,
                              context_instance=RequestContext(request))
