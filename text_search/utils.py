from xml.etree import ElementTree as ET


def haystack_id(obj):
    return obj.get_unique_id()


def parse_kwic(kwic_path, callback):
    '''
    parse a kwic.xml document.
    call callback(item) for each <item>
        item is the ET Element for the <item>
    call callback(item, elem) for each <string>
        elem is the ET Element for the <string>

    callback can return None or an object.
    If an object is returned this function yields it.

    next_mark is an iterator counter for next returned value
    (return 1 for first, 2 for second, etc.)
    Used by Django QuerySet API to take slices, etc.
    '''
    next_mark = 0
    for event, elem in ET.iterparse(
        kwic_path, events=['start', 'end']
    ):
        res = None
        if event == 'start' and elem.tag == 'item':
            item = elem
            res = callback(item, None)
        if event == 'end' and elem.tag == 'string':
            res = callback(item, elem)
        if res is not None:
            next_mark += 1
            yield next_mark, res
