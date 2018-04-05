from freebasics.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mc2_test.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

DEBUG = True
CELERY_ALWAYS_EAGER = True


def scratchpath(*paths):
    return abspath('.scratchpath', *paths)


SCRATCHPATH = scratchpath()

MESOS_MARATHON_HOST = 'http://testserver:8080'
FREE_BASICS_CAS_SERVER_URL = 'http://testserver'
FREE_BASICS_RAVEN_DSN = 'http://test-raven-dsn'
FREE_BASICS_VOLUME_PATH = '/path/to/media/'
HUB_DOMAIN = 'test.com'
