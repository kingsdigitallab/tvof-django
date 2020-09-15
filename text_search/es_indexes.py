from collections import deque, OrderedDict

from django.conf import settings
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, Search, Index, Boolean
from elasticsearch_dsl.connections import connections
from tqdm import tqdm
from elasticsearch.helpers import bulk, parallel_bulk, BulkIndexError

from text_search.utils import normalise_lemma

'''
http://localhost:9200/_cat/indices
# TODO: print -> log or sys.out
'''

# Define a default Elasticsearch client
from text_search import utils

# TODO: review all the connection calls
connections.create_connection(hosts=['localhost'])


class AnnotatedToken(Document):
    '''An ElasticSearch document for an annotated token in the text.
    The tokens and annotations come from the kwic file.'''
    # string
    token = Keyword()
    form = Keyword()
    lemma = Keyword()

    pos = Keyword()
    lemmapos = Keyword()

    speech_cat = Keyword()
    verse_cat = Keyword()

    manuscript_number = Integer()
    section_number = Keyword()
    is_rubric = Boolean()

    preceding = Text()
    following = Text()

    para_number = Integer()
    seg_number = Integer()
    # n
    token_number = Integer()

    previous_word = Keyword()
    next_word = Keyword()

    # the seq order of appearance in the text
    # for efficient sorting.
    seq_order = Integer()

    class Index:
        name = 'tokens'

    def set_derived_fields(self):
        self.form = self.token
        if self.pos == 'nom propre':
            self.form = self.form.lower()

    @classmethod
    def new_from_token_element(cls, token_element, parsing_context):
        attrib = utils.get_data_from_kwik_item(None, token_element)
        ret = cls()
        # print(attrib)
        for k, v in attrib.items():
            field = None

            if k == 'string':
                field = 'token'
                v = (v or '').strip()
            elif k == 'n':
                field = 'token_number'
            elif k == 'type':
                field = 'is_rubric'
                v = v == 'rubric_item'
            elif k == 'location':
                parts = v.split('_')
                ret.manuscript_number = int('edRoyal20D1' in v)
                ret.seg_number = parts[2] if len(parts) > 2 else 0
                field = 'para_number'
                v = int(parts[1])
            elif k == 'following':
                field = k
                ret.next_word = v.split(' ')[0]
            elif k == 'preceding':
                field = k
                ret.previous_word = v.split(' ')[-1]
            # TODO: verse_cat, speech_cat

            if field is None and hasattr(ret, k):
                field = k
            if field:
                setattr(ret, field, v)
            else:
                # print('WARNING: no field mapped to kwic attribute: {}'.format(k))
                # TODO: sp
                pass

        ret.meta.id = '{}.{:03d}'.format(attrib['location'], int(attrib['n']))

        ret.set_derived_fields()

        return [ret]


class LemmaDocument(Document):
    '''Indexing model for a lemma'''

    lemma = Keyword()
    lemma_sort = Keyword()
    # TODO?
    forms = Keyword()
    pos = Keyword()
    name_type = Keyword()

    class Index:
        name = 'lemmata'

    @classmethod
    def new_from_token_element(cls, token_element, parsing_context):
        tokenised_names = parsing_context.get('tokenised_names', None)
        if tokenised_names is None:
            tokenised_names = utils.read_tokenised_name_types()
            parsing_context['tokenised_names'] = tokenised_names

        ret = []
        lemma = normalise_lemma(token_element.attrib.get('lemma', ''))
        if lemma:
            location_full = '__'.join([
                token_element.attrib.get('location', ''),
                token_element.attrib.get('n', '')
            ])
            doc = cls(
                lemma=lemma,
                lemma_sort=lemma.split(',')[0].strip().lower(),
                pos=token_element.attrib.get('pos', 'Unspecified').strip(),
                name_type=tokenised_names.get(
                    location_full,
                    'Unspecified'
                )
            )

            # ES won't produce duplicates thanks to that id
            doc.meta.id = lemma

            ret.append(doc)

            # doc.set_derived_fields()

        return ret


