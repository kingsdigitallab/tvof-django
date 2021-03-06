# TODO: use lxml everywhere in this module
import sys
from xml.etree import ElementTree as ET
import os

from tqdm import tqdm

KWIC_XSLT_PATH = os.path.join(os.path.dirname(__file__), 'kwic_idx.xsl')
ORDER_BY_QUERY_STRING_PARAMETER_NAME = 'order'


def haystack_id(obj):
    return obj.get_unique_id()


def get_search_config(result_type):
    from django.conf import settings
    return settings.SEARCH_CONFIG[result_type]


def get_order_fields(request, result_type, es_search_class=None):
    '''returns a list of field names the result should be sorted by.'''
    order_key = request.GET.get(
        ORDER_BY_QUERY_STRING_PARAMETER_NAME, ''
    )
    orders = get_search_config(result_type)['orders']
    order = orders.get(order_key, list(orders.items())[0][1])

    ret = order['fields']

    if es_search_class:
        # solr id field -> seq_order in ES
        ret = [('seq_order' if f == 'id' else f) for f in ret]

    return ret


def get_ascii_from_unicode(s):
    import unicodedata
    return ''.join(
        c
        for c
        in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )


def normalise_form(token_element):
    ret = (token_element.text or '').strip()
    if token_element.attrib.get('pos', '') != 'nom propre':
        # capital in first letter may be due to:
        # . proper name (form should preserve it)
        # . capital at begining of sentence (we lowercase it)
        ret = ret.lower()
    else:
        # TODO: may not be right, e.g. d', and other determinants
        ret = ret.title()

    return ret

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

    Returns the path of the output XML file.

    This order will allow the grouping of consecutive "proper nouns" tokens
    into a single string (see AC-370).
    '''
    # dlog('transform kwic index')

    import gc

    from django.conf import settings
    ret = settings.KWIC_IDX_FILE_PATH
    kwic_path = settings.KWIC_OUT_FILE_PATH
    import os
    if (
        not force
        and os.path.exists(ret)
        and os.path.getmtime(kwic_path) < os.path.getmtime(ret)
        and os.path.getsize(ret) > 10
    ):
        return ret

    optimised = True

    if optimised:
        '''
        <item type="seg_item" location="edfr20125_00017_04" n="3" preceding="ainz que l' estoire faille . Matusalan vesqui" following="et ·lxxx· ans et ·vii· , si" sp="">
          <string>·c·</string>
        </item>
        '''
        # baseline: 64MB
        # strategy:
        #   1. we read file line by line and build an array of pointers
        #     for each encountered item: [location, n, file-position, length]
        #   2. sort the pointers by location
        #   3. re-read the items in the order of the pointers and add them to
        #   the output file. One item at a time.
        total_items = 0
        with open(kwic_path, 'rt') as fi:
            for line in fi:
                if '<item ' in line:
                    total_items += 1

        with tqdm(total=total_items) as tq:
            # edRoyal20D1_00001_01
            # [b'edfr20125_00868_05', 34, 91, 252]
            items = [[b'', 0, 0, 0] for i in range(total_items)]
            item_idx = 0
            pos = 0
            import re
            chunk_size = 1024
            content = b''
            end_marker = b'</item>'
            pattern = re.compile(rb'(?s)^.*?location="([^"]+)"\s+n="([^"]+)"')
            with open(kwic_path, 'rb') as fi:
                while True:
                    try:
                        end = content.index(end_marker)
                    except ValueError:
                        new_content = fi.read(chunk_size)
                        if len(new_content) == 0:
                            break
                        content += new_content
                        continue

                    start = content.index(b'<item ')
                    length = end - start + len(end_marker)
                    sortkey = pattern.findall(content)[0]
                    pos += start

                    # assign an item in our big list
                    item = items[item_idx]
                    item[0] = sortkey[0].replace(b'edRoyal20D1', b'R').replace(b'edfr20125', b'f')
                    item[1] = int(sortkey[1])
                    item[2] = pos
                    item[3] = length
                    tq.update(0.5)

                    pos += length
                    content = content[length+start:]
                    item_idx += 1

                # sort the items by location and n number
                items = sorted(items, key=lambda item: [item[0], item[1]])

                # write the output

                with open(ret, 'wb') as fo:
                    fo.write(b'<?xml version="1.0" encoding="utf-8"?>\n')
                    fo.write(b'<kwicindex>')
                    for item in items:
                        tq.update(0.5)
                        fi.seek(item[2])
                        content = fi.read(item[3])
                        fo.write(b'\n  ')
                        fo.write(content)
                    fo.write(b'\n</kwicindex>\n')

    else:
        # strategy: use a XSLT file
        # drawback: uses > 2.5GB of RAM, too expensive for our VMs
        # and risk of process being killed if exhausts all the RAM.
        import lxml.etree as ET
        xslt = ET.parse(KWIC_XSLT_PATH)
        transform = ET.XSLT(xslt)
        del xslt
        # ac-373.4: takes 2.5GB to parse and transform a 140MB xml file
        dom = ET.parse(kwic_path)
        newdom = transform(dom)
        del dom

        '''
        # ac-373.4: 140MB xml file will require 2.3GB to be transformed
        xsltproc -o o.xml text_search/kwic_idx.xsl kiln_out/received/kwic-out.xml
        '''
        newdom.write_output(ret)

    dlog('Transformed kwic index {} -> {}'.format(
        kwic_path,
        ret
    ))

    return ret


t0 = None


def dlog(s):
    '''Debug log'''
    from django.conf import settings
    if not settings.DEBUG:
        return

    from time import time
    import resource
    usage = resource.getrusage(resource.RUSAGE_SELF)

    global t0
    t1 = time()
    if not t0:
        t0 = t1
    print('[{:6.2f}s {:.2f}GB] {}'.format(
        (t1 - t0), usage[2] / 1024 / 1024, s)
    )
    t0 = t1


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

    for token_element in KwickParser(cb):
        ...

    DO NOT USE iter(p)
    '''

    def __init__(self, callback):
        self.callback = callback
        self.generator = None
        self.reset()

    def reset(self):
        self.next_mark = 0
        self.group = None

    def get_generator(self, from_mark):
        if not self.generator or self.next_mark > (from_mark or 0):
            assert(self.generator is None)
            self.generator = iter(self)
        return self.generator

    @classmethod
    def read_token_count(cls):
        '''Returns the total number of tokens in the kwic XML file'''
        ret = 0
        for i in (cls(lambda e: [0])):
            ret += 1
        return ret

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
                if elem.tag != 'kwicindex':
                    item.text = elem.text or ''
                res = self._add_token_to_group(item)
                if res is not None:
                    for r in self.callback(res):
                        self.next_mark += 1
                        yield r

    def _add_token_to_group(self, token):
        '''Group consecutive kwic items which belong to the same form
        E.g. Julius + Cesar => Julius Cesar

        returns an ET.Element
        '''
        ret = None

        if self.group is None:
            self.group = token
        else:
            group = self.group
            token_lemma = token.attrib.get('lemma', '')
            group_lemma = group.attrib.get('lemma', '')
            lemmas = group_lemma + token_lemma
            if token_lemma == group_lemma and lemmas.lower() != lemmas:
                # same lemma => add this token to the last group
                group.attrib['following'] = token.attrib.get('following', '')
                group.text = (group.text + ' ' + token.text)
            else:
                # release the last group
                ret = group
                ret.attrib['seq_order'] = self.next_mark
                self.group = token

        return ret



