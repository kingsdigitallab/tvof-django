# -*- coding: utf-8 -*-
"""
Django settings for tvof project.

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/

For production settings see
https://docs.djangoproject.com/en/dev/howto/deployment/checklist/
"""

import getpass
import logging
import os

from django_auth_ldap.config import LDAPGroupQuery
from kdl_ldap.settings import *  # noqa
from collections import OrderedDict

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

PROJECT_NAME = 'tvof'
PROJECT_TITLE = 'The Values of French'

# -----------------------------------------------------------------------------
# Core Settings
# https://docs.djangoproject.com/en/dev/ref/settings/#id6
# -----------------------------------------------------------------------------

ADMINS = (
    ('Geoffroy Noel', 'geoffroy.noel@kcl.ac.uk'),
)
MANAGERS = ADMINS

ALLOWED_HOSTS = []

# https://docs.djangoproject.com/en/dev/ref/settings/#caches
# https://docs.djangoproject.com/en/dev/topics/cache/
# http://redis.io/topics/lru-cache
# http://niwibe.github.io/django-redis/
CACHE_REDIS_DATABASE = '0'

DJANGO_CACHE_ROOT = os.path.join(BASE_DIR, 'django_cache')

if not os.path.exists(DJANGO_CACHE_ROOT):
    os.makedirs(DJANGO_CACHE_ROOT)

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/' + CACHE_REDIS_DATABASE,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'IGNORE_EXCEPTIONS': True
        }
    },
    'text_patterns': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(DJANGO_CACHE_ROOT, 'text_patterns'),
        'TIMEOUT': 30 * 60 * 60 * 24,
        # 'MAX_ENTRIES': 600,
    },
    'text_alignment': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(DJANGO_CACHE_ROOT, 'text_alignment'),
        'TIMEOUT': 1 * 60 * 60,
        # 'TIMEOUT': 0,
        # 'MAX_ENTRIES': 600,
    },
}

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False

# -----------------------------------------------------------------------------
# EMAIL SETTINGS
# -----------------------------------------------------------------------------

DEFAULT_FROM_EMAIL = 'noreply@kcl.ac.uk'
EMAIL_HOST = 'smtp.cch.kcl.ac.uk'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_SUBJECT_PREFIX = '[Django {}] '.format(PROJECT_NAME)
EMAIL_USE_TLS = False
# Sender of error messages to ADMINS and MANAGERS
SERVER_EMAIL = DEFAULT_FROM_EMAIL

INSTALLED_APPS = (
    # leave this ABOVE wagtail.search to avoid command conflicts (update_index)
    'haystack',

    'wagtail.contrib.postgres_search',

    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',

    'taggit',
    'modelcluster',

    'wagtail.contrib.modeladmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'compressor',
    'cms',
    'rest_framework',
)

INSTALLED_APPS += (
    # your project apps here
    'activecollab_digger',
    'kdl_ldap',
    'kiln',
    'text_viewer',
    'text_patterns',
    'text_alignment',
    'text_search',
    'tvof',
)

INTERNAL_IPS = ['127.0.0.1']

# https://docs.djangoproject.com/en/dev/topics/i18n/
LANGUAGE_CODE = 'en'
TIME_ZONE = 'Europe/London'
USE_I18N = True
USE_L10N = False
USE_TZ = True

# https://docs.djangoproject.com/en/dev/topics/logging/
LOGGING_ROOT = os.path.join(BASE_DIR, 'logs')
LOGGING_LEVEL = logging.WARN

if not os.path.exists(LOGGING_ROOT):
    os.makedirs(LOGGING_ROOT)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(levelname)s %(asctime)s %(module)s '
                       '%(process)d %(thread)d %(message)s')
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'timed': {
            'format': '%(asctime)s %(levelname)s %(message)s'
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOGGING_ROOT, 'django.log'),
            'formatter': 'verbose'
        },
        'kwic': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOGGING_ROOT, 'kwic.log'),
            'formatter': 'timed'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'mail_admins'],
            'level': LOGGING_LEVEL,
            'propagate': True
        },
        # 'django_auth_ldap': {
        #     'handlers': ['file'],
        #     'level': LOGGING_LEVEL,
        #     'propagate': True
        # },
        'tvof': {
            'handlers': ['file'],
            'level': LOGGING_LEVEL,
            'propagate': True
        },
        'kwic': {
            'handlers': ['kwic'],
            'level': logging.INFO,
            'propagate': True
        },
        'elasticsearch': {
            'handlers': ['file'],
            'level': LOGGING_LEVEL,
            'propagate': True
        },
    }
}

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    'wagtail.core.middleware.SiteMiddleware',

    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = PROJECT_NAME + '.urls'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
                'activecollab_digger.context_processors.activecollab_digger',
                'cms.context_processor.cms_lang',
            ],
        },
    },
]

