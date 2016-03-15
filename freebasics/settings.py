from mc2.settings import *
from os import environ

INSTALLED_APPS = ('freebasics', 'rest_framework') + INSTALLED_APPS

CELERY_IMPORTS += ('freebasics.tasks', )

ROOT_URLCONF = 'freebasics.urls'

FREE_BASICS_DOCKER_IMAGE = environ.get(
    'FREE_BASICS_DOCKER_IMAGE', 'praekeltfoundation/molo-freebasics')

FREE_BASICS_MOLO_SITE_DOMAIN = environ.get(
    'FREE_BASICS_MOLO_SITE_DOMAIN', 'molo.site')

FREE_BASICS_VOLUME_PATH = environ.get(
    'FREE_BASICS_VOLUME_PATH', '/deploy/media/')

FREE_BASICS_DOCKER_PORT = environ.get(
    'FREE_BASICS_DOCKER_PORT', 80)

FREE_BASICS_CAS_SERVER_URL = environ.get('FREE_BASICS_CAS_SERVER_URL', '')
FREE_BASICS_RAVEN_DSN = environ.get('FREE_BASICS_RAVEN_DSN', '')
