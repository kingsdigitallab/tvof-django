"""Hooks module."""
from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)
from text_search.models import SearchFacet


class BookAdmin(ModelAdmin):
    model = SearchFacet
    menu_label = 'Search facets'
    menu_icon = 'pilcrow'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('key', 'label', 'is_hidden')
    search_fields = ('key', 'label')


# Now you just need to register your customised ModelAdmin class with Wagtail
modeladmin_register(BookAdmin)
