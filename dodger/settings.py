import os

import djcelery


# helpers
BASE_DIR = os.path.dirname(__file__)


# debug config
DEBUG = False

TEMPLATE_DEBUG = DEBUG


# site config
ALLOWED_HOSTS = ['*']

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Chicago'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SESSION_EXPIRE_AT_BROWSER_CLOSE = True


# static config
STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# template config
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)


# middleware config
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


# celery config
djcelery.setup_loader()

CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

CELERY_ALWAYS_EAGER = True

# app config
ROOT_URLCONF = 'dodger.urls'

WSGI_APPLICATION = 'dodger.wsgi.application'

INSTALLED_APPS = (
    # bootstrapped admin
    'django_admin_bootstrapped.bootstrap3',
    'django_admin_bootstrapped',

    # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # migrations
    'south',

    # api
    'tastypie',

    # task scheduling
    'djcelery',
    'kombu.transport.django',

    # project apps
    'dat',
    'inventory_manager',
    'warehouse',
)


from local_settings import *
