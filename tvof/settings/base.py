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
        'LOCATION': os.path.join(BASE_DIR, 'django_cache/text_patterns/'),
        'TIMEOUT': 30 * 60 * 60 * 24,
        # 'MAX_ENTRIES': 600,
    },
    'kiln': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'django_cache/kiln/'),
        'TIMEOUT': 30 * 60 * 60 * 24,
        # 'TIMEOUT': 1,
        # 'MAX_ENTRIES': 600,
    }
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

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'compressor',
    'cms',
    'rest_framework',
    'haystack',
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
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOGGING_ROOT, 'django.log'),
            'formatter': 'verbose'
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

MEDIA_URL = STATIC_URL + 'media/'
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
        'BACKEND': 'wagtail.search.backends.elasticsearch5',
        'AUTO_UPDATE': False,
        'URLS': ['http://127.0.0.1:9200'],
        'INDEX': 'tvof_wagtail',
        'TIMEOUT': 5,
    }
}
# Change as required
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE':
        # 'haystack.backends.elasticsearch2_backend.Elasticsearch2SearchEngine',
        'haystack_es.backends.Elasticsearch5SearchEngine',
        'URL': 'http://localhost:9200/',
        'INDEX_NAME': 'tvof_haystack',
    }
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
        'label': 'Francais',
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

