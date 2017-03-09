from django.shortcuts import render
from text_viewer_tvof import TextViewerAPITvof


def view_text_viewer(request, path):
    # e.g. /textviewer/
    context = {
        'viewer_webpath': request.path_info[:-len(path)]
    }
    return render(request, 'text_viewer/page.html', context)


# TODO: convert to django rest framework?
def view_text_viewer_api(request, path):
    viewer = TextViewerAPITvof()
    viewer.process_request(request, path)
    return viewer.get_response()
