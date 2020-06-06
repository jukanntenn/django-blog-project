from django.urls import path, re_path

from . import views

app_name = "newsletters"
urlpatterns = [
    path("subscription/", views.SubscriptionCreateView.as_view(), name="subscription"),
    re_path(
        r"^subscription/confirm/(?P<key>[-:\w]+)/$",
        views.SubscriptionConfirmView.as_view(),
        name="subscription-confirm",
    ),
]
