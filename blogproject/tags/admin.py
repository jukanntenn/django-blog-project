from django.contrib import admin

from .models import Tag, TaggedItem


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "created_at", "modified_at")


@admin.register(TaggedItem)
class TaggedItemAdmin(admin.ModelAdmin):
    pass
