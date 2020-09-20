from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Category, FriendLink, Medium, Post, Recommendation, Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    date_hierarchy = "pub_date"
    list_display = [
        "title",
        "pub_date",
        "created",
        "modified",
        "category",
        "views",
        "status",
        "show_on_index",
        "pinned",
        "comment_enabled",
    ]
    list_filter = [
        "status",
        "category",
        "pub_date",
        "show_on_index",
        "comment_enabled",
        "pinned",
    ]

    fieldsets = (
        (None, {"fields": ("title", "body", "brief", "category")}),
        (
            _("Display control"),
            {
                "fields": (
                    "status",
                    "pub_date",
                    "show_on_index",
                    "comment_enabled",
                    "pinned",
                ),
            },
        ),
        (
            _("SEO"),
            {
                "fields": ("excerpt",),
            },
        ),
    )
    filter_horizontal = []
    search_fields = ["title", "body"]

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Medium)
class MediumAdmin(admin.ModelAdmin):
    list_display = ["flag", "name", "identifier"]


@admin.register(FriendLink)
class FriendLinkAdmin(admin.ModelAdmin):
    list_display = ["site_name", "site_domain"]


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Recommendation)
