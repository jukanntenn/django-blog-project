from .common import *  # noqa
from .common import env


SECRET_KEY = env("SECRET_KEY")

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")

DEBUG = False

# django anymail
ANYMAIL = {
    "SENDGRID_API_KEY": os.environ.get("DJANGO_SENDGRID_API_KEY"),
}
EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"
DEFAULT_FROM_EMAIL = "admin@zmrenwu.com"

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
