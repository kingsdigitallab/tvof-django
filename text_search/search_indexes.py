# from haystack import indexes
from haystack_es import indexes
from .models import AnnotatedToken


class AnnotatedTokenIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    token = indexes.CharField(model_attr='token', faceted=True)
    preceding = indexes.CharField(model_attr='preceding')
    following = indexes.CharField(model_attr='following')
    lemma = indexes.CharField(model_attr='lemma', faceted=True)
    location = indexes.CharField(model_attr='location')
    token_number = indexes.IntegerField(model_attr='token_number')
    pos = indexes.CharField(model_attr='pos', faceted=True)

    # these fields are derived from .location
    manuscript = indexes.CharField(model_attr='manuscript', faceted=True)
    section_name = indexes.CharField(model_attr='section_name', faceted=True)
    is_rubric = indexes.BooleanField(model_attr='is_rubric', faceted=True)

    def get_model(self):
        return AnnotatedToken

    def index_queryset(self, using=None):
        return self._index_queryset_models(using=using)

    def _index_queryset_xml(self):
        pass

    def _index_queryset_models(self, using=None):
        return self.get_model().objects.all()
