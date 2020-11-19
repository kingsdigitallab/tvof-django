from .base import *  # noqa

DEBUG = True

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

DATABASES = {
    'default': {
        'ENGINE': db_engine,
        'NAME': 'tvof',
        'USER': 'tvof',
        'PASSWORD': 'tvof',
        'ADMINUSER': 'postgres',
        'HOST': 'localhost'
    },
}

# 10.0.2.2 is the default IP for the VirtualBox Host machine
INTERNAL_IPS = ['0.0.0.0', '127.0.0.1', '::1', '10.0.2.2']

SECRET_KEY = '12345'

FABRIC_USER = ''

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    # 'django_auth_ldap.backend.LDAPBackend',
)

# -----------------------------------------------------------------------------
# Django Debug Toolbar
# http://django-debug-toolbar.readthedocs.org/en/latest/
# -----------------------------------------------------------------------------

COMPRESS_ENABLED = False

SHOW_DEBUG_TOOLBAR = 0
if SHOW_DEBUG_TOOLBAR:
    try:
        import debug_toolbar  # noqa

        INSTALLED_APPS = INSTALLED_APPS + ['debug_toolbar']
        MIDDLEWARE += [
            'debug_toolbar.middleware.DebugToolbarMiddleware']
        DEBUG_TOOLBAR_PATCH_SETTINGS = True
    except ImportError:
        pass

LOGGING['loggers']['tvof'] = {}
LOGGING['loggers']['tvof']['handlers'] = ['console']
LOGGING['loggers']['tvof']['level'] = logging.DEBUG

SEARCH_INDEX_LIMIT = -1
SEARCH_INDEX_LIMIT_AUTOCOMPLETE = 100

SEARCH_FACET_LIMIT_DEFAULT = 100

# If True, show the the token number on the search result page
SEARCH_SHOW_TOKEN_NUMBER = True


