"""This is additional settings config for development only."""
from ScamSearcher.settings import *


INSTALLED_APPS += (
    'debug_toolbar',
)
DEBUG_TOOLBAR_PATCH_SETTINGS = False

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)
INTERNAL_IPS = [
    'localhost', '127.0.0.1'
]
