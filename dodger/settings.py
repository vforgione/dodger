import os


# helpers
BASE_DIR = os.path.dirname(__file__)


# debug config
DEBUG = True

TEMPLATE_DEBUG = DEBUG


# site config
ALLOWED_HOSTS = []

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Chicago'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# static config
STATIC_URL = '/static/'


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
SECRET_KEY = 'wzgv3s2)z2(ah2%t906z8%+dto6d%z&g+gtu)y1wc*52cv=1fv'


# app config
ROOT_URLCONF = 'dodger.urls'

WSGI_APPLICATION = 'dodger.wsgi.application'

INSTALLED_APPS = (
    # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # migrations
    'south',

    # project apps
    'dat',
    'inventory_manager',
    'warehouse',
)


# db config
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
