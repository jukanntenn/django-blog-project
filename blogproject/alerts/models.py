from django.db import models

from model_utils.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _


class Alert(TimeStampedModel):
    text = models.TextField(_('text'))
    scopes = models.ManyToManyField('courses.Course', verbose_name=_('scopes'))

    class Meta:
        verbose_name = _('alert')
        verbose_name_plural = _('alerts')

    def __str__(self):
        return self.text[:20]
