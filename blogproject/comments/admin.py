from django.contrib import admin

from .models import BlogComment
from django_comments.admin import CommentsAdmin


@admin.register(BlogComment)
class BlogCommentAdmin(CommentsAdmin):
    list_select_related = ['user']
