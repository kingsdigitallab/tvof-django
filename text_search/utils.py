# TODO: use lxml everywhere in this module
from xml.etree import ElementTree as ET


def haystack_id(obj):
    return obj.get_unique_id()


def normalise_lemma(lemma):
    # ac-368

    import re
    ret = lemma
    # porfit(i)er => porfitier
    ret = re.sub(r'(\w)\(([^\)]+)\)', r'\1\2', ret)
    # maintas (a) => maintas, a
    # rechief (de) => rechief, de
    ret = re.sub(r'^(.*) \(([^\)]+)\)', r'\1, \2', ret)

    ret = ret.strip()

    return ret


def write_kwic_index(force=False):
    '''Transforms kwic.xml obtained from Lemmings
    into an xml file where all concordances are directly under the
    root element and sorted by their order of appearance in the text.

    This order will allow grouping of consecutive "proper nouns" tokens
    into a single string (see AC-370).
    '''
    from django.conf import settings
    ret = settings.KWIC_IDX_FILE_PATH
    kwic_path = settings.KWIC_OUT_FILE_PATH
    import os
    if not force and os.path.exists(ret) and os.path.getmtime(kwic_path) < os.path.getmtime(ret):
        return ret

    import lxml.etree as ET
    dom = ET.parse(kwic_path)
    xslt = ET.parse('text_search/kwic_idx.xsl')
    transform = ET.XSLT(xslt)
    newdom = transform(dom)

    with open(settings.KWIC_IDX_FILE_PATH, 'wt') as fh:
        s = ET.tostring(newdom, pretty_print=True, encoding='unicode')
        fh.write(s)

    return ret


class KwicParser:
    '''
    A generator that iterates through the KWIC XML file.
    It yields items (token and lemma element) for each <string> element.

    A callback system allows you transform the item into other objects
    before they are yielded.

    It also exposes a cursor (self.next_mark) to help with QuerySet slices.

    This class was created to tie a Generator (parsing the XML)
    with the current position in that XML (.next_mark) so we can reuse it.
    There are no built-in mechanism with Python 3 to easily attach a variable
    to a generator and access it from inside or outside so this class
    BINDS the instance of KwicParser with its generator via get_generator()

    Usage:

    p = KwickParser(cb)
    pg = p.get_generator()
    ri = pg.next()

    for ri in pq:
      ...

    p.next_mark

    DO NOT USE iter(p)
    '''

    def __init__(self, callback):
        self.callback = callback
        self.generator = None
        self.reset()

    def reset(self):
        self.next_mark = 0
        self.group = None

    def add_token_to_group(self, token):
        '''Group consecutive kwic items which belong to the same form
        E.g. Julius + Cesar => Julius Cesar
        '''
        ret = None

        if self.group is None:
            self.group = token
        else:
            group = self.group
            token_lemma = token.attrib.get('lemma', '')
            group_lemma = group.attrib.get('lemma', '')
            lemmas = group_lemma + token_lemma
            if (token_lemma == group_lemma and lemmas.lower() != lemmas):
                # same lemma => add this token to the last group
                group.attrib['following'] = token.attrib.get('following', '')
                group.text = (group.text + ' ' + token.text)
            else:
                # release the last group
                ret = group
                self.group = token

        return ret

    def get_generator(self, from_mark):
        if not self.generator or self.next_mark > (from_mark or 0):
            assert(self.generator is None)
            self.generator = iter(self)
        return self.generator

    def __iter__(self):
        '''
        parse a kwic.xml document.
        call callback(item) for each <string>
            item is the ET Element for the parent <item>
            where item.text is the text content of the child <string> element

        callback returns a list of objects to be yielded by this function.

        next_mark is an iterator counter for next returned value
        (return 1 for first, 2 for second, etc.)
        Used by Django QuerySet API to take slices, e.g. queryset[2:5]
        '''

        self.reset()

        kwic_path = write_kwic_index()

        for event, elem in ET.iterparse(
            kwic_path, events=['start', 'end']
        ):
            if event == 'start' and elem.tag == 'item':
                item = elem
            if event == 'end' and (elem.tag in ['string', 'kwicindex']):
                item.text = elem.text or ''
                res = self.add_token_to_group(item)
                if res:
                    for r in self.callback(res):
                        self.next_mark += 1
                        yield r


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