class Indexer:
    '''
    Manages the search indexes.

    The index_names argument used in the methods
    is a list of index names the action should work on.
    If empty or None the action will apply to all available indexes.
    '''

    # available indexes
    indexes = OrderedDict([
        ['tokens', {
            'document_class': AnnotatedToken,
        }],
        ['lemmata', {
            'document_class': LemmaDocument,
        }]
    ])

    def list(self, index_names=None):
        '''Retrieves stats about indexes'''
        # todo: return list and move actual display to textsearch
        import time
        client = Elasticsearch()

        titles = {
            'name': 'Name',
            'size': 'Docs',
            'created': 'Created',
            'disk': 'MBytes',
        }
        print('{name:15} | {size:8} | {disk:10} | {created:15}'.format(**titles))
        print('-' * 60)
        for index_name, index_data in self._get_selected_indexes(index_names):
            info = {
                'name': index_name,
                'size': 'not found',
                'created': '',
            }
            index = Index(using=client, name=index_name)
            if index.exists():
                info['size'] = 'exists'
                get_res = index.get()
                info['created'] = int(get_res[index_name]['settings']['index']['creation_date'])/1000
                info['created'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(info['created']))
                stats = index.stats()
                info['size'] = stats['_all']['total']['docs']['count']
                info['disk'] = stats['_all']['total']['store']['size_in_bytes'] / 1024 / 1024

            print('{name:15} | {size:>8} | {disk:>10.2f} | {created:>15}'.format(**info))

    def clear(self, index_names=None):
        '''Recreate the tokens index'''
        client = Elasticsearch()

        for index_name, index_data in self._get_selected_indexes(index_names):
            index = Index(using=client, name=index_name)
            if index.exists():
                index.delete()

            # recreate index with imposed schema.
            # without this the index schema would have text instead of keywords, etc.
            index_data['document_class'].init()

            print('cleared {}'.format(index_name))

    def rebuild(self, index_names=None, cap=-1):
        '''index all the tokens from the kwic'''
        self.clear(index_names)

        # https://github.com/elastic/elasticsearch-py/blob/master/examples/bulk-ingest/bulk-ingest.py
        stats = {}

        # set this to 1 to debug the indexing.
        # it seems the parallel version will just silence errors!
        debug_bulk = 1

        for index_name, index_data in self._get_selected_indexes(index_names):
            options = {
                'client': connections.get_connection(),
                'actions': self._bulk_actions(index_name, index_data, cap),
                'chunk_size': settings.SEARCH_INDEX_CHUNK_SIZE
            }
            try:
                if debug_bulk:
                    bulk(**options)
                else:
                    deque(parallel_bulk(**options), maxlen=0)
            except BulkIndexError as e:
                print('Errors while indexing: {}'.format(e))

    def _bulk_actions(self, index_name, index_data, cap=-1):
        '''elasticsearch-dsl bulk_actions callback'''
        # https://elasticsearch-py.readthedocs.io/en/master/helpers.html
        # #bulk-helpers
        count = 0
        if cap > -1:
            total = cap
        else:
            print('Read token counts')
            total = utils.KwicParser.read_token_count()

        print('Indexing {} {}...'.format(total, index_name))

        # A working area for the callback that persists across multiple calls.
        # Used for caching, etc.
        parsing_context = {}
        def parsing_callback(token_element):
            return index_data['document_class'].new_from_token_element(token_element, parsing_context)

        with tqdm(total=total) as t:
            for document in utils.KwicParser(parsing_callback):
                if -1 < cap <= count:
                    break
                yield document.to_dict(True)
                t.update()
                count += 1

        if total != count:
            print('WARNING: {} indexed != {} expected'.format(count, total))

    def _get_selected_indexes(self, index_names=None):
        '''Returns a list of index inforamtion.
        One item per name in index_names.
        Thrown Exception if name not found.'''
        ret = [
            (name, data)
            for name, data
            in self.indexes.items()
            if (not index_names) or (name in index_names)
        ]
        if index_names and len(index_names) != len(ret):
            raise Exception(
                'Index name not found ({}). Possible names are: {}.'.format(
                    ', '.join(index_names),
                    ', '.join(self.indexes.keys())
                )
            )
        return ret
