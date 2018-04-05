from mc2.settings import *
from os import environ

INSTALLED_APPS = (
    'freebasics', 'rest_framework') + INSTALLED_APPS + ('overextends', )

ROOT_URLCONF = 'freebasics.urls'

MAMA_CAS_ATTRIBUTE_CALLBACKS = ('freebasics.permissions.org_permissions',)

FREE_BASICS_DOCKER_IMAGE = environ.get(
    'FREE_BASICS_DOCKER_IMAGE', 'praekeltfoundation/molo-freebasics')

FREE_BASICS_MOLO_SITE_DOMAIN = environ.get(
    'FREE_BASICS_MOLO_SITE_DOMAIN', 'molo.site')

FREE_BASICS_VOLUME_PATH = environ.get(
    'FREE_BASICS_VOLUME_PATH', '/deploy/media/')

FREE_BASICS_DOCKER_PORT = environ.get(
    'FREE_BASICS_DOCKER_PORT', 80)

FREE_BASICS_HEALTH_CHECK_PATH = environ.get(
    'FREE_BASICS_HEALTH_CHECK_PATH', '/health/')

APP_ID_PREFIX = environ.get(
    'FREE_BASICS_APP_ID_PREFIX', 'freebasics-')

FREE_BASICS_CAS_SERVER_URL = environ.get('FREE_BASICS_CAS_SERVER_URL', '')
FREE_BASICS_RAVEN_DSN = environ.get('FREE_BASICS_RAVEN_DSN', '')

UNICORE_DISTRIBUTE_API = environ.get('UNICORE_DISTRIBUTE_API', '')
FROM_EMAIL = environ.get('FROM_EMAIL', "support@moloproject.org")
CONTENT_IMPORT_SUBJECT = environ.get(
    'CONTENT_IMPORT_SUBJECT', 'Molo Content Import')
