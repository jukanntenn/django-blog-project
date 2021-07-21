from alerts.admin import AlertInline
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Category, Course, Material


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [
        AlertInline,
    ]
    list_display = ["id", "title", "slug"]


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    date_hierarchy = "pub_date"
    list_display = [
        "title",
        "rank",
        "pub_date",
        "created",
        "modified",
        "course",
        "views",
        "status",
        "show_on_index",
        "comment_enabled",
    ]
    list_filter = ["status", "course", "pub_date", "show_on_index", "comment_enabled"]

    fieldsets = (
        (None, {"fields": ("title", "body", "brief", "course")}),
        (
            _("Display control"),
            {
                "fields": (
                    "status",
                    "rank",
                    "pub_date",
                    "show_on_index",
                    "comment_enabled",
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
    search_fields = ["title", "body"]

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Category)
