from django.contrib import admin

from .models import Favorite, Issue


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ["id", "number", "pub_date"]
    fields = [
        "description",
        "pub_date",
        "number",
        "tags",
    ]
    filter_horizontal = ["tags"]

    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        super().save_model(request, obj, form, change)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ["id", "rank", "title", "issue", "url"]
