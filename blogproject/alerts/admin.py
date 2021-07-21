from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import Alert


class AlertInline(GenericTabularInline):
    model = Alert


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ["id", "created_at", "modified_at"]
