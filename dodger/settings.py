import os


# helpers
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

PROJ_DIR = os.path.dirname(__file__)


# debug config
DEBUG = True

TEMPLATE_DEBUG = DEBUG


# site config
ALLOWED_HOSTS = ['*']

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Chicago'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# static config
STATICFILES_DIRS = (
    os.path.join(PROJ_DIR, 'static'),
)

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
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
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
SECRET_KEY = 'wzgv3s2)z2(ah2%t906z8%+dto6d%z&g+gtu)y1wc*52cv=1fv'


# app config
ROOT_URLCONF = 'dodger.urls'

WSGI_APPLICATION = 'dodger.wsgi.application'

INSTALLED_APPS = (
    # bootstrap in admin
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

    # sso
    'social.apps.django_app.default',

    # project apps
    'app',
)


# db config
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJ_DIR, 'db.sqlite3'),
    }
}

FIXTURE_DIRS = [
    os.path.join(PROJ_DIR, 'fixtures'),
]


# sso config
AUTHENTICATION_BACKENDS = (
    'social.backends.open_id.OpenIdAuth',
    'social.backends.google.GoogleOpenId',
    'social.backends.google.GoogleOAuth2',
    'social.backends.google.GoogleOAuth',
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_REDIRECT_URL = '/'

SOCIAL_AUTH_GOOGLE_WHITELISTED_DOMAINS = ['doggyloot.com', ]


try:
    from production_settings import *
except ImportError:
    pass
