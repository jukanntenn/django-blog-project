from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedModel


class Issue(TimeStampedModel):
    number = models.PositiveSmallIntegerField(_("number"), unique=True)
    pub_date = models.DateTimeField(_("publication datetime"))
    description = models.TextField(_("description"))
    tags = models.ManyToManyField("blog.Tag", verbose_name=_("tags"))
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("creator"),
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        ordering = ["-number"]
        verbose_name = _("issue")
        verbose_name_plural = _("issues")

    def __str__(self):
        return "{}".format(self.number)

    def get_absolute_url(self):
        return reverse("favorites:issue_detail", kwargs={"number": self.number})


class Favorite(TimeStampedModel):
    issue = models.ForeignKey(
        Issue,
        verbose_name=_("issue"),
        on_delete=models.SET_NULL,
        null=True,
        related_name="favorites",
    )
    title = models.CharField(_("title"), max_length=200)
    description = models.TextField(_("description"))
    url = models.URLField(_("url"))
    tags = models.ManyToManyField("blog.Tag", verbose_name=_("tags"))
    rank = models.IntegerField(_("rank"), default=0)

    class Meta:
        ordering = ["rank", "-created_at"]
        verbose_name = _("favorite")
        verbose_name_plural = _("favorites")

    def __str__(self):
        return self.title
