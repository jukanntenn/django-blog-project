from django.db.models import Manager
from django.utils import timezone
from django.db.models import QuerySet


class PostQuerySet(QuerySet):
    def published(self):
        return self.filter(status=self.model.STATUS_CHOICES.published)

    def draft(self):
        return self.filter(status=self.model.STATUS_CHOICES.draft)

    def hidden(self):
        return self.filter(status=self.model.STATUS_CHOICES.hidden)

    def searchable(self):
        return self.published().filter(pub_date__lte=timezone.now())


class PostManager(Manager.from_queryset(PostQuerySet)):
    pass


class IndexPostManager(Manager.from_queryset(PostQuerySet)):
    """
    专门用于管理首页文章的模型管理器
    """

    def get_queryset(self):
        return super().get_queryset().searchable().filter(show_on_index=True)
