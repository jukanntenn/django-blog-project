from .common import *  # noqa

DEBUG = True
SECRET_KEY = "fake-secret-key-for-development"
ALLOWED_HOSTS = ["*"]

# debug toolbar
INTERNAL_IPS = ["127.0.0.1", "localhost"]

DEBUG_TOOLBAR_CONFIG = {
    "JQUERY_URL": "https://cdn.bootcss.com/jquery/3.3.1/jquery.min.js",
}

MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
INSTALLED_APPS += [
    "debug_toolbar",
]

# Email configuration
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST", default="localhost")
# https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = 1025
