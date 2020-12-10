"""
Base settings to build other settings files upon.
"""
import os
from pathlib import Path
from collections import OrderedDict

import environ

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
# tvof/
APPS_DIR = ROOT_DIR / "tvof"
env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(ROOT_DIR / ".env"))


def makedir(apath):
    if not os.path.exists(apath):
        os.makedirs(apath)

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = "Europe/London"
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "en-gb"
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = [str(ROOT_DIR / "locale")]

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "config.urls"
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "config.wsgi.application"

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # "django.contrib.humanize", # Handy template tags
    "django.contrib.admin",
    "django.forms",
]
THIRD_PARTY_APPS = [
    "crispy_forms",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.contrib.settings",
    "wagtail.contrib.modeladmin",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.admin",
    "wagtail.core",
    "modelcluster",
    "taggit",
]

LOCAL_APPS = [
    # TODO: check if still needed
    # "tvof.users.apps.UsersConfig",
    "cms",
    "core",
    # this app could be simplified now and bib. view merged into core
    "kiln",
    "text_viewer",
    "text_alignment",
    "text_patterns",
    # TODO: check why this is necessary, tvof.text_search should be enough
    # "text_search.apps.TextSearchConfig",
    "text_search",
    "data_release",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIGRATIONS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
#MIGRATION_MODULES = {"sites": "tvof.contrib.sites.migrations"}

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

if 0:
    # GN: disabled this for the moment as not needed by legacy app.
    # TODO: to be reviewed
    # https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
    AUTH_USER_MODEL = "users.User"
    # https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
    LOGIN_REDIRECT_URL = "users:redirect"
    # https://docs.djangoproject.com/en/dev/ref/settings/#login-url
    LOGIN_URL = "account_login"
else:
    LOGIN_URL = '/wagtail/login/'

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation"
        ".UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    #"wagtail.core.middleware.SiteMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR / "staticfiles")
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [
    str(APPS_DIR / "static"),
    str(ROOT_DIR / "node_modules"),
]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR / "media")
MEDIA_ROOT_REL = os.path.relpath(MEDIA_ROOT, str(ROOT_DIR))
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"

makedir(MEDIA_ROOT)

MEDIA_UPLOAD_DIR = os.path.join(MEDIA_ROOT, 'upload')
makedir(MEDIA_UPLOAD_DIR)

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        "DIRS": [str(APPS_DIR / "templates")],
        "OPTIONS": {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "tvof.utils.context_processors.settings_context",
                "cms.context_processor.cms_lang",
            ],
        },
    }
]

# https://docs.djangoproject.com/en/dev/ref/settings/#form-renderer
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = "bootstrap4"

# FIXTURES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (str(APPS_DIR / "fixtures"),)

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "DENY"

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)
# https://docs.djangoproject.com/en/dev/ref/settings/#email-timeout
EMAIL_TIMEOUT = 5

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = "admin/"
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
# ADMINS = [("""King's Digital Lab""", "kdl-info@kcl.ac.uk")]
ADMINS = [("""TVOF ADMIN""", "ku.ca.lck@leon.yorffoeg"[::-1])]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {
        "level": env("LOGGING_ROOT_LEVEL", default="WARNING"),
        "handlers": ["console"]
    },
}


# django-allauth
# ------------------------------------------------------------------------------
ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_AUTHENTICATION_METHOD = "username"
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_REQUIRED = True
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_ADAPTER = "tvof.users.adapters.AccountAdapter"
# https://django-allauth.readthedocs.io/en/latest/configuration.html
SOCIALACCOUNT_ADAPTER = "tvof.users.adapters.SocialAccountAdapter"

# django-compressor
# ------------------------------------------------------------------------------
# https://django-compressor.readthedocs.io/en/latest/quickstart/#installation
INSTALLED_APPS += ["compressor"]
STATICFILES_FINDERS += ["compressor.finders.CompressorFinder"]

