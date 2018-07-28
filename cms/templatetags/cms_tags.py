import logging

from cms.util import unslugify
from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django.utils.text import slugify
from \
    wagtail.contrib.wagtailroutablepage.templatetags.wagtailroutablepage_tags \
    import routablepageurl

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.templatetags.wagtailcore_tags import pageurl

from ..models import BlogPost, get_field_lang
from cms.models import IndexPage

logger = logging.getLogger(__name__)

register = template.Library()


@register.inclusion_tag('cms/tags/breadcrumbs.html',
                        takes_context=True)
def breadcrumbs(context, root, current_page, extra=None):
    """Returns the pages that are part of the breadcrumb trail of the current
    page, up to the root page."""
    pages = current_page.get_ancestors(
        inclusive=True).descendant_of(root).filter(live=True)

    return {'request': context['request'], 'root': root,
            'current_page': current_page, 'pages': pages, 'extra': extra}


@register.assignment_tag(takes_context=False)
def are_comments_allowed():
    """Returns True if commenting on the site is allowed, False otherwise."""
    return getattr(settings, 'ALLOW_COMMENTS', False)


@register.assignment_tag(takes_context=False)
def get_disqus_shortname():
    """Returns the DISCUS shortname setting for comments."""
    return settings.DISQUS_SHORTNAME


@register.assignment_tag(takes_context=True)
def get_request_parameters(context, exclude=None):
    """Returns a string with all the request parameters except the exclude
    parameter."""
    params = ''
    request = context['request']

    for key, value in request.GET.items():
        if key != exclude:
            params += '&{key}={value}'.format(key=key, value=value)

    return params


@register.assignment_tag(takes_context=True)
def get_site_root(context):
    """Returns the site root Page, not the implementation-specific model used.

    :rtype: `wagtail.wagtailcore.models.Page`
    """
    return context['request'].site.root_page


@register.filter
def short_para_id(para_id):
    return int(para_id.split('_')[-1])


@register.filter
def is_current_or_ancestor(page, current_page):
    """Returns True if the given page is the current page or is an ancestor of
    the current page."""
    return current_page.is_current_or_ancestor(page)


@register.inclusion_tag('cms/tags/latest_blog_post.html',
                        takes_context=True)
def latest_blog_post(context, parent=None):
    """Returns the latest blog post that is child of the given parent. If no
    parent is given it defaults to the latest BlogPost object."""
    post = None

    if parent:
        post = parent.posts.order_by('-date').first()
    else:
        post = BlogPost.objects.filter(live=True).order_by('-date').first()

    return {'request': context['request'], 'post': post}


@register.inclusion_tag('cms/tags/featured_blog_post.html',
                        takes_context=True)
def featured_blog_post(context, parent=None):
    """Returns the latest featured blog post that is child of the
    given parent.
    If no parent is given it defaults to the latest featured BlogPost
    object."""
    post = None
    if parent:
        post = parent.posts.filter(featured=True).order_by('-date').first()
    else:
        post = BlogPost.objects.filter(featured=True).order_by('-date').first()

    return {'request': context['request'], 'post': post}


@register.inclusion_tag('cms/tags/latest_n_blog_posts.html',
                        takes_context=True)
def latest_n_blog_posts(context, nentries, parent=None):
    """Returns an array with the latest blog posts that are children of the
    given parent. The number of blog posts is specified in nentries. If
    there are not enough blog posts, it returns all the existing entries.
    If no parent is given it defaults to the latest BlogPost object."""

    posts = []
    base_model = BlogPost

    if parent:
        base_model = parent

    posts = base_model.objects.all().order_by('-date')[0:nentries]

    return {'request': context['request'], 'posts': posts}


@register.simple_tag(takes_context=True)
def page_title(context, page=None):
    return get_page_field_lang(context, 'title', page)


@register.simple_tag(takes_context=True)
def page_content(context, page=None):
    return get_page_field_lang(context, 'content', page)


def get_page_field_lang(context, field_name, page=None):
    if page is None:
        page = context.get('self', None)
    if page:
        page = page.specific
    return get_field_lang(page, field_name)


@register.inclusion_tag('cms/tags/main_menu.html', takes_context=True)
def main_menu(context, root, current_page=None):
    """Returns the main menu items, the children of the root page. Only live
    pages that have the show_in_menus setting on are returned."""
    menu_pages = root.get_children().live().in_menu()

    return {'request': context['request'], 'root': root,
            'current_page': current_page, 'menu_pages': menu_pages}


@register.filter
def get_section_page(page):
    '''Returns the highest IndexPage above <page> in the sitemap.
    None if not found.
    '''
    ret = None
    for p in page.get_ancestors(inclusive=True):
        if p.specific_class in [IndexPage]:
            ret = p
            break
    return ret


@register.simple_tag(takes_context=True)
def slugurl(context, slug):
    """Returns the URL for the page that has the given slug."""
    page = Page.objects.filter(slug=slug).first()

    if page:
        return pageurl(context, page)
    else:
        return None


@register.simple_tag(takes_context=True)
def archiveurl(context, page, *args):
    """[DEPRECATED] Returns the URL for the page that has the given slug.
        Use routablepageurl from wagtail.contrib.wagtailroutablepage
        templatetag
        instead.

        for example:
        `{% archiveurl page author %}`

        should be:
        `{% routablepageurl page 'author' author %}`
    """

    logger.warning(
        ('DEPRECATED: cms tag archiveurl is depracated. '
         'Use routablepageurl from wagtail.contrib.wagtailroutablepage '
         'templatetag instead.'))

    try:
        url_name = 'author'
        a_args = [slugify(args[0].username)]
    except AttributeError:
        try:
            url_name = 'tag'
            a_args = [slugify(args[0].name)]
        except AttributeError:
            url_name = 'date'
            a_args = args

    except IndexError:
        url_name = ''
        a_args = []

    return routablepageurl(context, page.specific, url_name, *a_args)


@register.filter(name="unslugify")
@stringfilter
def unslugify_filter(value):
    return unslugify(value)


@register.filter
def get_item(dictionary, key, default=None):
    return dictionary.get(key, default)


@register.filter
def in_path(page, request):
    return page.get_url(request) in request.path


@register.filter
def json(obj):
    import json
    from django.utils.safestring import mark_safe
    return mark_safe(json.dumps(obj, separators=(',', ':')))
