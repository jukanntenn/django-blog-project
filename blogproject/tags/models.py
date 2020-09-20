from core.models import TimeStampedModel
from django.db import models
from django.utils.translation import gettext_lazy as _
from taggit.models import GenericTaggedItemBase, TagBase


class Tag(TimeStampedModel, TagBase):
    class Meta:
        verbose_name = _("tag")
        verbose_name_plural = _("tags")


class TaggedItem(TimeStampedModel, GenericTaggedItemBase):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )

    class Meta:
        verbose_name = _("tagged item")
        verbose_name_plural = _("tagged items")
        unique_together = [["content_type", "object_id", "tag"]]
