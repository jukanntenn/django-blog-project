from django.db.models import Manager, QuerySet, Sum
from django.db.models.functions import Coalesce
from django.utils import timezone


class MaterialQuerySet(QuerySet):
    def published(self):
        return self.filter(status=self.model.STATUS.published)

    def writing(self):
        return self.filter(status=self.model.STATUS.writing)

    def draft(self):
        return self.filter(status=self.model.STATUS.draft)

    def hidden(self):
        return self.filter(status=self.model.STATUS.hidden)

    def searchable(self):
        return self.published().filter(pub_date__lte=timezone.now())


class MaterialManager(Manager.from_queryset(MaterialQuerySet)):
    pass


class IndexMaterialManager(MaterialManager):
    def get_queryset(self):
        return super().get_queryset().searchable().filter(show_on_index=True)
