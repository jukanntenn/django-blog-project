import pytest
from django.contrib.sites.models import Site
from django_dynamic_fixture import G

from blog.models import Post
from comments.forms import BlogCommentForm
from comments.models import BlogComment
from users.models import User

from .factories import BlogCommentFactory


@pytest.mark.django_db
class TestBlogCommentForm:
    def setup_method(self, method):
        user = G(User)
        site = Site.objects.get(name="example.com")
        post = G(Post, author=user, body="正文")
        self.comment = BlogCommentFactory(
            is_public=True, is_removed=False, site=site, content_object=post
        )
        form = BlogCommentForm(target_object=post, parent=self.comment)
        self.bound_form = BlogCommentForm(
            target_object=post,
            parent=self.comment,
            data=dict(**form.initial, comment="test comment"),
        )

    def test_get_comment_model(self):
        assert self.bound_form.get_comment_model() == BlogComment

    def test_get_comment_create_data(self):
        assert self.bound_form.is_valid(), self.bound_form.errors
        comment_create_data = self.bound_form.get_comment_create_data()
        assert comment_create_data["parent_id"] == self.comment.pk
