from django.contrib import admin

from .models import FriendLink


@admin.register(FriendLink)
class FriendLinkAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "rank",
        "site_name",
        "site_link",
        "created_at",
        "modified_at",
    ]
