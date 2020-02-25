from django.contrib import admin

from .models import Alert


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ["text", "created", "modified"]
    filter_horizontal = ["scopes"]
