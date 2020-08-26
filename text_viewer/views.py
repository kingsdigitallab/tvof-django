from django.shortcuts import render
from .text_viewer_tvof import TextViewerAPITvof
from django.urls import reverse
import re


def view_text_viewer(request, path):
    # e.g. /textviewer/
    context = {
        'viewer_webpath': request.path_info[:-len(path)]
    }
    return render(request, 'text_viewer/text_viewer.html', context)


# TODO: convert to django rest framework?
def view_text_viewer_api(request, path):
    viewer = TextViewerAPITvof()
    viewer.process_request(request, path)
    return viewer.get_response_json()


def view_text_print(request, path):
    viewer = TextViewerAPITvof()
    viewer.process_request(request, path, is_print=True)
    res = viewer.get_response()

    title = path.split('/')
    title = '{0}, {3} ({1})'.format(*title)

    link_to_full_text = None

    if 'whole' not in path:
        # add a link to the full text in print version
        path_full = re.sub(r'/[^/]+/[^/]+$', '/whole/whole', path.rstrip('/'))
        link_to_full_text = reverse('text_print', args=['']) + path_full

    context = {
        'res': res,
        'title': title,
        'link_text_viewer': reverse('text_viewer', args=['']) + '?p1=' + path,
        'link_to_full_text': link_to_full_text,
    }
    # print(context)
    return render(request, 'text_viewer/text_print.html', context)
