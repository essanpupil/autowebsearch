"""This is additional settings config for testing only."""
from ScamSearcher.settings import *  # pylint: disable=w0401,w0614


INSTALLED_APPS += (
    'django_nose',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=administrative,webscraper,website_analyzer,website_management',
    '--cover-inclusive',
]
