from django import template
from text_viewer.text_viewer_tvof import DOCUMENT_IDS

register = template.Library()


@register.filter
def format_seg_reference(segid):
    '''returns 'Fr20125 §590'
    if segid = 'fr20125_00590'
    '''

    ret = segid

    parts = ret.split('_')
    if len(parts) > 1:
        ret = '{} §{}'.format(
            DOCUMENT_IDS.get(parts[0].lower(), {'label': parts[0]})['label'],
            parts[1].lstrip('0')
        )

    return ret
