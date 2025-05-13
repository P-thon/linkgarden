
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from pathlib import Path
import logging

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'Va[%X>C2<pSUj7Q%Zn]-yR^N]yvic,K6qGwy@+IoN,_!85^n3Plbz$Bw_Ys46R1}')
PRODUCTION = os.environ.get('PRODUCTION', False)
DEVMODE = os.environ.get('DEVMODE', False)

PATH_LIST = ['', '/', 'home', 'error', 'verification']
MODELS_NAME = ['MyUser', 'MyLinkBetweenUserAndSession', 'MyCaptcha', 'MyTraficData', 'MyNewLetter', 'MyIpBanList', 'MyIpManagement', 'MyStatisticData', 'MySessionLog', 'MyInternalError', 'MyVisitor']

if PRODUCTION:
    
    ALLOWED_HOSTS = ['linkgarden']

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': '',
            'USER': '',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': ''
        }
    }

    DEBUG = False
    
    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django_session_timeout.middleware.SessionTimeoutMiddleware',
        'listings.models.PermissionDeniedErrorHandler',
    ]

    CSRF_COOKIE_SECURE = True 
    CSRF_TRUSTED_ORIGINS = ['https://linkgarden']
    CSRF_COOKIE_DOMAIN = "linkgarden"
    CSRF_COOKIE_HTTPONLY = True

    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True

else:

    ALLOWED_HOSTS = ['127.0.0.1']
    CSRF_COOKIE_SECURE = True

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'linkgarden',
            'USER': 'root',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': 3306
        }
    }

    DEBUG = True

    SESSION_COOKIE_SECURE = True
    LOGIN_URL = 'admin-login'

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django_session_timeout.middleware.SessionTimeoutMiddleware',
        'listings.models.PermissionDeniedErrorHandler',
    ]
    
    STATIC_URL = 'static/'

INSTALLED_APPS = [
    'listings',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.utils.html',
    'django_session_timeout',
    'django.contrib.sites',
    'django.utils'
    'cryptography'
]

ROOT_URLCONF = 'linkgarden.urls'

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
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'linkgarden.wsgi.application'

AUTH_USER_MODEL = 'listings.MyUser'
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


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = "/cdn/"
MEDIA_ROOT =  os.path.join(BASE_DIR, 'cdn')

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Paris'

USE_I18N = True
USE_TZ = False

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CSRF_FAILURE_VIEW = 'listings.system_error.errorcsrf'

MINIMUM_SCORE = 50

SESSION_EXPIRE_SECONDS = 3600
SESSION_EXPIRE_AFTER_LAST_ACTIVITY  = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SESSION_DEBAN_AFTER_S = 300

VERSION = 1.0
