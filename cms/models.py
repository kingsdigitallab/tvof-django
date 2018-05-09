"""Simple models for Wagtail."""

# from __future__ import unicode_literals

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.blocks import *  # noqa
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.contrib.wagtailroutablepage.models import route

from django import forms

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

# STREAMFIELD TYPES
############################################


def get_advanced_streamfield():
    return StreamField([
        ('heading', CharBlock(classname="")),
        ('paragraph', RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('image_caption', CharBlock(classname="richtext-caption")),
        ('image_and_caption', ImageAndCaptionBlock()),
        ('image_and_text', ImageAndTextBlock()),
    ])


# PAGES
############################################


class BaseRichPage(Page):
    class Meta:
        abstract = True

    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
    ]


class HomePage(BaseRichPage):
    """Basic home page."""
    subpage_types = ['IndexPage', 'RichTextPage', 'BlogIndexPage']

    content = StreamField([
        ('paragraph', RichTextBlock()),
        ('image_and_caption', ImageAndCaptionBlock()),
    ])


class IndexPage(BaseRichPage):
    """Streamfield richtextpage."""

    subpage_types = ['IndexPage', 'RichTextPage', 'BlogIndexPage']
    content = get_advanced_streamfield()


class RichTextPage(BaseRichPage):
    """Streamfield richtextpage."""

    content = get_advanced_streamfield()


class BlogPost(BaseRichPage):
    """Blog post."""

    search_name = "Blog post"
    content = get_advanced_streamfield()


class BlogIndexPage(Page):
    """Blog post index page."""

    search_name = 'Blog'

    subpage_types = ['BlogPost']

    @property
    def posts(self):
        return BlogPost.objects.all().order_by('-latest_revision_created_at')

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
