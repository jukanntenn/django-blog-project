import re

import markdown
from bs4 import BeautifulSoup
from constance import config
from django.apps import apps
from django.core import signing
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import BooleanField, CharField, Count, F, Value
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension


def generate_rich_content(value, *, toc_depth=2, toc_url=""):
    md = markdown.Markdown(
        extensions=[
            "markdown.extensions.extra",
            "markdown.extensions.codehilite",
            "markdown.extensions.admonition",
            "markdown.extensions.nl2br",
            TocExtension(slugify=slugify, toc_depth=toc_depth),
            "pymdownx.magiclink",
            "pymdownx.tasklist",
            "pymdownx.tilde",
            "pymdownx.caret",
        ]
    )
    content = md.convert(value)
    toc = md.toc

    soup = BeautifulSoup(toc, "html.parser")
    # must use contents, not children
    # if soup.ul.contents:
    toc = "".join(map(str, soup.ul.contents)).strip()

    if toc_url:

        def absolutify(matchobj):
            return 'href="{toc_url}{frag}"'.format(
                toc_url=toc_url, frag=matchobj.group(1)
            )

        toc = re.sub('href="(.+)"', absolutify, toc)
    return {"content": content, "toc": toc}


def compensate(value):
    if value.startswith("--"):
        return value.lstrip("--")
    return value


def get_index_entry_queryset():
    from blog.models import Post
    from courses.models import Material

    post_qs = Post.index.annotate(
        comment_count=Count("comments"),
        course__slug=Value("", CharField(max_length=100)),
        type=Value("p", CharField(max_length=1)),
    ).order_by()
    post_qs = post_qs.values_list(
        "id",
        "title",
        "brief",
        "views",
        "course__slug",
        "comment_count",
        "pub_date",
        "pinned",
        "type",
        named=True,
    )

    material_qs = (
        Material.index.annotate(pinned=Value(False, BooleanField()))
        .annotate(
            comment_count=Count("comments"),
            course__slug=F("course__slug"),
            type=Value("m", CharField(max_length=1)),
        )
        .order_by()
    )
    material_qs = material_qs.values_list(
        "id",
        "title",
        "brief",
        "views",
        "course__slug",
        "comment_count",
        "pub_date",
        "pinned",
        "type",
        named=True,
    )

    entry_qs = post_qs.union(material_qs)
    # In sqlite3, `False` takes first, but not sure in MySQL...
    entry_qs = entry_qs.order_by(F("pinned").desc(), "-pub_date")
    return entry_qs


class EmailConfirmation:
    salt = "django-blog-project"

    def __init__(self, instance):
        self.instance = instance

    def make_key(self):
        model_cls = self.instance.__class__
        app_label = model_cls._meta.app_label
        model_name = model_cls._meta.model_name
        return signing.dumps(
            obj={
                "app_label": app_label,
                "model_name": model_name,
                "pk": self.instance.pk,
            },
            salt=self.salt,
        )

    @classmethod
    def from_key(cls, key):
        try:
            max_age = 60 * 60 * 24 * config.EMAIL_CONFIRMATION_EXPIRE_DAYS
            data = signing.loads(key, max_age=max_age, salt=cls.salt)
            model_cls = apps.get_model(data["app_label"], data["model_name"])
            return EmailConfirmation(
                instance=model_cls._default_manager.get(pk=data["pk"])
            )
        except (
            signing.SignatureExpired,
            signing.BadSignature,
            ObjectDoesNotExist,
        ):
            return
