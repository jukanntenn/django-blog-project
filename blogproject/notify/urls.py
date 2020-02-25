from django.urls import path

from . import views

app_name = "notify"
urlpatterns = [
    path("", views.AllNotificationsListView.as_view(), name="notification_all"),
    path(
        "unread/",
        views.UnreadNotificationsListView.as_view(),
        name="notification_unread",
    ),
]