COMPRESS_CSS_FILTERS = [
    # CSS minimizer
    'compressor.filters.cssmin.CSSMinFilter'
]

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

# Elasticsearch
# ------------------------------------------------------------------------------
# https://github.com/django-es/django-elasticsearch-dsl
ELASTICSEARCH_DSL = {"default": {"hosts": "elasticsearch:9200"}}

# Wagtail
# ------------------------------------------------------------------------------
# https://docs.wagtail.io/en/v2.7.1/getting_started/integrating_into_django.html
WAGTAIL_SITE_NAME = "The Values of French"

# TVOF
# ------------------------------------------------------------------------------

WAGTAIL_APPEND_SLASH = False

# AUTH_LDAP_REQUIRE_GROUP = (
#     (
#         LDAPGroupQuery('cn=kdl-staff,' + LDAP_BASE_OU) |
#         LDAPGroupQuery('cn=tvof,' + LDAP_BASE_OU)
#     )
# )

PROJECT_TITLE = WAGTAIL_SITE_NAME
ITEMS_PER_PAGE = 10
WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.contrib.postgres_search.backend',
    }
}

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
    [lambda section, address: section['number'] in ['5', '5bis'],
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
    [lambda section, address: address['location_type'] == 'paragraph',
     '''{} ne contient pas ce paragraphe.'''
     ],
    # Absent sections in Roy20 : Genesis (1), Orient I (2), Alexander (9),
    # Conquest of France by Caesar (11)
    [lambda section, address: address['location_type'] == 'section',
     '''{} n’inclut pas cette section de l’Histoire ancienne.'''
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

# See kiln_requester.py
# We now request the docs from Kiln by reading them from disk.
# They are generated by tvof-kiln download_and_publish.sh command.
# All kiln paths below MUST remain relative (to instance root / ROOT_DIR).
# As we need to apply them to other instances for the data_release process.
KILN_STATIC_PATH = os.path.join(MEDIA_ROOT_REL, 'kiln_out')

# The list of MSS which will be on the public website
# Go to http://localhost:8000/lab/alignment/
# Click settings and select the desired MSS
# then copy &ms=...& from the querystring
# and paste it here
# ALIGNMENT_MSS = 'add-15268,add-19669,fr-17177,fr-20125,royal-20-d-1'\
#     .split(',')
# DEPRECATED, the list is saved as json in ALIGNMENT_FILTERS_PATH

# Filter which MSS and sections are visible
# Don't modify it here, copy and change it in your 'local.py'.
# Paths are relative to KILN_STATIC_PATH.
# TODO: change to json extension (!make sure change is applied on servers)
# TEXT_VIEWER_FILTERS_PATH = os.path.join(KILN_STATIC_PATH, 'settings/text_viewer_filters.py')
# ALIGNMENT_FILTERS_PATH = os.path.join(KILN_STATIC_PATH, 'settings/alignment_filters.py')

# kiln_out/received/kwic-out.xml
TOKENISED_FILES_BASE_PATH = KILN_STATIC_PATH
TOKENISED_FILES = {
    'fr': os.path.join(TOKENISED_FILES_BASE_PATH, 'prepared', 'fr_tokenised.xml'),
    'royal': os.path.join(TOKENISED_FILES_BASE_PATH, 'prepared', 'royal_tokenised.xml'),
}

KWIC_OUT_FILE_PATH = os.path.join(
    TOKENISED_FILES_BASE_PATH, 'received', 'kwic-out.xml')
KWIC_IDX_FILE_PATH = os.path.join(
    TOKENISED_FILES_BASE_PATH, 'prepared', 'kwic-idx.xml')


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
SEARCH_PAGE_SIZE_DEFAULT = 20
AUTOCOMPLETE_PAGE_SIZES = [10, 20, 50, 100]

'''
Used by front end and backend to sort the search results.
    [KEY, {
        'label': DISPLAY_LABEL,
        'fields': LIST_OF_HAYSTACK_FIELDS_TO_SORT_BY,
    }],
'''

'''
Search page configuration, shared by server and client code.
'''
SEARCH_CONFIG = [
    # config by result type
    ['tokens', {
        'label': 'Tokens',
        'api': '/api/v2/tokens/search/facets/?format=json',
        'phrase_title': 'Lemma or Form',
        'orders': OrderedDict([
            ['form', {
                'label': 'Form',
                'fields': ['form.insensitive', 'next_word.insensitive', 'id'],
            }],
            ['location', {
                'label': 'Location',
                'fields': ['id', 'form.insensitive'],
            }],
            ['previous', {
                'label': 'Previous word',
                'fields': ['previous_word.insensitive', 'form.insensitive', 'id'],
            }],
            ['next', {
                'label': 'Next word',
                'fields': ['next_word.insensitive', 'form.insensitive', 'id'],
            }],
        ]),
    }],
    ['names', {
        'label': 'Names',
        'api': '/api/v2/lemma/search/facets/?format=json&selected_facets=pos_exact%3Anom%20propre',
        'phrase_title': 'Name or Form',
        'orders': OrderedDict([
            ['lemma', {
                'label': 'Lemma',
                'fields': ['lemma.insensitive'],
            }],
            ['name_type', {
                'label': 'Type',
                'fields': ['name_type', 'lemma.insensitive'],
            }],
        ]),
    }],
    ['lemmata', {
        'label': 'Lemmata',
        'api': '/api/v2/lemma/search/facets/?format=json',
        'phrase_title': 'Lemma or Form',
        'orders': OrderedDict([
            ['lemma', {
                'label': 'Lemma',
                'fields': ['lemma.insensitive'],
            }],
            ['name_type', {
                'label': 'Type',
                'fields': ['name_type', 'lemma.insensitive'],
            }],
            ['pos', {
                'label': 'Part of speech',
                'fields': ['pos', 'lemma.insensitive'],
            }],
        ]),
    }]
]

SEARCH_CONFIG = OrderedDict(SEARCH_CONFIG)


HAYSTACK_IDENTIFIER_METHOD = 'text_search.utils.haystack_id'

# ./manage.py textviewer sections
SECTIONS_NAME = {
    '1': 'Genesis',
    '2': 'Orient I',
    '3': 'Thebes',
    '4': 'Greeks and Amazons',
    '5': 'Troy',
    '5bis': 'Prose 5',
    '6': 'Eneas',
    '6bis': 'Assyrian Kings',
    '7': 'Rome I',
    '8': 'Orient II',
    '9': 'Alexander',
    '10': 'Rome II',
    '11': 'Conquest of France by Caesar',
}


# maximum number of kwic entries to index
# -1: no limit
# 0: none
SEARCH_INDEX_LIMIT = -1
SEARCH_INDEX_LIMIT_AUTOCOMPLETE = -1
SEARCH_INDEX_CHUNK_SIZE = 500

SEARCH_FACET_LIMIT_DEFAULT = 1000

SEARCH_FACETS_INFO_PATH = '/about/search'

# If True, show the the token number on the search result page
SEARCH_SHOW_TOKEN_NUMBER = False

# The facets o the search page.
# Note that entries in this array can be overridden by
# instances in models.SearchFacet.
# The key should match the field name in AnnotatedTokenIndex
SEARCH_FACETS = [
    {
        'key': 'manuscript_number',
        'label': 'Manuscript',
        'use_for_count': True,
        'type': int,
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
    {
        'key': 'name_type',
        'label': 'Lemma type',
        'use_for_count': True,
    },
]

ELASTICSEARCH_FACET_OPTIONS_LIMIT = 1000

# List of settings vars exposed on client side as windows.SETTINGS_JS
# see base.html and cms_tags.py
SETTINGS_JS = [
    'SHORT_HANDS',
    'SEARCH_PAGE_SIZES',
    'SEARCH_PAGE_SIZE_DEFAULT',
    'SEARCH_PAGE_ORDERS',
    'SECTIONS_NAME',
    'SEARCH_SHOW_TOKEN_NUMBER',
    'SEARCH_CONFIG',
    'IMAGE_SERVER_URL',
]

# IMAGE_SERVER_URL = '//loris.cch.kcl.ac.uk/tvof/webroot/images/jp2/'
IMAGE_SERVER_URL = '//loris.kdl.kcl.ac.uk/tvof2/webroot/images/jp2/'

WAGTAIL_PAGE_CONTENT_TRANSFORMS = [
    'text_search.views.transform_search_facets'
]

# See data_release app
DATA_RELEASE = {
    # those folders must exist under KILN_STATIC_PATH
    'folders': ['prepared', 'received', 'settings', 'jobs'],
    'settings': {
        'text_viewer_filters': 'settings/text_viewer_filters.py',
        'alignment_filters': 'settings/alignment_filters.py',
    },
    'sites': {
        # Don't edit the first entry, it's a special one for the current site.
        'source': {
            'name': 'This website',
            'path': KILN_STATIC_PATH,
        },
        'liv': {
            'name': 'Public live site',
            'path': '/media_target/kiln_out',
        },
        # for testing locally only.
        # you'll need to create this folder:
        # ./kiln_out under path
        'lcl2': {
            'name': 'Local target instance (TEST)',
            'path': '/media_target/kiln_out',
        },
    },
    'files': OrderedDict([
        ['fr_semi_diplomatic', {
            'name': 'Fr semi-diplomatic',
            'path': 'backend-texts-fr20125-semi-diplomatic',
            'group': 'tei',
        }],
        ['fr_interpretive', {
            'name': 'Fr interpretive',
            'path': 'backend-texts-fr20125-interpretive',
            'group': 'tei',
        }],
        ['royal_semi_diplomatic', {
            'name': 'Royal semi-diplomatic',
            'path': 'backend-texts-royal-semi-diplomatic',
            'group': 'tei',
        }],
        ['royal_interpretive', {
            'name': 'Royal interpretive',
            'path': 'backend-texts-royal-interpretive',
            'group': 'tei',
        }],

        ['bibliography', {
            'name': 'Bibliography',
            'path': 'backend-bibliography',
            'group': 'tei',
        }],
        ['alignment', {
            'name': 'Alignment',
            'path': 'backend-preprocess-alists-tvofparaalignmentxml',
            'group': 'tei',
        }],

        ['kwic_out', {
            'name': 'Kwic out',
            'path': 'received/kwic-out.xml',
            'group': 'search',
        }],
        ['fr_tokenised', {
            'name': 'Fr Tokenised',
            'path': 'prepared/fr_tokenised.xml',
            'group': 'search',
        }],
        ['royal_tokenised', {
            'name': 'Royal Tokenised',
            'path': 'prepared/royal_tokenised.xml',
            'group': 'search',
        }],
    ]),
    'file_groups': OrderedDict([
        ['tei', {
            'name': 'TEI files',
            'job': 'convert',
        }],
        ['search', {
            'name': 'Search index',
            'job': 'index',
        }]
    ]),
    'jobs': OrderedDict([
        ['convert', {
            'class_name': 'JobConvert',
            'label': 'Conversion',
            # 'command': 'cd /vagrant/tmp && bash t.sh',
            'command': 'cd /vol/tvof2/webroot/stg/tvof-kiln && bash download_and_publish.sh',
            'help': 'download source TEI files from Dropbox and convert them to HTML (using Kiln)',
        }],
        ['index', {
            'class_name': 'JobIndex',
            'label': 'Indexing',
            'help': 'rebuild the concordance index for the search page',
        }],
    ]),
}

# List of available targets for data release web page.
# Each entry refers to a key in DATA_RELEASE['sites'].
# First entry is the default target.
#
# LEAVE THIS BLANK HERE - customise it in local.py on stg and your vagrant
#
DATA_RELEASE_AVAILABLE_TARGETS = []
