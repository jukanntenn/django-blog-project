from datetime import timedelta

import pytest
from blog.models import Post
from blog.tests.factories import CategoryFactory, PostFactory
from django.utils import timezone


@pytest.mark.django_db
class TestPost:
    def test_auto_populate_excerpt_from_body(self):
        post = PostFactory(body="正文" * 100)
        assert len(post.excerpt) == 150

    def test_auto_set_pub_date_for_published_post(self):
        post = PostFactory(
            status=Post.STATUS_CHOICES.published,
        )
        assert post.pub_date == post.created

    def test_type_property(self, post):
        assert post.type == "p"

    def test_get_absolute_url(self, post):
        assert post.get_absolute_url() == f"/post/{post.pk}/"


@pytest.mark.django_db
class TestPostQuerySetAndIndexManager:
    def setup_method(self):
        after_3_days = timezone.now() + timedelta(days=3)

        self.published_post = PostFactory(
            status=Post.STATUS_CHOICES.published,
            show_on_index=True,
        )
        self.draft_post = PostFactory(
            status=Post.STATUS_CHOICES.draft,
            show_on_index=True,
        )
        self.hidden_post = PostFactory(
            status=Post.STATUS_CHOICES.hidden,
            show_on_index=True,
        )
        self.future_publishing_post = PostFactory(
            status=Post.STATUS_CHOICES.published,
            show_on_index=True,
            pub_date=after_3_days,
        )
        self.future_draft_post = PostFactory(
            status=Post.STATUS_CHOICES.draft,
            show_on_index=True,
            pub_date=after_3_days,
        )
        self.hide_on_index_published_post = PostFactory(
            status=Post.STATUS_CHOICES.published,
            show_on_index=False,
        )

    def test_published(self):
        posts = Post.objects.published()
        assert posts.count() == 3
        # Note the ordering
        assert list(posts) == [
            self.future_publishing_post,
            self.hide_on_index_published_post,
            self.published_post,
        ]

    def test_draft(self):
        posts = Post.objects.draft()
        assert posts.count() == 2
        # Note the ordering
        assert list(posts) == [self.future_draft_post, self.draft_post]

    def test_hidden(self):
        posts = Post.objects.hidden()
        assert posts.count() == 1
        assert list(posts) == [self.hidden_post]

    def test_searchable(self):
        posts = Post.objects.searchable()
        assert posts.count() == 2
        # Note the ordering
        assert list(posts) == [self.hide_on_index_published_post, self.published_post]

    def test_index_manager_get_queryset(self):
        posts = Post.index.all()
        assert posts.count() == 1
        assert list(posts) == [self.published_post]


@pytest.mark.django_db
class TestCategoryModel:
    def test_auto_populate_title_from_name(self):
        category = CategoryFactory(title="", name="Test")
        assert category.title == category.name
