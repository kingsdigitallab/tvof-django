"""Simple models for Wagtail."""

# from __future__ import unicode_literals

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock


class HomePage(Page):
    """Basic home page."""

    subpage_types = ['IndexPage', 'RichTextPage', 'BlogIndexPage']


class IndexPage(Page):
    """Streamfield richtextpage."""

    subpage_types = ['IndexPage', 'RichTextPage', 'BlogIndexPage']
    content = StreamField([
        ('heading', blocks.CharBlock(classname="")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('image_caption', blocks.CharBlock(classname="richtext-caption")),
    ])

IndexPage.content_panels = [
    FieldPanel('title'),
    StreamFieldPanel('content'),
]


class RichTextPage(Page):
    """Streamfield richtextpage."""

    content = StreamField([
        ('heading', blocks.CharBlock(classname="")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('image_caption', blocks.CharBlock(classname="richtext-caption")),
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
