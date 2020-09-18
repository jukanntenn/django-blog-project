from braces.views import SetHeadlineMixin
from notifications.views import AllNotificationsList, UnreadNotificationsList
from pure_pagination.mixins import PaginationMixin


class AllNotificationsListView(PaginationMixin, SetHeadlineMixin, AllNotificationsList):
    headline = "全部通知"
    paginate_by = 10
    prefetch_related = ("actor", "target")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["num_all"] = self.request.user.notifications.active().count()
        context["num_unread"] = self.request.user.notifications.unread().count()
        return context


class UnreadNotificationsListView(
    PaginationMixin, SetHeadlineMixin, UnreadNotificationsList
):
    headline = "未读通知"
    paginate_by = 10
    prefetch_related = ("actor", "target")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["num_all"] = self.request.user.notifications.active().count()
        context["num_unread"] = self.request.user.notifications.unread().count()
        return context
