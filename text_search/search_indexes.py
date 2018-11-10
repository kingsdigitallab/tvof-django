from haystack import indexes
from .models import AnnotatedToken


class AnnotatedTokenIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True)  # , use_template=True
    token = indexes.CharField(model_attr='token')
    preceding = indexes.CharField(model_attr='preceding')
    following = indexes.CharField(model_attr='following')
    lemma = indexes.CharField(model_attr='lemma')
    location = indexes.CharField(model_attr='location')
    token_number = indexes.IntegerField(model_attr='token_number')
    pos = indexes.CharField(model_attr='pos')

    def get_model(self):
        return AnnotatedToken

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
