import pytest
from blog.models import Post
from blog.tests.factories import PostFactory
from comments.models import BlogComment
from django.contrib.sites.models import Site
from django_dynamic_fixture import G
from users.models import User

from .factories import BlogCommentFactory


@pytest.mark.django_db
def test_smoke(site):
    assert site.name == "example.com"


@pytest.mark.django_db
class TestBlogCommentQuerySet:
    def setup_method(self):
        site = Site.objects.get(name="example.com")
        post = PostFactory()
        self.visible_root_comment = BlogCommentFactory(
            is_public=True, is_removed=False, site=site, content_object=post
        )
        self.visible_child_comment = BlogCommentFactory(
            is_public=True,
            is_removed=False,
            parent=self.visible_root_comment,
            site=site,
            content_object=post,
        )

    def test_visible(self, site, post):
        BlogCommentFactory(
            is_public=False, is_removed=False, site=site, content_object=post
        )
        BlogCommentFactory(
            is_public=True, is_removed=True, site=site, content_object=post
        )
        BlogCommentFactory(
            is_public=False, is_removed=True, site=site, content_object=post
        )

        qs = BlogComment.objects.visible()
        assert qs.count() == 2
        assert list(qs) == [self.visible_root_comment, self.visible_child_comment]

    def test_roots(self):
        qs = BlogComment.objects.roots()
        assert qs.count() == 1
        assert qs[0] == self.visible_root_comment
