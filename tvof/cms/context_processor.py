from .models import AbstractMultilingualContentPage


def cms_lang(request):
    return {
        'cms_lang': AbstractMultilingualContentPage.get_languages(request),
    }
