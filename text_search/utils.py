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


def read_tokenised_data():
    '''
    Read XML file of tokenised texts (Fr & Royal).
    Return a dictionary with information about all the
        <said> elements
        <seg type="6"> verses elements

    That dictionary key is the location of the element and the value
    is a categorisation of the element.

    The output is meant to be combined with a kwic file to build the
    search index.

    <seg type="6" xml:id="edfr20125_00910_07"><lg type="octo_coup">
        <lg type="lineated">
            <l n="001">
                <w n="1">Q[ua]r</w> <w n="2">ele</w> <w n="3">fu</w>
                <w n="4">si</w> <w n="5">bien</w>
                <w n="6">plantee<pc rend="1" /></w>
            </l>
    '''
    from django.conf import settings
    import re

    lg_types = {'lineated': 2, 'cont': 3, 'unspecified': 4}
    sc_types = {'true': 2, 'false': 3, 'unspecified': 4}

    ret = {}

    for _, path in settings.TOKENISED_FILES.items():
        with open(path, 'rt') as f:
            content = f.read()
            content = re.sub(r'\sxmlns="[^"]+"', '', content, count=1)

        root = ET.fromstring(content)
        xmlns = 'http://www.w3.org/XML/1998/namespace'

        # lt = language_type/verse_cat
        for seg in root.findall('.//seg[@type="6"]'):
            seg_id = seg.attrib.get('{%s}id' % xmlns)
            ret[seg_id] = {'verse_cat': 4}
            for lg in seg.findall('.//lg'):
                ret[seg_id]['verse_cat'] = lg_types.get(
                    lg.attrib.get('type'), 4)

        # sc = speech_cat
        for seg in root.findall('.//seg'):
            seg_id = seg.attrib.get('{%s}id' % xmlns)
            for said in seg.findall('.//said'):
                said_type = said.attrib.get(
                    'direct', 'unspecified'
                ).strip().lower()
                for word in said.findall('.//w'):
                    seg_id_n = seg_id + '.' + word.attrib.get('n')
                    if seg_id_n not in ret:
                        # we ignore nested <said>
                        ret[seg_id_n] = {
                            'speech_cat': sc_types.get(said_type, 4)
                        }
                    else:
                        # print('Nested {}'.format(seg_id_n))
                        pass

    return ret