WSGI_APPLICATION = PROJECT_NAME + '.wsgi.application'

# -----------------------------------------------------------------------------
# Authentication
# https://docs.djangoproject.com/en/dev/ref/settings/#auth
# -----------------------------------------------------------------------------

if 'wagtail.core' in INSTALLED_APPS:
    LOGIN_URL = '/wagtail/login/'
else:
    LOGIN_URL = '/admin/login/'

# -----------------------------------------------------------------------------
# Sessions
# https://docs.djangoproject.com/en/dev/ref/settings/#sessions
# -----------------------------------------------------------------------------

SESSION_COOKIE_SECURE = True

# -----------------------------------------------------------------------------
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/
# https://docs.djangoproject.com/en/dev/ref/settings/#static-files
# -----------------------------------------------------------------------------

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, STATIC_URL.strip('/'))

if not os.path.exists(STATIC_ROOT):
    os.makedirs(STATIC_ROOT)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets'),
    os.path.join(BASE_DIR, 'node_modules'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_URL.strip('/'))

if not os.path.exists(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT)

# -----------------------------------------------------------------------------
# Installed Applications Settings
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Django Compressor
# http://django-compressor.readthedocs.org/en/latest/
# -----------------------------------------------------------------------------

COMPRESS_ENABLED = True

COMPRESS_CSS_FILTERS = [
    # CSS minimizer
    'compressor.filters.cssmin.CSSMinFilter'
]

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

# -----------------------------------------------------------------------------
# FABRIC
# -----------------------------------------------------------------------------

FABRIC_USER = getpass.getuser()

# -----------------------------------------------------------------------------
# GLOBALS FOR JS
# -----------------------------------------------------------------------------

# Google Analytics ID
GA_ID = ''

# -----------------------------------------------------------------------------
# Automatically generated settings
# -----------------------------------------------------------------------------

# Check which db engine to use:
db_engine = 'django.db.backends.postgresql_psycopg2'
if 'django.contrib.gis' in INSTALLED_APPS:
    db_engine = 'django.contrib.gis.db.backends.postgis'

WAGTAIL_APPEND_SLASH = False

# -----------------------------------------------------------------------------
# ACTIVE COLLAB DIGGER
# -----------------------------------------------------------------------------

AC_BASE_URL = ''
AC_API_URL = AC_BASE_URL + '/api/v1/'
AC_PROJECT_ID = 0
AC_USER = 0
AC_TOKEN = ''
AUTH_LDAP_REQUIRE_GROUP = (
    (
        LDAPGroupQuery('cn=kdl-staff,' + LDAP_BASE_OU) |
        LDAPGroupQuery('cn=tvof,' + LDAP_BASE_OU)
    )
)
WAGTAIL_SITE_NAME = PROJECT_TITLE
ITEMS_PER_PAGE = 10
WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.contrib.postgres_search.backend',
    }
}

# Change as required
# https://django-haystack.readthedocs.io/en/stable/settings.html
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://localhost:8983/solr/default',
        'TIMEOUT': 60 * 5,
        'INCLUDE_SPELLING': False,
        'BATCH_SIZE': 100,
    },
    #     'default': {
    #         'ENGINE': 'haystack_es.backends.Elasticsearch5SearchEngine',
    #         'URL': 'http://localhost:9200/',
    #         'INDEX_NAME': 'tvof_haystack',
    #     }
}

# -----------------------------------------------------------------------------
# TVOF
# -----------------------------------------------------------------------------

#
CMS_LANGUAGES = [
    {
        'code': 'en',
        'label': 'English',
        'label_en': 'English',
    },
    {
        'code': 'fr',
        'label': 'Français',
        'label_en': 'French',
    }
]

