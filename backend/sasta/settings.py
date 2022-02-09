"""
Django settings for sasta project.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add sastadev to sys path
sys.path.append(os.path.join(BASE_DIR, 'sastadev'))

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'kxreeb3bds$oibo7ex#f3bi5r+d(1x5zljo-#ms=i2%ih-!pvn'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(' ')
ALLOWED_HOSTS += ['localhost', '127.0.0.1']

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'sasta.authentication.CsrfExemptSessionAuthentication',
    ]
}

# Application definition
ALPINO_HOST = os.environ.get('ALPINO_HOST', 'localhost')
ALPINO_PORT = 7001
CORPUS2ALPINO_LOG_DIR = '.logs'


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'livereload',
    'django.contrib.staticfiles',
    'django_cron',
    'django_celery_results',
    'rest_framework',
    'rest_framework.authtoken',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_auth',
    'rest_auth.registration',
    'revproxy',
    'analysis',
    'authentication',
    'parse',
    'convert',
    'sastadev'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

# export from ../analysis/cron/__init__.py
CRON_CLASSES = [
    'analysis.cron.ExtractJob',
    'analysis.cron.ParseJob',
    'analysis.cron.ConvertJob',
]

ROOT_URLCONF = 'sasta.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sasta.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.postgresql"),
        "NAME": os.environ.get("SQL_DATABASE", "sasta"),
        "USER": os.environ.get("SQL_USER", "sasta"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "sasta"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    },
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Amsterdam'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = []
PROXY_FRONTEND = None


# Auth
SITE_ID = 1
SITE_NAME = 'SASTA'
HOST = 'localhost:5000'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Celery stuff
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'amqp://guest:guest@localhost:5672')
# CELERY_BROKER_URL = 'amqp://'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_IGNORE_RESULT = False
CELERY_TIMEZONE = TIME_ZONE

# Logs
# TODO: set log locations on deployment
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        # 'django_debug_file': {
        #     'level': 'DEBUG',
        #     'class': 'logging.FileHandler',
        #     # 'filename': os.path.join(BASE_DIR, 'logs', 'django', 'debug.log'),
        #     'filename': os.path.join(BASE_DIR, 'logs', 'django', 'debug.log'),
        # },
        # 'django_info_file': {
        #     'level': 'INFO',
        #     'class': 'logging.FileHandler',
        #     'filename': os.path.join(BASE_DIR, 'logs', 'django', 'info.log'),
        # },
        # 'django_error_file': {
        #     'level': 'ERROR',
        #     'class': 'logging.FileHandler',
        #     'filename': os.path.join(BASE_DIR, 'logs', 'django', 'error.log'),
        # },
        'django_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django.log'),
        },
        'sasta_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'sasta.log'),
            'formatter': 'standard'
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] %(levelname)s\t%(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['django_file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.server': {
            'handlers': ['django_file'],
            'level': 'INFO',
            'propagate': False
        },
        'sasta': {
            'handlers': ['sasta_file', 'console'],
            'level': 'INFO',
            'propagate': True
        }
    },
}
