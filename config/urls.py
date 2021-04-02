"""blogproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import core.views
from blog.feeds import AllPostsRssFeed
from blog.sitemaps import sitemaps
from comments import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("comments", views.CommentViewSet, basename="comment")

urlpatterns = [
    path("", include("blog.urls")),
    path("admin/", admin.site.urls),
    path("courses/", include("courses.urls")),
    path("comments/", include("django_comments.urls")),
    path("notifications/", include("notify.urls")),
    path("notifications/", include("notifications.urls")),
    path("accounts/", include("allauth.urls")),
    path("favorites/weekly/", include("favorites.urls")),
    path("newsletters/", include("newsletters.urls")),
    path("webtools/", include("webtools.urls")),
    path("watchman/", include("watchman.urls")),
    path("maintenance-mode/", include("maintenance_mode.urls")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("all/rss/", AllPostsRssFeed()),
    path("api/v1/", include(router.urls)),
    # API docs
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger",
    ),
    path(
        "redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path("__debug__", include(debug_toolbar.urls)),
        # email debug
        path("_debug/email/single/", core.views.SingleEmailDebugView.as_view()),
        path("_debug/email/mass/", core.views.MassEmailDebugView.as_view()),
    ]
