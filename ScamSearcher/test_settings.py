"""This is additional settings config for testing only."""
from ScamSearcher.settings import *  # pylint: disable=w0401,w0614


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'website_management',
    'website_analyzer',
    'administrative',
    'django_nose',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=administrative,webscraper,website_analyzer,website_management',
    '--cover-inclusive',
]
