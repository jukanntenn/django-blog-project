from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TagsConfig(AppConfig):
    name = "tags"
    verbose_name = _("Tags")
