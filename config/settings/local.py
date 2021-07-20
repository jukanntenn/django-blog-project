from .common import *  # noqa
from .common import env

DEBUG = True
SECRET_KEY = "fake-secret-key-for-development"
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["*"])

# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
INTERNAL_IPS = ["127.0.0.1", "localhost"]
if env.bool("USE_DOCKER", default=False):
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]

INSTALLED_APPS += [  # noqa
    "debug_toolbar",
]
MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")  # noqa
DEBUG_TOOLBAR_CONFIG = {
    "JQUERY_URL": "https://cdn.bootcdn.net/ajax/libs/jquery/3.6.0/jquery.min.js",
}


# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = env("DJANGO_EMAIL_HOST", default="localhost")
# https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = env.int("DJANGO_EMAIL_PORT", default=1025)


# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    "default": env.db("DATABASE_URL", "sqlite:///blogproject/database/db.sqlite3")
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True


# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {"default": env.cache("REDIS_URL", default="locmemcache://")}

# Celery
# ------------------------------------------------------------------------------
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-eager-propagates
CELERY_TASK_EAGER_PROPAGATES = True

# django-dbbackup
# ------------------------------------------------------------------------------
# https://django-dbbackup.readthedocs.io/en/master/configuration.html
DBBACKUP_STORAGE = "django.core.files.storage.FileSystemStorage"
DBBACKUP_STORAGE_OPTIONS = {"location": "backups"}
# DBBACKUP_STORAGE = "tencentcos_storage.TencentCOSStorage"
# DBBACKUP_CLEANUP_KEEP = 2
# DBBACKUP_CLEANUP_KEEP_MEDIA = 2

# django-tencentcos-storage
# ------------------------------------------------------------------------------
# https://github.com/jukanntenn/django-tencentcos-storage
# TENCENTCOS_STORAGE = {
#     "BUCKET": env.str("TENCENTCOS_STORAGE_BUCKET"),
#     "CONFIG": {
#         "Region": env.str("TENCENTCOS_STORAGE_CONFIG_Region"),
#         "SecretId": env.str("TENCENTCOS_STORAGE_CONFIG_SecretId"),
#         "SecretKey": env.str("TENCENTCOS_STORAGE_CONFIG_SecretKey"),
#     },
# }
