import logging.config
import os


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": "db",
        # 'HOST': 'localhost',
        # "HOST": "127.0.0.1",
        "NAME": "bazra",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "PORT": "5432",
    }
}


# For smtp4dev
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "192.168.1.79"
EMAIL_HOST_USER = None
EMAIL_HOST_PASSWORD = None
EMAIL_PORT = "26"

# For gmail
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = "smtp.gmail.com"
# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False
# EMAIL_PORT = 587
# EMAIL_HOST_USER = "your google id"
# EMAIL_HOST_PASSWORD = "your password"


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
