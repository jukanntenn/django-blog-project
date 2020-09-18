from datetime import timedelta

import pytest
from blog.models import Post
from blog.tests.factories import PostFactory
from core.utils import compensate, generate_rich_content, get_index_entry_queryset
from courses.models import Material
from courses.tests.factories import MaterialFactory
from django.utils import timezone


def test_generate_rich_content():
    value = "~~del~~"
    result = generate_rich_content(value)
    assert result["content"] == "<p><del>del</del></p>"
    assert result["toc"] == ""

    value = "# 标题"
    result = generate_rich_content(value)
    assert result["content"] == '<h1 id="标题">标题</h1>'
    assert result["toc"] == '<li><a href="#标题">标题</a></li>'

    value = "# header"
    result = generate_rich_content(value, toc_url="/absolute/")
    assert result["toc"] == '<li><a href="/absolute/#header">header</a></li>'


def test_compensate():
    assert compensate("-field") == "-field"
    assert compensate("--field") == "field"
    assert compensate("field") == "field"


@pytest.mark.django_db
def test_get_index_entry_queryset():
    now = timezone.now()

    pinned_post1 = PostFactory(
        status=Post.STATUS_CHOICES.published,
        pinned=True,
        show_on_index=True,
        pub_date=now,
    )
    pinned_post2 = PostFactory(
        status=Post.STATUS_CHOICES.published,
        pinned=True,
        show_on_index=True,
        pub_date=now - timedelta(days=1),
    )
    material = MaterialFactory(
        status=Material.STATUS.published, show_on_index=True, pub_date=now
    )
    post = PostFactory(
        status=Post.STATUS_CHOICES.published,
        pinned=False,
        show_on_index=True,
        pub_date=now - timedelta(days=1),
    )

    expected = [pinned_post1.id, pinned_post2.id, material.id, post.id]
    assert [entry.id for entry in get_index_entry_queryset()] == expected
