from django.contrib import admin
from django_comments.admin import CommentsAdmin

from .models import BlogComment


@admin.register(BlogComment)
class BlogCommentAdmin(CommentsAdmin):
    list_select_related = ["user"]
