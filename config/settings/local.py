"""
Local settings

- Run in Debug mode

- Use console backend for emails

- Add Django Debug Toolbar
- Add django-extensions as app
"""

from .base import *  # noqa

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=True)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['*'])
# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env('DJANGO_SECRET_KEY', default='4~l:gOw5sSuthmTiKh14hw`.N>jrh>Ix*1>5kQ.vp_>(5:Pr^g')

# Mail settings
# ------------------------------------------------------------------------------
#
# EMAIL_PORT = 1025
#
# EMAIL_HOST = 'localhost'
# EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND',
#                     default='django.core.mail.backends.console.EmailBackend')

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'  # Например, smtp.gmail.com
EMAIL_HOST_USER = 'asmnotifications@gmail.com'
EMAIL_HOST_PASSWORD = "amanatay123"


# CACHING
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

# django-debug-toolbar
# ------------------------------------------------------------------------------
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
INSTALLED_APPS += ['debug_toolbar', ]

INTERNAL_IPS = ['127.0.0.1', '10.0.2.2', ]

DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DB_DIR, 'ooba.sqlite3'),
    }
}

# django-extensions
# ------------------------------------------------------------------------------
INSTALLED_APPS += ['django_extensions', ]

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

########## CELERY
# In development, all tasks will be executed locally by blocking until the task returns
CELERY_ALWAYS_EAGER = True
########## END CELERY

# Your local stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------

DOMAIN_URL = "http://localhost:8000"
