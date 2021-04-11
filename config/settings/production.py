import logging

import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

from .common import *  # noqa
from .common import env

SECRET_KEY = env.str("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")
DEBUG = False

# DATABASES
# ------------------------------------------------------------------------------
DATABASES = {"default": env.db("DATABASE_URL")}  # noqa F405
DATABASES["default"]["ATOMIC_REQUESTS"] = True  # noqa F405
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)  # noqa F405

# CACHES
# ------------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env.str("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # Mimicing memcache behavior.
            # http://jazzband.github.io/django-redis/latest/#_memcached_exceptions_behavior
            "IGNORE_EXCEPTIONS": True,
        },
    }
}


# django anymail
ANYMAIL = {
    "SENDGRID_API_KEY": env.str("DJANGO_ANYMAIL_SENDGRID_API_KEY"),
}
EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
CELERY_EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"
DEFAULT_FROM_EMAIL = "admin@zmrenwu.com"

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# django-dbbackup
# ------------------------------------------------------------------------------
# https://django-dbbackup.readthedocs.io/en/master/configuration.html
# DBBACKUP_STORAGE = "storages.backends.dropbox.DropBoxStorage"
# DBBACKUP_STORAGE_OPTIONS = {
#     "oauth2_access_token": env.str("DJANGO_DBBACKUP_DROPBOX_OAUTH2_ACCESS_TOKEN"),
# }
DBBACKUP_STORAGE = "django_storage_qcloud.storage.QcloudStorage"
DBBACKUP_CLEANUP_KEEP = 2
DBBACKUP_CLEANUP_KEEP_MEDIA = 2

CELERY_BROKER_URL = env.str("CELERY_BROKER_URL")

# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "django.db.backends": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
        # Errors logged by the SDK itself
        "sentry_sdk": {"level": "ERROR", "handlers": ["console"], "propagate": False},
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

# Sentry
# ------------------------------------------------------------------------------
SENTRY_DSN = env.str("SENTRY_DSN", default="")
SENTRY_LOG_LEVEL = env.int("DJANGO_SENTRY_LOG_LEVEL", logging.INFO)

if SENTRY_DSN != "":
    sentry_logging = LoggingIntegration(
        level=SENTRY_LOG_LEVEL,  # Capture info and above as breadcrumbs
        event_level=logging.ERROR,  # Send errors as events
    )
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[sentry_logging, DjangoIntegration(), CeleryIntegration()],
        traces_sample_rate=1.0,
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,
    )

WATCHMAN_TOKENS = env.str("DJANGO_WATCHMAN_TOKENS")


# django-storage-qcloud
# ------------------------------------------------------------------------------
# https://github.com/fordguo/django-storage-qcloud
QCLOUD_STORAGE_OPTION = {
    "SecretId": env.str("QCLOUD_STORAGE_OPTION_SECRET_ID"),
    "SecretKey": env.str("QCLOUD_STORAGE_OPTION_SECRET_KEY"),
    "Region": env.str("QCLOUD_STORAGE_OPTION_REGION"),
    "Bucket": env.str("QCLOUD_STORAGE_OPTION_BUCKET"),
}
