"""Simple models for Wagtail."""

# from __future__ import unicode_literals

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.blocks import *  # noqa
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.contrib.wagtailroutablepage.models import (
    route, RoutablePageMixin)
from django.db import models
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel, FieldPanel,\
    TabbedInterface, ObjectList
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.urls.base import translate_url
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wagtail.wagtailadmin.edit_handlers import MultiFieldPanel
from wagtail.wagtailimages.models import Image
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.fields import WagtailImageField


def get_field_lang(obj, field_name):
    if obj is None:
        return ''

    from django.utils import translation
    ret = getattr(obj, '%s_%s' % (
        field_name, translation.get_language()
    ), None)
    if not ret:
        ret = getattr(obj, '%s' % field_name, None)

    return ret

# STREAMFIELD BLOCKS
############################################


class ImageFormatChoiceBlock(FieldBlock):
    """Doc string."""

    field = forms.ChoiceField(choices=(
        ('left', 'Left'), ('centre', 'Centre'), ('right', 'Right'),
    ))


class ImageAndCaptionBlock(StructBlock):
    """Image and caption streamfield"""
    images = ImageChooserBlock()
    caption = RichTextBlock()


class ImageAndTextBlock(StructBlock):
    """Doc string."""

    text = RichTextBlock()
    image = ImageChooserBlock()
    caption = RichTextBlock()
    alignment = ImageFormatChoiceBlock()


def get_advanced_streamfield(blank=False):
    return StreamField([
        ('heading', CharBlock(classname="")),
        ('paragraph', RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('image_caption', CharBlock(classname="richtext-caption")),
        ('image_and_caption', ImageAndCaptionBlock()),
        ('image_and_text', ImageAndTextBlock()),
    ], blank=blank)

# MUTLILINGUAL BASE PAGE
############################################


class AbstractMultilingualContentPage(Page):
    '''A multilingual abstract wagtail page.

    Language supported: English and French.

    It provides a new tab in the admin for each alternative language.
    title & content fields are duplicated for each language.
    e.g. title_fr, content_fr

    Provides language-based web path:

    /PATH (for english)
    /lang/PATH (for other languages)

    Author: GN, May 2018
    '''
    class Meta:
        abstract = True

    # TODO: generalise the title_X and content_X and language tabs
    title_fr = models.CharField(
        verbose_name='Title',
        max_length=255,
        help_text=_(
            "The page title as you'd like it to be seen by the public"
        ),
        blank=True, null=False, default=''
    )
    content_fr = get_advanced_streamfield(blank=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
    ]

    content_panels_fr = [
        FieldPanel('title_fr', classname="full title"),
        StreamFieldPanel('content_fr'),
    ]

    redirect_url = models.CharField(
        verbose_name='Redirect URL',
        max_length=255,
        help_text=_(
            'Absolute or relative URL to the web page'
            ' this page will redirect to'
        ),
        blank=True, null=False, default=''
    )

    promote_panels = Page.promote_panels + [
        MultiFieldPanel([
            FieldPanel('redirect_url'),
        ], 'Redirect'),
    ]

    # TODO: move that to a function...
    # Problem is that changes to the panels in the subclasses
    # will be ignored.
    edit_handler2 = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(content_panels_fr, heading='Content (French)'),
        ObjectList(promote_panels, heading='Promote'),
        ObjectList(
            Page.settings_panels, heading='Settings',
            classname="settings"
        ),
    ])

    def clean(self, *args, **kwargs):
        ret = super(AbstractMultilingualContentPage,
                    self).clean(*args, **kwargs)

        self.redirect_url = self.redirect_url.strip()

        return ret

    def content_lang(self):
        return get_field_lang(self, 'content')

    def title_lang(self):
        return get_field_lang(self, 'title')

    @classmethod
    def get_languages(cls, request=None):
        languages = []

        code = settings.CMS_LANGUAGES[0]['code']
        if request:
            code = request.LANGUAGE_CODE

        # if we find /fr/ in the requested path.
        # we set selected = <french>.
        selected = None
        for lang in settings.CMS_LANGUAGES:
            lang = lang.copy()

            if selected is None or lang['code'] == code:
                selected = lang

            if request:
                lang['href'] = translate_url(request.path, lang['code'])

            languages.append(lang)

        # alternative = the first non-selected language.
        # useful when dealing with only two languages.
        for lang in languages:
            lang['selected'] = (lang == selected)
            if not lang['selected']:
                alternative = lang

        ret = {
            'selected': selected,
            'all': languages,
            'alt': alternative or selected,
        }

        return ret

    def get_url_parts(self, *args, **kwargs):
        ret = super(AbstractMultilingualContentPage,
                    self).get_url_parts(*args, **kwargs)
        redirect_url = self.redirect_url
        if redirect_url:
            ret = (ret[0], ret[1], redirect_url)
        return ret


# PAGES
############################################


class HomePage(AbstractMultilingualContentPage):
    """Basic home page."""
    subpage_types = ['IndexPage', 'RichTextPage', 'BlogIndexPage']

    content = StreamField([
        ('paragraph', RichTextBlock()),
        ('image_and_caption', ImageAndCaptionBlock()),
    ])


class IndexPage(AbstractMultilingualContentPage):
    """Streamfield richtextpage."""

    subpage_types = ['IndexPage', 'RichTextPage', 'BlogIndexPage']
    content = get_advanced_streamfield()


