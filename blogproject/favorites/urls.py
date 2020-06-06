from django.urls import path

from . import views

app_name = "favorites"
urlpatterns = [
    path("issues/", views.IssueListView.as_view(), name="issue_list"),
    path("issues/<int:number>/", views.IssueDetailView.as_view(), name="issue_detail"),
]
