import pytest
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django_dynamic_fixture import G
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from blog.models import Post
from comments.models import BlogComment
from users.models import User

from .factories import BlogCommentFactory


@pytest.mark.django_db
class TestCommentViewSet:
    def setup_method(self):
        self.user = User.objects.create_superuser(
            username="test", email="test@blogproject.test", password="12345678"
        )
        site = Site.objects.get(name="example.com")
        post = G(Post, author=self.user, body="正文")
        self.ct = str(post._meta)
        self.object_pk = post.pk
        self.client = APIClient()
        self.root_comment_a = BlogCommentFactory(
            is_public=True, is_removed=False, site=site, content_object=post
        )
        self.root_comment_b = BlogCommentFactory(
            is_public=True, is_removed=False, site=site, content_object=post
        )
        self.child_comment_b = BlogCommentFactory(
            is_public=True,
            is_removed=False,
            site=site,
            content_object=post,
            parent=self.root_comment_b,
        )
        self.root_comment_c = BlogCommentFactory(
            is_public=True, is_removed=False, site=site, content_object=post
        )
        self.child_comment_c = BlogCommentFactory(
            is_public=True,
            is_removed=False,
            site=site,
            content_object=post,
            parent=self.root_comment_c,
        )
        self.grandchild_comment_c = BlogCommentFactory(
            is_public=True,
            is_removed=False,
            site=site,
            content_object=post,
            parent=self.child_comment_c,
        )

    def test_invalid_target(self):
        # list comments
        url = reverse("comment-list")

        # Missing content_type or object_pk
        response = self.client.get(url, data={"object_pk": self.object_pk})
        assert response.status_code == 400
        response = self.client.get(url, data={"content_type": self.ct})
        assert response.status_code == 400

        # Invalid content_type value
        response = self.client.get(
            url, data={"content_type": "invalid content type value"}
        )
        assert response.status_code == 400
        response = self.client.get(url, data={"content_type": "invalid.model"})
        assert response.status_code == 400

        # Target object does not exist
        response = self.client.get(
            url, data={"content_type": self.ct, "object_ok": 99999}
        )
        assert response.status_code == 400

        # post comment
        token = Token.objects.get(user__username="test")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.post(url, data={"object_pk": self.object_pk})
        assert response.status_code == 400
        response = self.client.post(url, data={"content_type": self.ct})
        assert response.status_code == 400

        # Invalid content_type value
        response = self.client.post(
            url, data={"content_type": "invalid content type value"}
        )
        assert response.status_code == 400
        response = self.client.post(url, data={"content_type": "invalid.model"})
        assert response.status_code == 400

        # Target object does not exist
        response = self.client.post(
            url, data={"content_type": self.ct, "object_ok": 99999}
        )
        assert response.status_code == 400

    def test_security_data(self):
        url = reverse("comment-security-data")
        response = self.client.get(
            url, data={"content_type": self.ct, "object_pk": self.object_pk}
        )
        assert response.status_code == 200
        assert response.data["content_type"] == self.ct
        assert response.data["object_pk"] == str(self.object_pk)
        assert "timestamp" in response.data
        assert "security_hash" in response.data

    def test_list_comments(self):
        url = reverse("comment-list")
        response = self.client.get(
            url, data={"content_type": self.ct, "object_pk": self.object_pk}
        )
        assert len(response.data["results"]) == 3
        results = response.data["results"]
        assert results[0]["id"] == self.root_comment_c.pk
        assert [c["id"] for c in results[0]["descendants"]] == [
            self.child_comment_c.pk,
            self.grandchild_comment_c.pk,
        ]
        assert results[1]["id"] == self.root_comment_b.pk
        assert [c["id"] for c in results[1]["descendants"]] == [
            self.child_comment_b.pk,
        ]
        assert results[2]["id"] == self.root_comment_a.pk
        assert results[2]["descendants"] == []

    def test_only_authenticated_user_can_post_comment(self):
        url = reverse("comment-list")
        response = self.client.get(
            reverse("comment-security-data"),
            data={"content_type": self.ct, "object_pk": self.object_pk},
        )
        security_data = response.data
        data = dict(**security_data, comment="test comment")
        response = self.client.post(url, data=data)
        assert response.status_code == 401

    def test_post_comment_with_insecure_data(self):
        data = {
            "content_type": self.ct,
            "object_pk": self.object_pk,
            "timestamp": "1582344806",
            "security_hash": "xxd324cea7043442cbeb455e8e5fb1bedd3f0e00",
            "comment": "test comment",
        }
        url = reverse("comment-list")
        token = Token.objects.get(user__username="test")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.post(url, data=data)
        assert response.status_code == 400
        assert "failed security verification" in response.json()["detail"]

    def test_post_comment_with_invalid_data(self):
        url = reverse("comment-list")
        response = self.client.get(
            reverse("comment-security-data"),
            data={"content_type": self.ct, "object_pk": self.object_pk},
        )
        security_data = response.data
        data = dict(**security_data)
        token = Token.objects.get(user__username="test")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.post(url, data=data)
        assert response.status_code == 400

    def test_post_comment_with_valid_data_but_killed(self):
        pass

    def test_post_comment_with_valid_data(self):
        url = reverse("comment-list")
        response = self.client.get(
            reverse("comment-security-data"),
            data={"content_type": self.ct, "object_pk": self.object_pk},
        )
        security_data = response.data
        data = dict(**security_data, comment="test comment")
        token = Token.objects.get(user__username="test")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.post(url, data=data)
        assert response.status_code == 201
        assert response.json()["comment_html"] == "<p>test comment</p>"

    def test_remove_comment(self):
        pass

    def test_edit_comment(self):
        pass

    def test_highlight_comment(self):
        pass

    def test_moderate_comment(self):
        pass
