"""Hooks module."""
from django.conf import settings
from django.utils.html import format_html, format_html_join
from wagtail.admin.rich_text.converters.editor_html import WhitelistRule

from wagtail.core import hooks
from wagtail.core.whitelist import attribute_rule, check_url

from wagtail.images.formats import *  # noqa

# GN: jan 2021, this doesn't seem to have any effect in the Format
# Right-aligned is available even if this is commented-out.
# And the class will be 'richtext-image right'.
# TODO: to be reviewed if this is an issue.
register_image_format(Format(
    'Foundation right', 'Right-aligned',
    'richtext-image float-right', 'width-500'
))

# Whitelist tags and attributes in the web editor
# https://docs.wagtail.io/en/stable/releases/2.0.html?highlight=construct_whitelister_element_rules#construct-whitelister-element-rules-hook-is-deprecated
use_deprecated_functions = False

attribute_rules = {
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

if use_deprecated_functions:
    def whitelister_element_rules():
        """Doc string."""
        return attribute_rules

    hooks.register('construct_whitelister_element_rules',
                   whitelister_element_rules)
else:
    @hooks.register('register_rich_text_features')
    def whitelister_element_rules(features):
        for tag, rule in attribute_rules.items():
            rule_name = f'tvof_{tag}'
            features.register_converter_rule('editorhtml', rule_name, [
                WhitelistRule(tag, rule),
            ])
            features.default_features.append(rule_name)

# Support for font-awesome in the web editor
# https://docs.wagtail.io/en/latest/reference/hooks.html#editor-interface


@hooks.register('insert_editor_css')
def editor_css():
    return format_html(
        """<link href="{}{}" rel="stylesheet" type="text/css">""",
        settings.STATIC_URL,
        '/font-awesome/css/font-awesome.css'
    )

# Add a HTML source button to the Web editor

if use_deprecated_functions:
    def editor_js():
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

    hooks.register('insert_editor_js', editor_js)
else:
    # TODO: add a HTML editing button to Draftail.
    # Does that exist out of the box?
    # If not leave it.
    pass

