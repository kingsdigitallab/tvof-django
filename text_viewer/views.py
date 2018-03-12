from django.shortcuts import render
from text_viewer_tvof import TextViewerAPITvof


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
    viewer.process_request(request, path)
    res = viewer.get_response()

    title = path.split('/')
    title = '{0}, {3} ({1})'.format(*title)

    context = {
        'res': res,
        'title': title,
    }
    # print(context)
    return render(request, 'text_viewer/text_print.html', context)
