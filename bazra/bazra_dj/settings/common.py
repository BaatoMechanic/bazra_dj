"""
Django settings for bazra_dj project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
import logging.config
from datetime import timedelta
from pathlib import Path

import sentry_sdk
from django.utils.text import gettext_lazy as _
from dotenv import load_dotenv, find_dotenv
from firebase_admin import initialize_app

load_dotenv(find_dotenv())

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# SECRET_KEY = "django-insecure-_a)-4oxe)#%1*@=jl$d7t0v-vp4np(sio&q$k41uhn$%ld(7!d"
SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = os.environ.get("DEBUG") == "true"
STAGING = os.environ.get("STAGING") == "true"
ALLOWED_HOST = os.environ.get("ALLOWED_HOST")
ALLOWED_HOSTS = []
if ALLOWED_HOST:
    ALLOWED_HOSTS.append(ALLOWED_HOST)


DJANGO_APPS = [
    "channels",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

NATIVE_APPS = [
    "autho",
    "social_auth",
    "permission",
    "utils",
    "vehicle_repair",
    "gis",
    "feedback",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "djoser",
    "django_filters",
    "fcm_django",
    "corsheaders",
    "django_prometheus",
]

INSTALLED_APPS = DJANGO_APPS + NATIVE_APPS + THIRD_PARTY_APPS


MIDDLEWARE = [
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]

ROOT_URLCONF = "bazra_dj.urls"
ROOT_WEBSOCKETCONF = "bazra_dj.routing"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI_APPLICATION = 'bazra_dj.wsgi.application'
ASGI_APPLICATION = "bazra_dj.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
        },
    },
}


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get("DB_HOST"),
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "PORT": os.environ.get("DB_PORT"),
    }
}

if os.environ.get("DB_SSL_MODE_REQUIRED") == "true":
    DATABASES["default"]["OPTIONS"] = {"sslmode": "require"}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

APPEND_SLASH = True


# Bazra settings constants

AUTH_USER_MODEL = "autho.User"

AUTHENTICATION_BACKENDS = ["autho.authentication.CustomSimpleJWTAuthentication"]

REST_FRAMEWORK = {
    "COERCE_DECIMAL_TO_STRING": False,
    "DEFAULT_AUTHENTICATION_CLASSES": ("autho.authentication.CustomSimpleJWTAuthentication",),
}

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("BM",),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "TOKEN_OBTAIN_SERIALIZER": "autho.serializers.LoginSerializer",
}


RECOVERY_CODE = {
    "MAX_RETRIES": 5,
    "MAX_SENDS": 5,
    "OTP_TTL": 2,
}

VERIFICATION_CODE = {"MAX_RETRIES": 5, "MAX_SENDS": 5, "OTP_TTL": 2}


CELERY_BROKER_URL = "redis://redis:6379/1"

FIREBASE_APP = initialize_app()

FCM_DJANGO_SETTINGS = {
    "APP_VERBOSE_NAME": _("Bazra FCM"),
    "ONE_DEVICE_PER_USER": True,
    "DELETE_INACTIVE_DEVICES": True,
    "UPDATE_ON_DUPLICATE_REG_ID": True,
}


sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

# ========================================================================================
LOG_FILE_PATH = os.path.expanduser("~") + "/baatomechanic.log"


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.FileHandler",
            "filename": LOG_FILE_PATH,
        },
        "adminhandler": {  # NOTE: THIS IS NOT USED
            "level": "WARN",
            "formatter": "standard",
            "class": "logging.handlers.SMTPHandler",
            "mailhost": "",  # NOTE: add value here
            "fromaddr": "admin@baatomechanic.com",
            "toaddrs": ["krishna@baatomechanic.com"],
            "subject": "Warning/Error Log",
        },
    },
    "loggers": {
        "": {"handlers": ["default"], "level": "INFO", "propagate": False},
        "django.request": {
            "handlers": ["default"],
            "level": "WARN",
            "propagate": False,
        },
        "adminlogger": {  # NOTE: THIS IS NOT USED
            "handlers": ["adminhandler"],
            "level": "WARN",
            "propagate": False,
        },
    },
}


logging.config.dictConfig(LOGGING)


if STAGING:
    try:
        from bazra_dj.settings.local_settings import *  # noqa: F403, F401
    except ImportError as e:
        print(e)
        pass
