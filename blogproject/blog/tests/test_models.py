from datetime import timedelta

import pytest
from blog.models import Post
from django.utils import timezone
from django_dynamic_fixture import G


@pytest.fixture
def post():
    return G(Post, body='正文')


@pytest.mark.django_db
class TestPost:
    def test_populate_excerpt(self):
        post = G(Post, body='正文' * 100, ignore_fields=['excerpt'])
        assert len(post.excerpt) == 150

        post = G(Post, body='正文' * 100, excerpt='摘要')
        assert post.excerpt == '摘要'

    def test_populate_pub_date(self):
        post = G(Post, status=Post.STATUS_CHOICES.draft, fill_nullable_fields=False)
        assert post.pub_date is None

        after_3_days = timezone.now() + timedelta(days=3)
        post = G(Post, status=Post.STATUS_CHOICES.published, pub_date=after_3_days)
        assert post.pub_date == after_3_days

        post = G(Post, status=Post.STATUS_CHOICES.published, fill_nullable_fields=False)
        assert post.pub_date == post.created

    def test_type_property(self, post):
        assert post.type == 'p'

    def test_get_absolute_url(self, post):
        assert post.get_absolute_url() == f'/post/{post.pk}/'


@pytest.mark.django_db
class TestPostQuerySetAndIndexManager:
    def setup_method(self):
        after_3_days = timezone.now() + timedelta(days=3)

        self.published_post = G(Post, status=Post.STATUS_CHOICES.published, show_on_index=True,
                                ignore_fields=['pub_date'])
        self.draft_post = G(Post, status=Post.STATUS_CHOICES.draft, show_on_index=True, ignore_fields=['pub_date'])
        self.hidden_post = G(Post, status=Post.STATUS_CHOICES.hidden, show_on_index=True, ignore_fields=['pub_date'])
        self.future_publishing_post = G(Post, status=Post.STATUS_CHOICES.published, show_on_index=True,
                                        pub_date=after_3_days)
        self.future_draft_post = G(Post, status=Post.STATUS_CHOICES.draft, show_on_index=True,
                                   pub_date=after_3_days)
        self.hide_on_index_published_post = G(Post, status=Post.STATUS_CHOICES.published, show_on_index=False,
                                              ignore_fields=['pub_date'])

    def test_published(self):
        posts = Post.objects.published()
        assert posts.count() == 3
        # Note the ordering
        assert list(posts) == [self.future_publishing_post, self.hide_on_index_published_post, self.published_post]

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
