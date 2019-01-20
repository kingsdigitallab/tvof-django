from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
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
