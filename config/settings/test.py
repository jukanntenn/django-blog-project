from .common import *  # noqa

DEBUG = True
SECRET_KEY = "fake-secret-key-for-test"
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS += [
    "core.tests",
]
DDF_NUMBER_OF_LAPS = 1

# Email configuration
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

ADMINS = [("admin", "admin@example.com")]
MANAGERS = ADMINS
LANGUAGE_CODE = "en-us"
