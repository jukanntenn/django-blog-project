from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedModel


class Subscription(TimeStampedModel):
    email = models.EmailField(_("email"))
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("user"),
        on_delete=models.SET_NULL,
        null=True,
    )
    confirmed = models.BooleanField(_("confirmed"), default=False)
    active = models.BooleanField(_("active"), default=False)

    class Meta:
        verbose_name = _("subscription")
        verbose_name_plural = _("subscriptions")
        ordering = ["-created_at"]

    def __str__(self):
        return self.email

    def confirm(self):
        self.confirmed = True
        self.active = True
        self.save(update_fields=["confirmed", "active"])