def read_tokenised_name_types():
    '''
    :return: returns all the 'name' instances
    found among all the tokenised XML files.

    {SEGID__N: NAME_TYPE}
    '''

    from django.conf import settings
    import re

    tags = {
        'persName': 'Person',
        'name': 'Name',
        'placeName': 'Place',
        'geogName': 'Geographical Feature',
    }

    ret = {}

    for _, path in settings.TOKENISED_FILES.items():
        with open(path, 'rt') as f:
            content = f.read()
            content = re.sub(r'\sxmlns="[^"]+"', '', content, count=1)

        root = ET.fromstring(content)
        xmlns = 'http://www.w3.org/XML/1998/namespace'

        for parent_tag in ['div', 'seg']:
            for seg in root.findall('.//{}'.format(parent_tag)):
                seg_id = seg.attrib.get('{%s}id' % xmlns, None)
                if seg_id is None:
                    continue
                if parent_tag == 'div':
                    seg = seg.find('head')
                    if seg is None:
                        # print('WARNING: no head under {}'.format(seg_id))
                        continue
                for tag in tags:
                    for name in seg.findall('.//{}'.format(tag)):
                        # we can have more than one w in a persname (e.g. choice)
                        for w in name.findall('.//w'):
                            name_type = name.attrib.get('type', tags[tag])
                            akey = '{}__{}'.format(seg_id, w.attrib.get('n', '0'))
                            ret[akey] = name_type.title()

    return ret


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


mss_sections = None
tokenised_data = None


def get_data_from_kwik_item(cls, item):
    '''
    Returns a dictionary from a kwic item (XML Element).
    The dictionary will be used to create a new AnnotatedToken.
    '''

    global mss_sections, tokenised_data

    if mss_sections is None:
        # print('  REQUEST')
        mss_sections = {}
        from text_viewer.text_viewer_tvof import TextViewerAPITvof
        tvof_viewer = TextViewerAPITvof()
        mss_sections.update(tvof_viewer.read_all_sections_data())

    if tokenised_data is None:
        tokenised_data = {}
        tokenised_data.update(read_tokenised_data())

    # Maps attributes to dictionary entries.
    ret = {
        k.lower().strip(): clean_value(v)
        for k, v
        in list(item.attrib.items())
        if cls is None or hasattr(cls, k.lower())
    }
    ret['string'] = (item.text or '').strip()

    ret['lemma'] = normalise_lemma(ret.get('lemma', ''))

    # sets section_number from location attribute and mss_sections
    if mss_sections:
        ms = 'Royal'
        if 'edfr' in ret['location']:
            ms = 'Fr20125'
        for section in mss_sections[ms]:
            if section['para'] > ret['location']:
                break
            ret['section_number'] = section['number']

    # augment the dictionary with metadata coming from tokenised XML
    if tokenised_data:
        ret['verse_cat'] = tokenised_data.get(
            ret['location'], {}
        ).get('verse_cat', 0)

        ret['speech_cat'] = tokenised_data.get(
            ret['location'] + '.' + ret['n'], {}
        ).get('speech_cat', 0)

    return ret


def get_unique_id_from_token(token):
    return '{}.{:03d}'.format(token.location, int(token.n))


def clean_value(value):
    if value is None:
        ret = ''
    elif isinstance(value, str):
        ret = value.strip()
    else:
        ret = value
    return ret

