from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from wagtail.documents.models import Document
import re


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


def transform_absolute_self_links(content):
    '''
    CMS Editors have inserted absolute links to the live site.
    These need to be turned into relative links in the REF2021 clone.
    Otherwise the reviewers might land on the live site without noticing.

    <a href="https://tvof.ac.uk/textviewer/?p1=fr20125/interpretive/section/3">
        <b>thebes</b>
    </a>

    =>

    <a href="/textviewer/?p1=fr20125/interpretive/section/3">
        <b>thebes</b>
    </a>
    '''

    content = re.sub(
        r'"\s*https?://(www\.)?tvof\.ac\.uk/',
        r'"/',
        content
    )

    return content
