from core.utils import generate_rich_content
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from django_comments.abstracts import CommentAbstractModel
from django_comments.managers import CommentManager
from mptt.managers import TreeManager
from mptt.models import MPTTModel, TreeForeignKey
from mptt.querysets import TreeQuerySet


class BlogCommentQuerySet(TreeQuerySet):
    def visible(self):
        return self.filter(is_public=True, is_removed=False)

    def roots(self):
        return self.visible().filter(parent__isnull=True)


class BlogCommentManager(TreeManager, CommentManager):
    pass


class BlogComment(MPTTModel, CommentAbstractModel):
    parent = TreeForeignKey(
        "self",
        verbose_name=_("parent comment"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="children",
    )
    objects = BlogCommentManager.from_queryset(BlogCommentQuerySet)()

    class Meta(CommentAbstractModel.Meta):
        verbose_name = _("comment")
        verbose_name_plural = _("comments")

    class MPTTMeta:
        # 必须加入 user_id，否则在调用 mptt 的 get_queryset_descendants 时，
        # 确保 select_related user 时 user_id 字段已经 load，否则会报错：
        # Field %s.%s cannot be both deferred and traversed using select_related at the same time.
        order_insertion_by = ["-submit_date", "user_id"]

    @cached_property
    def comment_html(self):
        rich_content = generate_rich_content(self.comment)
        return rich_content.get("content", "")
