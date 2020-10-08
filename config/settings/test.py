from .common import *  # noqa

DEBUG = True
SECRET_KEY = "fake-secret-key-for-test"
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS += [  # noqa
    "core.tests",
]

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# DATABASE
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "ATOMIC_REQUESTS": True,
    }
}

ADMINS = [("admin", "admin@example.com")]
MANAGERS = ADMINS
LANGUAGE_CODE = "en-us"

WEBPACK_LOADER["DEFAULT"]["STATS_FILE"] = os.path.join(
    BASE_DIR, "frontend", "webpack-test-stats.json"
)
