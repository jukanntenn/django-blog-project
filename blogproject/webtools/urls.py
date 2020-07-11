from django.urls import path

from . import views

app_name = "webtools"
urlpatterns = [
    path(
        "django-secret-key-creator",
        views.DjangoSecretKeyCreateView.as_view(),
        name="create_django_secret_key",
    ),
]