# The list of MSS which will be on the public website
# Go to http://localhost:8000/lab/alignment/
# Click settings and select the desired MSS
# then copy &ms=...& from the querystring
# and paste it here
# ALIGNEMENT_MSS = 'add-15268,add-19669,fr-17177,fr-20125,royal-20-d-1'\
#     .split(',')
ALIGNEMENT_MSS = []

# Filter which MSS and sections are visible
# Don't modify it here, copy and change it in your 'local.py'
# TEXT_VIEWER_DOC_FILTERS = {
#     'textviewer': {
#         'Fr20125': {
#             'semi-diplomatic': [],
#             'interpretive': [
#                 '6', '6bis'
#             ],
#         },
#         'Royal': {
#             'semi-diplomatic': [
#                 '6', '6bis'
#             ],
#             'interpretive': [
#                 '6', '6bis'
#             ],
#         },
#     }
# }

'''
List of pairs (path, message).
When the text viewer cannot find a chunk of text to sync with a given
path, the message is shown to the user on in the panel.

Each path is a Python regular expression pattern.
See AC-184.
'''
TV_NOT_FOUND_ERRORS = [
    # 3. Specific explanation for Troy (5) Fr20125 + Prose 5 (5bis) Roy20
    # (display in parallel viewer when consulting either Fr20 Troy(5)
    # or Roy20 P5 (5bis))
    [r'Fr20125/.*/section/5\b|Royal/.*/section/5bis\b',
     '''Les récits de la guerre de Troie dans Fr20125 et dans Royal 20 D 1 ne
    correspondent pas. Alors que Fr20125 (manuscrit de la première rédaction)
    contient une traduction de l’Historia de Troiae excidio de Dares Phrygius,
    le manuscrit Royal 20 D 1 inclut une version beaucoup plus longue,
    reproduisant
    la cinquième mise en prose du Roman de Troie de Benoît de Sainte-Maure.
    Cette version, dite Prose 5 (voir Jung (1996), pp. 505-562), mélange des
    matériaux procédant pour la plupart de la première et de la troisième mise
    en prose de l’œuvre de Benoît (Prose 1 et Prose 3), et, bien que dans une
    moindre mesure, de la version transmise par la première rédaction de
    l’Histoire ancienne (notamment, des sections Genèse et Troie). Prose 5
    contient, en outre, treize des Héroïdes d’Ovide traduites en français et
    enchâssées à l’intérieur de la narration.'''
     ],
    [r'/paragraph/',
     '''Royal 20 D 1 ne contient pas ce paragraphe.'''
     ],
    # Absent sections in Roy20 : Genesis (1), Orient I (2), Alexander (9),
    # Conquest of France by Caesar (11)
    [r'/section/',
     '''Royal 20 D 1 n’inclut pas cette section de l’Histoire ancienne.'''
     ],
]

# tells which MSS can be linked from the visualisation to the Text Editor
# Override the value in local.py
ALIGNMENT_LINKABLE_MSS = ['fr20125', 'royal20d1']

# Override the value in local.py
ALIGNMENT_SHOW_INTERNAL_NOTES = True

#
ALIGNMENT_FEATURE_LABELS = {
    'loc': 'location',
    'var': 'variation',
    'rub': 'rubric',
}

# -----------------------------------------------------------------------------
# Kiln
# https://github.com/kcl-ddh/django-kiln
# -----------------------------------------------------------------------------

KILN_CONTEXT_PATH = 'k/'
# IF you are using vagrant, this address will not work.
# you'll need to change it in your local.py (NOT HERE).
# From your VM, run the following:
# netstat -rn
# Take the first value in the Gateway column which is not 0.0.0.0
# (e.g. 10.0.2.2) and replace localhost with it.
# e.g. 'http://10.0.2.2:8180'
KILN_BASE_URL = 'http://localhost:8180'

# See kiln_requester.py
# We know request the docs from Kiln by reading them from disk
# they must be generated by tvof-kiln download_and_publish.sh command
KILN_STATIC_PATH = os.path.join(BASE_DIR, 'kiln_out')
if not os.path.exists(KILN_STATIC_PATH):
    os.makedirs(KILN_STATIC_PATH)

