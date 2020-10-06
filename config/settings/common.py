"""
Django settings for blogproject project.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import sys
from email.utils import getaddresses

import environ

env = environ.Env()
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = str(environ.Path(__file__) - 3)  # str for python < 3.5

# Project root
sys.path.append(os.path.join(BASE_DIR, "blogproject"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

SITE_ID = 1
SECRET_KEY = env("SECRET_KEY", default="fake-secret-key")
# Application definition
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

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

COMMENTS_APP = "comments"

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
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "blogproject", "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "notify.context_processors.notification_count",  # notification
                "constance.context_processors.config",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Password validation
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

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = "zh-hans"

TIME_ZONE = "Asia/Shanghai"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = (
    # 不要设置为包含 node_modules 的目录，因为其中会有一些奇怪命名的文件，使得 django 报错
    os.path.join(BASE_DIR, "frontend", "dist"),
)
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "django.contrib.staticfiles.finders.FileSystemFinder",
]

MEDIA_ROOT = os.path.join(BASE_DIR, "blogproject", "media")
MEDIA_URL = "/media/"

AUTH_USER_MODEL = "users.User"

# django-allauth
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

SOCIALACCOUNT_ADAPTER = "users.adapter.SocialAccountAdapter"
ACCOUNT_LOGOUT_ON_GET = True

LOGIN_REDIRECT_URL = "/"

# django-haystack
HAYSTACK_CONNECTIONS = {
    "default": {
        "ENGINE": "blog.whoosh_cn_backend.WhooshJiebaEngine",
        "PATH": os.path.join(BASE_DIR, "blogproject", "index", "whoosh"),
    },
}
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 20
HAYSTACK_SIGNAL_PROCESSOR = "haystack.signals.RealtimeSignalProcessor"
HAYSTACK_CUSTOM_HIGHLIGHTER = "blog.utils.Highlighter"

ADMINS = getaddresses([env("DJANGO_ADMINS", default="zmrenwu <zmrenwu@163.com>")])
MANAGERS = ADMINS
SERVER_EMAIL = env.str("DJANGO_SERVER_EMAIL", default="noreply@zmrenwu.com")

WEBPACK_LOADER = {
    "DEFAULT": {
        "CACHE": False,
        "BUNDLE_DIR_NAME": "",  # must end with slash
        "STATS_FILE": os.path.join(BASE_DIR, "frontend", "webpack-stats.json"),
        "POLL_INTERVAL": 0.1,
        "TIMEOUT": None,
        "IGNORE": [r".+\.hot-update.js", r".+\.map"],
    }
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
}

# 分页设置
PAGINATION_SETTINGS = {
    "PAGE_RANGE_DISPLAYED": 4,  # 分页条当前页前后应该显示的总页数（两边均匀分布，因此要设置为偶数），
    "MARGIN_PAGES_DISPLAYED": 1,  # 分页条开头和结尾显示的页数
    "SHOW_FIRST_PAGE_WHEN_INVALID": True,  # 当请求了不存在页，显示第一页
}

DJANGO_NOTIFICATIONS_CONFIG = {
    "SOFT_DELETE": True,
}

CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"
CONSTANCE_DATABASE_PREFIX = "constance:djangoblogproject:"

CONSTANCE_CONFIG = {
    "COMMENT_EMAIL_SUBJECT": ("", "", str),
    "NEWSLETTERS_SUBSCRIPTION_CONFIRMATION_SUBJECT": ("每日收藏精选订阅确认", "", str),
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

LOCALE_PATHS = [os.path.join(BASE_DIR, "locale")]

# celery
if USE_TZ:
    CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_URL = env("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = "django-db"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
