from .models import FriendLink
from django.contrib import admin


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
