from braces.views import SetHeadlineMixin
from django.views.generic import DetailView, ListView

from .models import Issue


class IssueListView(SetHeadlineMixin, ListView):
    model = Issue
    context_object_name = "issue_list"
    template_name = "favorites/issue_list.html"
    paginate_by = 15
    headline = "每周精选收藏"

    def get_queryset(self):
        return super().get_queryset().prefetch_related("tags").order_by("-number")


class IssueDetailView(SetHeadlineMixin, DetailView):
    model = Issue
    context_object_name = "issue"
    template_name = "favorites/issue_detail.html"
    slug_field = "number"
    slug_url_kwarg = "number"

    def get_context_data(self, *, object_list=None, **kwargs):
        issue = self.object
        favorite_qs = issue.favorites.order_by("rank", "-created_at")
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["favorite_list"] = favorite_qs
        return context

    def get_headline(self):
        return "第{}周精选收藏".format(self.get_object().number)
