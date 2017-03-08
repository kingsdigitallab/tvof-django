from django.shortcuts import render


def view_text_viewer(request):
    context = {}
    return render(request, 'text_viewer/page.html', context)


# TODO: convert to django rest framework?
def view_text_viewer_api(request, path):
    viewer = TextViewer()
    viewer.process_request(request, path)
    return viewer.get_response()


class TextViewer(object):

    def __init__(self):
        self.data = {}

    def process_request(self, request, path):
        self.request = request
        self.requested_path = path

    def get_response(self):
        ret = {
            'data': self.data,
            'status': 'ok',
            'message': '',
        }

        from django.http import JsonResponse
        return JsonResponse(ret)
