"""
Django settings for django-blog-project project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import sys
from email.utils import getaddresses
from pathlib import Path

import environ
from django.core.exceptions import ImproperlyConfigured
from watchman import constants as watchman_constants

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
APPS_DIR = ROOT_DIR / "blogproject"
sys.path.append(str(APPS_DIR))

env = environ.Env()
READ_ENV_FILE = env.bool("READ_ENV_FILE", default=True)
if READ_ENV_FILE:
    # OS environment variables take precedence over variables from env file
    env.read_env(str(ROOT_DIR / "blogproject.env"))


# GENERAL
# ------------------------------------------------------------------------------
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = "Asia/Shanghai"
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "zh-hans"
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = [str(ROOT_DIR / "locale")]


# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "config.urls"
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "config.wsgi.application"


# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "django.contrib.sites",
    "django.contrib.redirects",
]
THIRD_PARTY_APPS = [
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.weibo",
    "allauth.socialaccount.providers.github",
    "django_comments",
    "django_extensions",
    "haystack",
    "notifications",
    "webpack_loader",
    "rest_framework",
    "rest_framework.authtoken",
    "pure_pagination",
    "constance",
    "constance.backends.database",
    "djcelery_email",
    "dbbackup",
    "django_celery_results",
    "django_celery_beat",
    "watchman",
    "maintenance_mode",
    "drf_spectacular",
]
LOCAL_APPS = [
    "blog.apps.BlogConfig",
    "comments.apps.CommentsConfig",
    "courses.apps.CoursesConfig",
    "notify",
    "users.apps.UsersConfig",
    "alerts.apps.AlertsConfig",
    "favorites.apps.FavoritesConfig",
    "newsletters.apps.NewslettersConfig",
    "webtools.apps.WebtoolsConfig",
    "friendlinks.apps.FriendlinksConfig",
    "tags.apps.TagsConfig",
    "taskapp.celery.CeleryAppConfig",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.redirects.middleware.RedirectFallbackMiddleware",
    "maintenance_mode.middleware.MaintenanceModeMiddleware",
]

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(APPS_DIR / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "constance.context_processors.config",
                "maintenance_mode.context_processors.maintenance_mode",
                "notify.context_processors.notification_count",  # notification
            ],
        },
    },
]


# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa
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


# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR / "static")
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    str(ROOT_DIR / "frontend/build"),
]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "django.contrib.staticfiles.finders.FileSystemFinder",
]


# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR / "media")
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"


# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)
AUTH_USER_MODEL = "users.User"
LOGIN_REDIRECT_URL = "/"


# ADMIN
# ------------------------------------------------------------------------------
ADMIN_URL = "admin/"
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = getaddresses([env("DJANGO_ADMINS", default="zmrenwu <zmrenwu@163.com>")])
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS


# EMAIL
# -----------------------------------------------------------------
SERVER_EMAIL = env.str("DJANGO_SERVER_EMAIL", default="noreply@zmrenwu.com")
# https://docs.djangoproject.com/en/dev/ref/settings/#email-timeout
EMAIL_TIMEOUT = 5
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
email_backend = env.str("DJANGO_EMAIL_BACKEND", default="console")
if email_backend == "console":
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
elif email_backend == "smtp":
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
elif email_backend == "file":
    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
    EMAIL_FILE_PATH = str(APPS_DIR / "app-messages")
else:
    raise ImproperlyConfigured(
        f"Invalid DJANGO_EMAIL_BACKEND: {email_backend}. "
        "Valid choices are console, smtp, file."
    )


# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "DENY"


# django-celery-email
# ------------------------------------------------------------------------------
# https://github.com/pmclanahan/django-celery-email
async_email = env.bool("ASYNC_EMAIL", default=False)
if async_email:
    CELERY_EMAIL_BACKEND = EMAIL_BACKEND
    EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
    CELERY_EMAIL_TASK_CONFIG = {
        "ignore_result": True,
    }


# python-webpack-boilerplate
# ------------------------------------------------------------------------------
# https://python-webpack-boilerplate.readthedocs.io/en/latest/setup_with_django/
WEBPACK_LOADER = {
    "MANIFEST_FILE": str(ROOT_DIR / "frontend" / "build" / "manifest.json"),
}

# Django REST framework
# ------------------------------------------------------------------------------
# https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# django-pure-pagination
# ------------------------------------------------------------------------------
# https://github.com/jamespacileo/django-pure-pagination
PAGINATION_SETTINGS = {
    "PAGE_RANGE_DISPLAYED": 4,  # 分页条当前页前后应该显示的总页数（两边均匀分布，因此要设置为偶数），
    "MARGIN_PAGES_DISPLAYED": 1,  # 分页条开头和结尾显示的页数
    "SHOW_FIRST_PAGE_WHEN_INVALID": True,  # 当请求了不存在页，显示第一页
}


# django-notifications
# ------------------------------------------------------------------------------
# https://github.com/django-notifications/django-notifications
DJANGO_NOTIFICATIONS_CONFIG = {
    "SOFT_DELETE": True,
}


# django-constance
# ------------------------------------------------------------------------------
CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"
CONSTANCE_DATABASE_PREFIX = "constance:djangoblogproject:"
CONSTANCE_CONFIG = {
    "NEWSLETTERS_SUBSCRIPTION_CONFIRMATION_SUBJECT": ("每日收藏精选订阅确认", "", str),
    "COMMENT_EMAIL_SUBJECT": ("新的文章评论", "", str),
    "REPLY_EMAIL_SUBJECT": ("评论有了新回复", "", str),
    "LOGO": ("追梦人物的博客", "博客 Logo", str),
    "EMAIL_CONFIRMATION_EXPIRE_DAYS": (3, "验证邮件有效天数", int),
    "BAIDU_SCRIPT": ("", "百度统计 JavaScript 脚本", str),
}
CONSTANCE_CONFIG_FIELDSETS = {
    "Blog Settings": [
        "LOGO",
        "EMAIL_CONFIRMATION_EXPIRE_DAYS",
        "NEWSLETTERS_SUBSCRIPTION_CONFIRMATION_SUBJECT",
    ],
    "Comment Notification Email": ["COMMENT_EMAIL_SUBJECT", "REPLY_EMAIL_SUBJECT"],
    "SEO": ["BAIDU_SCRIPT"],
}


# Celery
# ------------------------------------------------------------------------------
if USE_TZ:
    # http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-timezone
    CELERY_TIMEZONE = TIME_ZONE
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-broker_url
CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="redis://localhost:6379/0")
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_backend
CELERY_RESULT_BACKEND = "django-db"
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-accept_content
CELERY_ACCEPT_CONTENT = ["json"]
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-task_serializer
CELERY_TASK_SERIALIZER = "json"
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_serializer
CELERY_RESULT_SERIALIZER = "json"
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-time-limit
# todo: set to whatever value is adequate in your circumstances
CELERY_TASK_TIME_LIMIT = 5 * 60
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-soft-time-limit
# todo: set to whatever value is adequate in your circumstances
CELERY_TASK_SOFT_TIME_LIMIT = 60
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#beat-scheduler
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
CELERY_BROKER_TRANSPORT_OPTIONS = {"max_retries": 3}


# django-watchman
# ------------------------------------------------------------------------------
# https://django-watchman.readthedocs.io/en/latest/readme.html#paid-checks
# WATCHMAN_ENABLE_PAID_CHECKS = True
WATCHMAN_CHECKS = watchman_constants.DEFAULT_CHECKS + ("watchman.checks.email",)
WATCHMAN_TOKENS = "django-watchman-token"
WATCHMAN_EMAIL_SENDER = SERVER_EMAIL
WATCHMAN_EMAIL_RECIPIENTS = [a[1] for a in MANAGERS]


# django-maintenance-mode
# ------------------------------------------------------------------------------
# https://github.com/fabiocaccamo/django-maintenance-mode
MAINTENANCE_MODE_IGNORE_ADMIN_SITE = True


# drf-spectacular
# ------------------------------------------------------------------------------
# https://drf-spectacular.readthedocs.io/en/latest/settings.html
SPECTACULAR_SETTINGS = {
    # path prefix is used for tagging the discovered operations.
    # use '/api/v[0-9]' for tagging apis like '/api/v1/albums' with ['albums']
    "SCHEMA_PATH_PREFIX": r"/api/v[0-9]",
}

# django-haystack
# -----------------------------------------------------------------
# https://django-haystack.readthedocs.io/en/master/settings.html
HAYSTACK_CONNECTIONS = {
    "default": {
        "ENGINE": "blog.whoosh_cn_backend.WhooshJiebaEngine",
        "PATH": str(APPS_DIR / "index" / "whoosh"),
    },
}
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 20
HAYSTACK_SIGNAL_PROCESSOR = "haystack.signals.RealtimeSignalProcessor"
HAYSTACK_CUSTOM_HIGHLIGHTER = "blog.utils.Highlighter"


# django-allauth
# -----------------------------------------------------------------------
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_LOGOUT_ON_GET = True
SOCIALACCOUNT_ADAPTER = "users.adapter.SocialAccountAdapter"


# django-contrib-comments
# -----------------------------------------------------------------------
# https://django-contrib-comments.readthedocs.io/en/latest/settings.html
COMMENTS_APP = "comments"
