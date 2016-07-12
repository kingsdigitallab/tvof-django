"""Simple models for Wagtail."""

# from __future__ import unicode_literals

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.blocks import *  # noqa
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.contrib.wagtailroutablepage.models import route

from django import forms


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
        ('image_and_caption', ImageAndCaptionBlock()),
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
        ('image_and_caption', ImageAndCaptionBlock()),
        ('image_and_text', ImageAndTextBlock()),
    ])

RichTextPage.content_panels = [
    FieldPanel('title'),
    StreamFieldPanel('content'),
]


# class BlogIndexPage(Page):
#    """Blog index Page."""

#    search_name = "Blog"
#    subpage_types = ['BlogPost', ]


class BlogPost(Page):
    """Blog post."""

    search_name = "Blog post"
    content = StreamField([
        ('heading', CharBlock(classname="")),
        ('paragraph', RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('image_caption', CharBlock(classname="richtext-caption")),
        ('image_and_caption', ImageAndCaptionBlock()),
        ('image_and_text', ImageAndTextBlock()),
    ], null=True, blank=True)

BlogPost.content_panels = [
    FieldPanel('title'),
    StreamFieldPanel('content'),
]


class BlogIndexPage(Page):
    """Blog post index page."""

    search_name = 'Blog'

    subpage_types = ['BlogPost']

    @property
    def posts(self):
        """Return a list of the blog posts that are children of this page."""
        return BlogPost.objects.filter(
            live=True, path__startswith=self.path).order_by('-date')

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

        return render(request,
                      self.get_template(request),
                      {'self': self,
                       'posts': self._paginate(request, posts)})

    @route(r'^author/(?P<author>[\w ]+)/$')
    def author(self, request, author=None):
        """Listing of posts by a specific author."""
        if not author:
            # Invalid author filter
            raise Http404('Invalid Author')

        posts = self.posts.filter(
            models.Q(owner__username=author) |
            models.Q(owner__username=unslugify(author)))

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
            models.Q(tags__name=tag) |
            models.Q(tags__name=unslugify(tag)))

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
