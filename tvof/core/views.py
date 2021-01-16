from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from wagtail.documents.models import Document


def serve_wagtail_doc(request, document_id, document_filename):
    """
    See https://github.com/wagtail/wagtail/issues/1407
    See TVOF 131
    Replacement for ``wagtail.documents.views.serve.serve``
    Wagtail's default document view serves everything as an attachment.
    We'll bounce back to the URL and let the media server serve it.
    """
    doc = get_object_or_404(Document, id=document_id)
    print(doc.file.url)
    return HttpResponseRedirect(doc.file.url)

def view_test(request, code):
    context = {
        'self': {'title': 'Page not found (404)'}
    }
    template = 'cookie/404.html'

    if code in ['error', 'exception']:
        raise Exception('Test error')
    if code == '500':
        context['self']['title'] = 'Server error (500)'
        template = 'cookie/500.html'
    if code == '404':
        pass
    if code == '403':
        context['self']['title'] = 'Access denied (403)'
        template = 'cookie/403.html'

    return render(request, template, context)
