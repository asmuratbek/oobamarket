# coding=utf-8

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
DEBUG = env.bool('DJANGO_DEBUG', default=False)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['ooba.market.kg', '176.31.28.85'])

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env('DJANGO_SECRET_KEY', default='4~l:gOw5sSuthmTiKh14hw`.N>jrh>Ix*1>5kQ.vp_>(5:Pr^g')

# Mail settings
# ------------------------------------------------------------------------------

# EMAIL_PORT = 1025
#
# EMAIL_HOST = 'localhost'
# EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND',0
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

DATABASES['default'] = env.db('DATABASE_URL')


# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

########## CELERY
# In development, all tasks will be executed locally by blocking until the task returns
CELERY_ALWAYS_EAGER = True
########## END CELERY

# Your local stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------
