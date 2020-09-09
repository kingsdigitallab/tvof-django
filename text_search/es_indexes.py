from elasticsearch_dsl import Document, Date, Integer, Keyword, Text
from elasticsearch_dsl.connections import connections

# Define a default Elasticsearch client
connections.create_connection(hosts=['localhost'])


class AnnotatedToken(Document):
    token = Keyword()
    form = Keyword()
    lemma = Keyword()
    preceding = Text()
    following = Text()

    class Meta:
        index = 'tokens'

    def save(self, ** kwargs):
        return super(AnnotatedToken, self).save(**kwargs)
