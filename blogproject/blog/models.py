from core.abstracts import AbstractEntry
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from model_utils import Choices
from model_utils.models import TimeStampedModel
from taggit_selectize.managers import TaggableManager
from tags.models import TaggedItem

from .managers import IndexPostManager, PostManager


class Tag(models.Model):
    name = models.CharField(_("name"), max_length=100)

    class Meta:
        verbose_name = _("tag")
        verbose_name_plural = _("tags")

    def __str__(self):
        return self.name


class Category(TimeStampedModel):
    name = models.CharField(_("name"), max_length=100)
    title = models.CharField(_("title"), max_length=255, blank=True)
    slug = models.SlugField(_("slug"), unique=True)
    description = models.TextField(_("description"), blank=True)
    cover = models.ImageField(
        _("cover"), upload_to="covers/categories/%Y/%m/%d/", blank=True
    )
    cover_thumbnail = ImageSpecField(
        source="cover",
        processors=[ResizeToFill(500, 300)],
        format="JPEG",
        options={"quality": 90},
    )
    cover_caption = models.CharField(_("cover caption"), max_length=255, blank=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("creator"), on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.name

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:category", kwargs={"slug": self.slug})


def post_cover_path(instance, filename):
    """已弃用，保留仅为了兼容性"""
    return ""


class Post(AbstractEntry):
    # Todo: 统一 Post 和 Material 的状态选项
    STATUS_CHOICES = Choices(
        (1, "published", _("published")),
        (2, "draft", _("draft")),
        (3, "hidden", _("hidden")),
    )

    status = models.PositiveSmallIntegerField(
        _("status"), choices=STATUS_CHOICES, default=STATUS_CHOICES.draft
    )
    pinned = models.BooleanField(_("pinned"), default=False)

    # Todo：移除封面字段
    cover = models.ImageField(_("cover"), upload_to="covers/posts/", blank=True)
    cover_thumbnail = ImageSpecField(
        source="cover",
        processors=[ResizeToFill(60, 60)],
        format="JPEG",
        options={"quality": 90},
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name=_("category"),
        null=True,
        blank=True,
    )
    tags = TaggableManager(verbose_name=_("tags"), through=TaggedItem, blank=True)

    # 模型管理器
    objects = PostManager()
    index = IndexPostManager()

    class Meta:
        verbose_name = _("Posts")
        verbose_name_plural = _("Posts")
        ordering = ["-pub_date", "-created"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.excerpt:
            self.excerpt = strip_tags(self.body_html)[:150]

        if not self.pub_date and self.status == self.STATUS_CHOICES.published:
            self.pub_date = self.created

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"pk": self.pk})

    @property
    def type(self):
        return "p"


class Medium(TimeStampedModel):
    FLAG_CHOICES = (
        (0, "QQ 群"),
        (1, "知乎专栏"),
    )
    flag = models.SmallIntegerField(_("flag"), choices=FLAG_CHOICES)
    name = models.CharField(_("name"), max_length=200)
    identifier = models.CharField(_("identifier"), max_length=300)

    class Meta:
        verbose_name = _("medium")
        verbose_name_plural = _("mediums")
        ordering = ["flag", "name"]

    def __str__(self):
        return "{}: {}/{}".format(self.flag, self.name, self.identifier)


class FriendLink(TimeStampedModel):
    site_name = models.CharField(_("site_name"), max_length=100)
    site_domain = models.URLField(_("site_domain"))

    class Meta:
        verbose_name = _("friend link")
        verbose_name_plural = _("friend links")

    def __str__(self):
        return self.site_name


class Recommendation(TimeStampedModel):
    pic = models.ImageField(_("picture"), upload_to="recommendation/", blank=True)
    pic_thumbnail = ImageSpecField(
        source="pic",
        processors=[ResizeToFill(100, 100)],
        format="JPEG",
        options={"quality": 80},
    )
    url = models.URLField(_("url"), blank=True)
    description = models.TextField(_("description"))

    class Meta:
        verbose_name = _("recommendation")
        verbose_name_plural = _("recommendations")

    def __str__(self):
        return self.description[:50]
