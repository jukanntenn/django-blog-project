from core.models import TimeStampedModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class FriendLink(TimeStampedModel):
    site_name = models.CharField(_("site name"), max_length=100)
    site_link = models.URLField(_("site link"))
    rank = models.IntegerField(_("rank"), default=0)

    class Meta:
        verbose_name = _("friend link")
        verbose_name_plural = _("friend links")
        ordering = ["rank", "created_at"]

    def __str__(self):
        return self.site_name
