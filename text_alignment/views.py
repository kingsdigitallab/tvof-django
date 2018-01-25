from django.shortcuts import render
from text_viewer.text_viewer_tvof import TextViewerAPITvof


def view_alignment(request, path):
    # e.g. /textviewer/
    context = {
        'test': 'TEST'
    }
    return render(request, 'text_alignment/alignment.html', context)


# TODO: convert to django rest framework?
def view_text_viewer_api(request, path):
    viewer = TextViewerAPITvof()
    viewer.process_request(request, path)
    return viewer.get_response_json()
