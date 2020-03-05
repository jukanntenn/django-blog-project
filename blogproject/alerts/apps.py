from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AlertsConfig(AppConfig):
    name = "alerts"
    verbose_name = _("alerts")
