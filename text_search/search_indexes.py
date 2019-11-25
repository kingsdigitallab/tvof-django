from haystack import indexes
from .models import AnnotatedToken, AutocompleteForm


class AutocompleteFormIndex(indexes.SearchIndex, indexes.Indexable):
    # this is required by haystack
    # we also need to match the type of AnnotatedTokenIndex.text
    text = indexes.CharField(document=True)
    autocomplete = indexes.EdgeNgramField()
    form = indexes.CharField(model_attr='form')
    lemma = indexes.CharField(model_attr='lemma')

    def get_model(self):
        '''We must override this method'''
        return AutocompleteForm

    def prepare_text(self, token):
        # .text is necessary but unused, so we leave it blank to save space
        return ''

    def prepare_autocomplete(self, token):
        return ' '.join([v for v in [token.form, token.lemma] if v])

    def index_queryset(self, using=None):
        '''We must override this method'''
        return self._index_queryset_xml()

    def _index_queryset_xml(self):
        '''Returns the searchable models from XML files.
        Why not using DB?
        We already have the XML file created by partners for text viewer, etc.
        We have no need so far for holding that specific data in the RDB,
        only used for search.
        So instead of loading a large amount of data from XML to DB,
        then from DB to Solr, we directly load from XML to Solr.
        '''
        return self.get_model().from_kwic.all()


class AnnotatedTokenIndex(indexes.SearchIndex, indexes.Indexable):
    '''
    https://django-haystack.readthedocs.io/en/master/installing_search_engines.html

    https://django-haystack.readthedocs.io/en/master/tutorial.html#reindex

    If you’re using the Solr backend, you have an extra step.
    Solr’s configuration is XML-based,
    so you’ll need to manually regenerate the schema. You should [first] run

    # 1. generate solr config & schema files
    mkdir -p /tmp/solr && ./manage.py build_solr_schema --configure-directory=/tmp/solr

    # 2. copy to solr

    # the very first time you run this,
    # make sure managed-schema is removed from your solr conf dir

    # for local vagrant
    sudo cp /tmp/solr/* /var/solr/data/default/conf/ && sudo service solr restart

    # for STG MV
    sudo cp /tmp/solr/* /var/solr/data/stg/conf/ && sudo service solr restart
    # for LIV MV
    sudo cp /tmp/solr/* /var/solr/data/liv/conf/ && sudo service solr restart

    # 3. rebuild the index
    ./manage.py rebuild_index --noinput

    By default, all fields in Haystack are both indexed and stored
    '''

    # document=True : the primary field used for keyword searches
    # use_template=True : value created by using the following template
    #  see templates/search/indexes/text_search/annotatedtoken_text.txt
    text = indexes.CharField(document=True, use_template=True)

    # Facets
    token = indexes.CharField(model_attr='string')
    form = indexes.CharField(faceted=True)
    lemma = indexes.CharField(model_attr='lemma', faceted=True)
    pos = indexes.CharField(model_attr='pos', faceted=True)
    lemmapos = indexes.CharField(model_attr='lemmapos', faceted=True)
    # 0: non-speech, 1: speech, 2: direct, 3: indirect
    speech_cat = indexes.MultiValueField(faceted=True)
    # 0: prose, 1: verse, 2: lineated, 3: continuous
    verse_cat = indexes.MultiValueField(faceted=True)

    # these fields are derived from .location
    manuscript_number = indexes.IntegerField(faceted=True, stored=True)
    section_number = indexes.CharField(
        model_attr='section_number', faceted=True)
    is_rubric = indexes.BooleanField(faceted=True)

    # Non-faceted (stored and indexed)
    preceding = indexes.CharField(model_attr='preceding')
    following = indexes.CharField(model_attr='following')
    para_number = indexes.IntegerField()
    seg_number = indexes.IntegerField()
    token_number = indexes.IntegerField(model_attr='n')

    # Indexed only
    previous_word = indexes.CharField(stored=False)
    next_word = indexes.CharField(stored=False)

    def prepare_form(self, token):
        ret = (token.string or '').strip()
        if token.pos != 'nom propre':
            # capital in first letter may be due to:
            # . proper name (form should preserve it)
            # . capital at begining of sentence (we lowercase it)
            ret = ret.lower()
        return ret

    def prepare_speech_cat(self, token):
        ret = [0]
        if token.speech_cat:
            ret = [1, token.speech_cat]
        return ret

    def prepare_verse_cat(self, token):
        ret = [0]
        if token.verse_cat:
            ret = [1, token.verse_cat]
        return ret

    def prepare_previous_word(self, token):
        parts = token.preceding.split(' ')
        return parts[-1]

    def prepare_next_word(self, token):
        parts = token.following.split(' ')
        return parts[0]

    def prepare_para_number(self, token):
        parts = token.location.split('_')
        return int(parts[1])

    def prepare_seg_number(self, token):
        ret = 0
        parts = token.location.split('_')
        if len(parts) > 2:
            ret = int(parts[2])
        return ret

    def prepare_is_rubric(self, token):
        return token.type == 'rubric_item'

    def prepare_manuscript_number(self, token):
        '''0: Fr, 1: Royal'''
        ret = 0
        if 'edRoyal20D1' in token.location:
            ret = 1
        return ret

    def get_model(self):
        '''We must override this method'''
        return AnnotatedToken

    def index_queryset(self, using=None):
        '''We must override this method'''
        # return self._index_queryset_rdb(using=using)
        return self._index_queryset_xml()

    def _index_queryset_rdb(self, using=None):
        '''Returns the searchable models from the Relational Database'''
        return self.get_model().objects.all()

    def _index_queryset_xml(self):
        '''Returns the searchable models from XML files.
        Why not using DB?
        We already have the XML file created by partners for text viewer, etc.
        We have no need so far for holding that specific data in the RDB,
        only used for search.
        So instead of loading a large amount of data from XML to DB,
        then from DB to Solr, we directly load from XML to Solr.
        '''
        return self.get_model().from_kwic.all()
