"""Hooks module."""
from django.conf import settings
from django.utils.html import format_html, format_html_join

from wagtail.core import hooks
from wagtail.core.whitelist import attribute_rule, check_url

from wagtail.images.formats import *  # noqa

register_image_format(Format('Foundation right', 'Right-aligned',
                             'richtext-image float-right', 'width-500'))


def whitelister_element_rules():
    """Doc string."""
    return {
        'div': attribute_rule({'class': True}),
        'p': attribute_rule({'class': True}),
        'a': attribute_rule({'target': True, 'href': check_url,
                             'id': True, 'class': True}),
        'span': attribute_rule({'class': True, 'id': True}),
        'i': attribute_rule({'class': True}),
        'img': attribute_rule({'class': True}),
        'iframe': attribute_rule({'id': True, 'class': True, 'src': True,
                                  'style': True, 'frameborder': True,
                                  'allowfullscreen': True, 'width': True,
                                  'height': True}),
    }


hooks.register('construct_whitelister_element_rules',
               whitelister_element_rules)


def editor_css():
    """Doc string."""
    return format_html("""
                       <link href="{0}{1}" rel="stylesheet"
                       type="text/x-scss">
                       """,
                       settings.STATIC_URL,
                       'vendor/font-awesome/scss/font-awesome.scss')


hooks.register('insert_editor_css', editor_css)


def editor_js():
    """Doc string."""
    js_files = [
        'js/hallo_source_editor.js',
    ]

    js_includes = format_html_join('\n', '<script src="{0}{1}"></script>',
                                   ((settings.STATIC_URL, filename)
                                    for filename in js_files))

    return js_includes + format_html("""
        <script>
            registerHalloPlugin('editHtmlButton');
        </script>
        """)


# GN: removed, this plugin no longer exist in Wagtail 1.8.1
hooks.register('insert_editor_js', editor_js)