# labels for the codes used in TEI to describe the text "hands"
SHORT_HANDS = {
    'S':  'copiste',
    'E':  'rédacteur médiéval',
    'CE': 'rédacteur médiéval en cursive',
    'R':  'rubricateur',
    'D':  'annotateur D',
    'LH': 'annotateur catalan?',
    'LH2': 'annotateur X',
    'U':  'inconnue',
    '':   'indeterminée',
}

SEARCH_PAGE_SIZES = [10, 20, 50, 100]
AUTOCOMPLETE_PAGE_SIZES = [10, 20, 50, 100]

'''
Used by front end and backend to sort the search results.
    [KEY, {
        'label': DISPLAY_LABEL,
        'fields': LIST_OF_HAYSTACK_FIELDS_TO_SORT_BY,
    }],
'''
SEARCH_PAGE_ORDERS = OrderedDict([
    ['form', {
        'label': 'Form',
        'fields': ['form', 'next_word', 'id'],
    }],
    ['location', {
        'label': 'Location',
        'fields': ['id', 'form'],
    }],
    ['previous', {
        'label': 'Previous word',
        'fields': ['previous_word', 'form', 'id'],
    }],
    ['next', {
        'label': 'Next word',
        'fields': ['next_word', 'form', 'id'],
    }],
])

HAYSTACK_IDENTIFIER_METHOD = 'text_search.utils.haystack_id'

# ./manage.py textviewer sections
SECTIONS_NAME = {
    '1': 'Genesis',
    '10': 'Rome II',
    '11': 'Conquest of France by Caesar',
    '2': 'Orient I',
    '3': 'Thebes',
    '4': 'Greeks and Amazons',
    '5': 'Troy',
    '5bis': 'Prose 5',
    '6': 'Eneas',
    '6bis': 'Assyrian Kings',
    '7': 'Rome I',
    '8': 'Orient II',
    '9': 'Alexander'
}


# kiln_out/received/kwic-out.xml
TOKENISED_FILES_BASE_PATH = 'kiln_out/'
TOKENISED_FILES = {
    'fr': os.path.join(TOKENISED_FILES_BASE_PATH, 'prepared', 'fr_tokenised.xml'),
    'royal': os.path.join(TOKENISED_FILES_BASE_PATH, 'prepared', 'royal_tokenised.xml'),
}

KWIC_FILE_PATH = os.path.join(
    TOKENISED_FILES_BASE_PATH, 'received', 'kwic-out.xml')

# maximum number of kwic entries to index
# -1: no limit
# 0: none
SEARCH_INDEX_LIMIT = -1

SEARCH_FACET_LIMIT_DEFAULT = 1000

SEARCH_FACETS_INFO_PATH = '/about/search'

# If True, show the the token number on the search result page
SEARCH_SHOW_TOKEN_NUMBER = False

# The facets o the search page.
# Note that entries in this array can be overridden by
# instances in models.SearchFacet.
# The key shoudl match the field name in AnnotatedTokenIndex
SEARCH_FACETS = [
    {
        'key': 'manuscript_number',
        'label': 'Manuscript',
    },
    {
        'key': 'lemma',
        'label': 'Lemma',
        'limit': 10,
    },
    {
        'key': 'form',
        'label': 'Form',
        'limit': 70,
    },
    {
        'key': 'section_number',
        'label': 'Section',
    },
    {
        'key': 'pos',
        'label': 'Part of speech',
    },
    {
        'key': 'lemmapos',
        'label': 'TVOF POS',
    },
    {
        'key': 'is_rubric',
        'label': 'Text body/rubrics',
    },
    {
        'key': 'verse_cat',
        'label': 'Textual form',
    },
    {
        'key': 'speech_cat',
        'label': 'Speech',
    },
]

# List of settings vars exposed on client side as windows.SETTINGS_JS
# see base.html and cms_tags.py
SETTINGS_JS = [
    'SHORT_HANDS',
    'SEARCH_PAGE_SIZES',
    'SEARCH_PAGE_ORDERS',
    'SECTIONS_NAME',
    'SEARCH_SHOW_TOKEN_NUMBER',
]

WAGTAIL_PAGE_CONTENT_TRANSFORMS = [
    'text_search.views.transform_search_facets'
]
