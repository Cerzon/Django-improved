"""
Django settings for geekshop project.

Generated by 'django-admin startproject' using Django 2.2.12.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from configparser import RawConfigParser
from ast import literal_eval

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create RawConfigParser instance and read a conf file with all that
# secret and critical settings shit
CONF_PARSER = RawConfigParser()
CONF_PARSER.read(os.path.join(BASE_DIR, 'conf', 'local.conf'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = CONF_PARSER.get('keys', 'SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = CONF_PARSER.getboolean('common', 'DEBUG', fallback=False)

ALLOWED_HOSTS = literal_eval(CONF_PARSER.get('common', 'ALLOWED_HOSTS', fallback='[]'))


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mainapp.apps.MainappConfig',
    'authapp.apps.AuthappConfig',
    'quotesapp.apps.QuotesappConfig',
    'basketapp.apps.BasketappConfig',
    'adminapp.apps.AdminappConfig',
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

ROOT_URLCONF = 'geekshop.urls'

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

                'mainapp.context_processors.site_set',
                'quotesapp.context_processors.header_quote',
                'basketapp.context_processors.user_basket',
            ],
        },
    },
]

WSGI_APPLICATION = 'geekshop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': CONF_PARSER.get('db', 'ENGINE', fallback='django.db.backends.sqlite3'),
        'NAME': CONF_PARSER.get('db', 'NAME', fallback=os.path.join(BASE_DIR, 'db.sqlite3')),
        'USER': CONF_PARSER.get('db', 'USER', fallback=''),
        'PASSWORD': CONF_PARSER.get('db', 'PASSWORD', fallback=''),
        'HOST': CONF_PARSER.get('db', 'HOST', fallback=''),
        'PORT': CONF_PARSER.get('db', 'PORT', fallback=''),
        'OPTIONS': literal_eval(CONF_PARSER.get('db', 'OPTIONS', fallback='{}')),
    }
}


AUTH_USER_MODEL = 'authapp.HoHooUser'

LOGIN_URL = '/user/login/'

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Mail stuff

ADMINS = literal_eval(CONF_PARSER.get('mail', 'ADMINS', fallback='[]'))

MANAGERS = literal_eval(CONF_PARSER.get('mail', 'MANAGERS', fallback='[]'))

# Some other stuff

FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880
FIRST_DAY_OF_WEEK = 1
SECURE_SSL_REDIRECT = False
SITE_ID = 1
