from .common import *  # noqa
from .common import env, os

SECRET_KEY = env("SECRET_KEY")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")
DEBUG = False

# DATABASES
# ------------------------------------------------------------------------------
DATABASES = {"default": env.db("DATABASE_URL")}  # noqa F405
DATABASES["default"]["ATOMIC_REQUESTS"] = True  # noqa F405
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)  # noqa F405

# django anymail
ANYMAIL = {
    "SENDGRID_API_KEY": os.environ.get("DJANGO_SENDGRID_API_KEY"),
}
EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"
CELERY_EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
DEFAULT_FROM_EMAIL = "admin@zmrenwu.com"

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
