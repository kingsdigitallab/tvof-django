from django import template


register = template.Library()


@register.filter
def unicode_to_ascii(string):
    import unicodedata
    return ''.join(
        c
        for c
        in unicodedata.normalize('NFD', string)
        if unicodedata.category(c) != 'Mn'
    )
