"""
Django settings for ScamSearcher project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4ku@i8ns-(2z!ia@%gih&bab+3=6^_b=i6*5)d#oz7n9$u(8&)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
#DEBUG = False

TEMPLATE_DEBUG = True
#TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['localhost']


# Application definition

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
    'django_extensions',
    'django_filters',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ScamSearcher.urls'

WSGI_APPLICATION = 'ScamSearcher.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        #'ENGINE': 'django.db.backends.mysql',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'scam_db',
        'USER': 'scam_user',
        'PASSWORD': 'semuapenipu',
        'HOST': 'localhost',

    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Jakarta'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATICFILES_DIRS = (os.path.join(os.path.dirname(__file__), 'static').replace('\\', '/'),)
STATIC_URL = '/static/'
#STATIC_ROOT = '/home/skripsi/ScamSearcher/ScamSearcher/static/'



LOGIN_URL = 'login'

LOGIN_REDIRECT_URL = 'welcome'

LOGOUT_URL = 'logout'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':  (os.path.join(os.path.dirname(__file__), 'templates').replace('\\', '/'),),
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.request',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
