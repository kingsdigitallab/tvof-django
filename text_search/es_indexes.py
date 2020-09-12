from django.conf import settings
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, Search, Index
from elasticsearch_dsl.connections import connections

# Define a default Elasticsearch client
from text_search import utils

connections.create_connection(hosts=['localhost'])


class AnnotatedToken(Document):
    string = Keyword()
    form = Keyword()
    lemma = Keyword()

    location = Keyword()
    n = Integer()

    preceding = Text()
    following = Text()

    class Index:
        name = 'tokens'

    def save(self, ** kwargs):
        return super(AnnotatedToken, self).save(**kwargs)


class Indexer:

    def clear(self):
        client = Elasticsearch()
        Index(using=client, name='tokens').delete()

    def index(self):
        token_doc_sample = AnnotatedToken()

        def callback(token_element):
            data = utils.get_data_from_kwik_item(token_doc_sample, token_element)
            data = {k: v for k, v in data.items() if hasattr(token_doc_sample, k)}

            ret = AnnotatedToken(
                **data,
            )
            ret.meta.id = utils.get_unique_id_from_token(ret)
            return [ret]

        count = 0
        for token_doc in utils.KwicParser(callback):
            if settings.SEARCH_INDEX_LIMIT != -1 and count >= settings.SEARCH_INDEX_LIMIT:
                break
            token_doc.save()
            count += 1
