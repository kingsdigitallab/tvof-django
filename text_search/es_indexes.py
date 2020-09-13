from collections import deque

from django.conf import settings
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, Search, Index, Boolean
from elasticsearch_dsl.connections import connections
from tqdm import tqdm
from elasticsearch.helpers import bulk, parallel_bulk, BulkIndexError

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

    class Index:
        name = 'tokens'

    def set_derived_fields(self):
        self.form = self.token
        if self.pos == 'nom propre':
            self.form = self.form.lower()

    @classmethod
    def new_from_token_element(cls, token_element):
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


class Indexer:
    '''
    Manages the search indexes.
    '''

    def clear(self):
        '''Recreate the tokens index'''
        client = Elasticsearch()
        index_tokens = Index(using=client, name='tokens')
        if index_tokens.exists():
            index_tokens.delete()

        # recreate index with imposed schema.
        # without this the index schema would have text instead of keywords, etc.
        AnnotatedToken.init()

    def rebuild(self):
        '''index all the tokens from the kwic'''
        self.clear()

        # https://github.com/elastic/elasticsearch-py/blob/master/examples/bulk-ingest/bulk-ingest.py
        stats = {}
        try:
            deque(parallel_bulk(
                connections.get_connection(),
                self._bulk_actions(),
                # stats_only=True,
                chunk_size=settings.SEARCH_INDEX_CHUNK_SIZE
            ), maxlen=0)
        except BulkIndexError as e:
            print('Errors while indexing: {}'.format(e))

    def _bulk_actions(self):
        # https://elasticsearch-py.readthedocs.io/en/master/helpers.html
        # #bulk-helpers
        count = 0
        cap = settings.SEARCH_INDEX_LIMIT
        if cap > -1:
            total = cap
        else:
            print('Read token counts')
            total = utils.KwicParser.read_token_count()

        print('Indexing {} tokens'.format(total))

        with tqdm(total=total) as t:
            for token_doc in utils.KwicParser(AnnotatedToken.new_from_token_element):
                if -1 < cap <= count:
                    break
                yield token_doc.to_dict(True)
                t.update()
                count += 1

        print('indexed {} tokens'.format(count))
