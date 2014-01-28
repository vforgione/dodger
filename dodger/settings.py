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


# secret config
SECRET_KEY = os.environ['DODGER_SECRET_KEY']


# celery config
djcelery.setup_loader()

BROKER_URL = 'amqp://%s:%s@%s:%s//' % (
    os.environ['DODGER_AMQP_USER'],
    os.environ['DODGER_AMQP_PASSWD'],
    os.environ['DODGER_AMQP_HOST'],
    os.environ['DODGER_AMQP_PORT']
)

CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'


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


# db config
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['DODGER_PSQL_NAME'],
        'USER': os.environ['DODGER_PSQL_USER'],
        'PASSWORD': os.environ['DODGER_PSQL_PASSWD'],
        'HOST': os.environ['DODGER_PSQL_HOST'],
    }
}