class RichTextPage(AbstractMultilingualContentPage):
    """Streamfield richtextpage."""

    content = get_advanced_streamfield()


class BlogPost(AbstractMultilingualContentPage):
    """Blog post / News Item."""

    search_name = "Blog post"
    content = get_advanced_streamfield()

    thumbnail_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

#     def __init__(self, *args, **kwargs):
#         super(AbstractMultilingualContentPage, self).__init__(*args, **kwargs)
#         self.edit_handler.children[2] = ObjectList(
#             self.promote_panels, heading='Promote')

    promote_panels = AbstractMultilingualContentPage.promote_panels + [
        MultiFieldPanel([
            ImageChooserPanel('thumbnail_image'),
        ], 'Thumbnail'),
    ]

    @property
    def thumbnail(self):
        ''' returns self.thumbnail_image or
        the first image from streamfield
        '''

        ret = self.thumbnail_image

        if ret is None:
            image = None

            for block_data in self.content.stream_data:
                value = block_data['value']
                if isinstance(value, dict):
                    image = value.get('image', None) or value.get(
                        'images', None)
                    if image:
                        break

            if image:
                ret = Image.objects.get(id=image)

        return ret


class BlogIndexPage(RoutablePageMixin, Page):
    """Blog post index page."""

    search_name = 'Blog'

    subpage_types = ['BlogPost']

    @property
    def posts(self):
        ret = self.get_children().live().order_by(
            '-latest_revision_created_at'
        )
        return ret

    @property
    def active_months(self):
        """Return active months."""
        dates = self.posts.values('date').distinct()
        new_dates = set([date(d['date'].year, d['date'].month, 1)
                         for d in dates])

        return sorted(new_dates, reverse=True)

    def _paginate(self, request, posts):
        """Paginate posts."""
        # Pagination
        page = request.GET.get('page')
        paginator = Paginator(posts, settings.ITEMS_PER_PAGE)

        try:
            posts = paginator.page(page)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        except PageNotAnInteger:
            posts = paginator.page(1)

        return posts

    @route(r'^$')
    def serve_listing(self, request):
        """Main listing."""
        posts = self.posts

        return render(
            request,
            self.get_template(request),
            {
                'self': self,
                'page_of_posts': self._paginate(request, posts)
            }
        )

    @route(r'^author/(?P<author>[\w ]+)/$')
    def author(self, request, author=None):
        """Listing of posts by a specific author."""
        if not author:
            # Invalid author filter
            raise Http404('Invalid Author')

        posts = self.posts.filter(
            models.Q(owner__username=author) | models.Q(
                owner__username=unslugify(author)
            )
        )

        return render(request,
                      self.get_template(request),
                      {'self': self,
                       'posts': self._paginate(request, posts),
                       'filter_type': 'author',
                       'filter': author})

    @route(r'^tag/(?P<tag>[\w ]+)/$')
    def tag(self, request, tag=None):
        """Listing of posts in a specific tag."""
        if not tag:
            # Invalid tag filter
            raise Http404('Invalid Tag')

        posts = self.posts.filter(
            models.Q(tags__name=tag) | models.Q(tags__name=unslugify(tag)))

        return render(request,
                      self.get_template(request),
                      {'self': self,
                       'posts': self._paginate(request, posts),
                       'filter_type': 'tag',
                       'filter': tag})

    @route((r'^date'
            r'/(?P<year>\d{4})'
            r'/$'))
    @route((r'^date'
            r'/(?P<year>\d{4})'
            r'/(?P<month>(?:\w+|\d{1,2}))'
            r'/$'))
    @route((r'^date'
            r'/(?P<year>\d{4})'
            r'/(?P<month>(?:\w+|\d{1,2}))'
            r'/(?P<day>\d{1,2})'
            r'/$'))
    def date(self, request, year=None, month=None, day=None):
        """Listing of posts published within a specific year."""
        if not year:
            # Invalid year filter
            raise Http404('Invalid Year')

        # filter by date
        date_filter = {'date__year': int(year)}
        date_factory = [int(year)]
        date_format = 'Y'

        if month:
            # specifiec month
            m = self.get_month_number(month.title())

            if m:
                date_filter['date__month'] = m
                date_factory.append(int(m))
            else:
                date_filter['date__month'] = month
                date_factory.append(int(month))

            date_format = 'N Y'
        else:
            # no month defined
            date_factory.append(1)

        if day:
            # specific day defined
            date_filter['date__day'] = int(day)
            date_factory.append(int(day))
            date_format = 'N d, Y'
        else:
            # no day defined
            date_factory.append(1)

        try:
            posts = self.posts.filter(**date_filter)
        except ValueError:
            # Invalid date filter
            raise Http404

        return render(request,
                      self.get_template(request),
                      {'self': self,
                       'posts': self._paginate(request, posts),
                       'filter_type': 'date',
                       'filter_format': date_format,
                       'filter': date(*date_factory)})

    def get_month_number(self, month):
        """Get months."""
        names = dict((v, k) for k, v in enumerate(calendar.month_name))
        abbrs = dict((v, k) for k, v in enumerate(calendar.month_abbr))

        month_str = month.title()

        try:
            return names[month_str]
        except KeyError:
            try:
                return abbrs[month_str]
            except KeyError:
                return 0
