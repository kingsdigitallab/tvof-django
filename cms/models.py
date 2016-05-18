"""Simple models for Wagtail."""

# from __future__ import unicode_literals

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.blocks import *  # noqa
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock

from django import forms


class ImageFormatChoiceBlock(FieldBlock):
    """Doc string."""

    field = forms.ChoiceField(choices=(
        ('left', 'Left'), ('centre', 'Centre'), ('right', 'Right'),
    ))


class ImageAndTextBlock(StructBlock):
    """Doc string."""

    text = RichTextBlock()
    image = ImageChooserBlock()
    caption = RichTextBlock()
    alignment = ImageFormatChoiceBlock()


class HomePage(Page):
    """Basic home page."""

    subpage_types = ['IndexPage', 'RichTextPage', 'BlogIndexPage']


class IndexPage(Page):
    """Streamfield richtextpage."""

    subpage_types = ['IndexPage', 'RichTextPage', 'BlogIndexPage']
    content = StreamField([
        ('heading', CharBlock(classname="")),
        ('paragraph', RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('image_caption', CharBlock(classname="richtext-caption")),
        ('image_and_text', ImageAndTextBlock()),
    ])

IndexPage.content_panels = [
    FieldPanel('title'),
    StreamFieldPanel('content'),
]


class RichTextPage(Page):
    """Streamfield richtextpage."""

    content = StreamField([
        ('heading', CharBlock(classname="")),
        ('paragraph', RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('image_caption', CharBlock(classname="richtext-caption")),
        ('image_and_text', ImageAndTextBlock()),
    ])

RichTextPage.content_panels = [
    FieldPanel('title'),
    StreamFieldPanel('content'),
]


class BlogIndexPage(Page):
    """Blog index Page."""

    search_name = "Blog"
    subpage_types = ['BlogPost', ]


class BlogPost(Page):
    """Blog post."""

    search_name = "Blog post"
    content = StreamField([
        ('heading', CharBlock(classname="")),
        ('paragraph', RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('image_caption', CharBlock(classname="richtext-caption")),
        ('image_and_text', ImageAndTextBlock()),
    ])
