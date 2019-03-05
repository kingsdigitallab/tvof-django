import xml.etree.ElementTree as ET

import requests
import re
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.gzip import gzip_page
from django.shortcuts import render
from text_viewer.text_viewer import get_unicode_from_xml
from text_viewer.kiln_requester import CachedRequesterKiln


@gzip_page
def process(request, kiln_url, template):
    """Processes a request that needs to be sent to Kiln."""
    params = {}

    query_string = request.META.get('QUERY_STRING')
    query_string = '?' + query_string if query_string else ''
    url = 'backend/' + kiln_url + query_string

    requester = CachedRequesterKiln()

    res = requester.request(url)

    template = 'kiln_page.html'
    # TODO: send email / log if not found
    status = 404
    if res:
        status = 200
        # TODO: use ET instead of regepx
        res = re.sub(r'(?musi)^.*<data[^>]*>', r'', res)
        res = re.sub(r'(?musi)</data.*', r'', res)
    params['content'] = res

    if 'bibliography' in kiln_url.lower():
        params['title'] = 'Bibliography'

    return render(request, template, params, status=status)


@gzip_page
def __process(request, kiln_url, template):
    """Processes a request that needs to be sent to Kiln."""
    params = _send_to_kiln_and_process_response(request, kiln_url)

    # TODO: temporary hack, will find a more general way to branch processing
    # later
    if 'texts/' not in kiln_url:
        template = 'kiln_page.html'

    return render(request, template, params)


def __send_to_kiln_and_process_response(request, kiln_url):
    # Construct the URL for the request to the Kiln server.
    query_string = request.META.get('QUERY_STRING')
    query_string = '?' + query_string if query_string else ''
    kiln_base_url = settings.KILN_BASE_URL
    if kiln_base_url[-1] != '/':
        kiln_base_url = kiln_base_url + '/'
    url = kiln_base_url + 'backend/' + kiln_url + query_string

    # Send the request to Kiln.
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
        params['content'] = get_unicode_from_xml(params['content'])
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
            params['texts'][idx]['content'] = get_unicode_from_xml(
                get_processed_content(text_el.find('content'))
            )

            params['texts'][idx]['toc'] = []
            toc_els = text_el.findall('toc/item')
            for item_el in toc_els:
                params['texts'][idx]['toc'].append({
                    'name': get_unicode_from_xml(item_el.find('*')),
                    'id': item_el.get('id')
                })

            params['texts'][idx]['manuscripts'] = []
            manuscript_els = text_el.findall('manuscripts/manuscript')
            for manuscript_el in manuscript_els:
                manuscript_name = manuscript_el.get('name')

                if not is_manuscript_visible(manuscript_name):
                    continue

                version_els = manuscript_el.findall('versions/version')
                for version_el in version_els:
                    version_name = version_el.get('name')

                    current_url[idx * 2 + url_offset] = manuscript_name
                    current_url[idx * 2 + url_offset + 1] = version_name

                    url_change_to = get_url_change_to(
                        kiln_url, idx, manuscript_name, version_name)

                    params['texts'][idx]['manuscripts'].append({
                        'name': manuscript_name + ': ' + version_name,
                        'active': version_el.get('active', False),
                        'url_change_to': url_change_to,
                        'url_compare_with': '/' + '/'.join(current_url) + '/',
                    })

    return params


def __is_manuscript_visible(manuscript_name):
    return manuscript_name in ['Fr20125']


def __get_url_change_to(kiln_url, idx, manuscript_name, version_name):
    '''Produce a 'change-to' URL to switch a view to another version
        idx= 0 for first view, 1 for second view
        E.g. texts/Fr20125/semi-diplomatic/Fr20125/interpretive/, 0, MS1, V1
        => /k/texts/M1/V1/Fr20125/interpretive/
    '''
    parts = kiln_url.strip('/').split('/')
    change_idx = (idx * 2) + 1
    parts[change_idx: change_idx + 2] = [manuscript_name, version_name]
    ret = '/' + \
        settings.KILN_CONTEXT_PATH.strip('/') + '/' + '/'.join(parts) + '/'
    return ret


def __get_processed_content(xml):
    '''translate the hyperlinks to the biblio entries
    <a href="Montorsi_2016a">Montorsi (2016a)</a>
    =>
    <a href="/k/bibliography/#Montorsi_2016a">Montorsi (2016a)</a>
    '''
    ret = xml

    # translate the hyperlinks to the biblio entries
    for link in xml.findall('.//a[@href]'):
        link.attrib['href'] = r'/{}/bibliography/#{}'.format(
            settings.KILN_CONTEXT_PATH.strip('/'),
            link.attrib['href']
        )
        link.attrib['target'] = '_blank'

    # remove the notations
    for el in xml.findall('.//div[@class="tei body"]'):
        sub = el.find('div[@id="text-conventions"]')
        el.remove(sub)

    # remove the notations
    if xml.tag == 'content':
        xml.tag = 'div'
        xml.attrib['data-tei'] = 'content'

    return ret
