"""
Django settings for bazra_dj project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from datetime import timedelta
import os
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_a)-4oxe)#%1*@=jl$d7t0v-vp4np(sio&q$k41uhn$%ld(7!d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "192.168.1.86",
    "localhost",
    "127.0.0.1",
    "192.168.1.68",
    "192.168.1.74",
    "192.168.1.79",
    "192.168.1.81",
    "192.168.101.18"
]


# Application definition


DJANGO_APPS = [
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

NATIVE_APPS = [
    'autho',
    'permission',
    'utils',
    'vehicle_repair',
    'gis'
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'djoser',
    'django_filters',
]

INSTALLED_APPS = DJANGO_APPS + NATIVE_APPS + THIRD_PARTY_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bazra_dj.urls'
ROOT_WEBSOCKETCONF = 'bazra_dj.routing'

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

# WSGI_APPLICATION = 'bazra_dj.wsgi.application'
ASGI_APPLICATION = 'bazra_dj.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        # 'BACKEND': 'channels.layers.InMemoryChannelLayer',
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('redis', 6379)],
        },
    },
}


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'HOST': os.environ.get('POSTGRES_HOST'),
    #     'NAME': os.environ.get('POSTGRES_DB'),
    #     'USER': os.environ.get('POSTGRES_USER'),
    #     'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
    #     'PORT': os.environ.get('POSTGRES_PORT'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'db',
        # 'HOST': 'localhost',
        # 'HOST': '127.0.0.1',
        'NAME': 'bazra',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

APPEND_SLASH = True


# Bazra settings constants
OTP_TTL = 5


AUTH_USER_MODEL = 'autho.User'

AUTHENTICATION_BACKENDS = [
    'autho.authentication.CustomSimpleJWTAuthentication'
]

REST_FRAMEWORK = {

    'COERCE_DECIMAL_TO_STRING': False,
    'DEFAULT_AUTHENTICATION_CLASSES': (

        # 'rest_framework.authentication.BasicAuthentication',
        'autho.authentication.CustomSimpleJWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('BM',),
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    "TOKEN_OBTAIN_SERIALIZER": "autho.serializers.LoginSerializer",
    # "TOKEN_OBTAIN_VIEW": "permission.permissions.BazraPermission",
}

# JWT_CONF = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
#     'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
# }
