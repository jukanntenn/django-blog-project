import pytest
from constance import config
from django.conf import settings
from django.contrib.sites.models import Site
from django_dynamic_fixture import G
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from blog.models import Post
from notifications.models import Notification
from tl.testing.thread import ThreadJoiner
from users.models import User

from .factories import BlogCommentFactory


@pytest.mark.django_db
class TestNotification:
    def setup_method(self, method):
        self.moderator = User.objects.create_superuser(
            username="moderator",
            email="moderator@blogproject.test",
            password="12345678",
        )
        self.user = User.objects.create_user(
            username="test",
            email="test@blogproject.test",
            password="12345678",
            **{"email_bound": True},
        )
        self.other_user = User.objects.create_user(
            username="other",
            email="other@blogproject.test",
            password="12345678",
            **{"email_bound": True},
        )
        site = Site.objects.get(name="example.com")
        post = G(Post, author=self.moderator, body="正文")
        self.ct = str(post._meta)
        self.object_pk = post.pk
        self.client = APIClient()
        self.url = reverse("comment-list")
        self.moderator_comment = BlogCommentFactory(
            is_public=True,
            is_removed=False,
            site=site,
            content_object=post,
            user=self.moderator,
        )
        self.user_comment = BlogCommentFactory(
            is_public=True,
            is_removed=False,
            site=site,
            content_object=post,
            user=self.user,
        )
        self.other_user_comment = BlogCommentFactory(
            is_public=True,
            is_removed=False,
            site=site,
            content_object=post,
            user=self.other_user,
        )

    def test_moderator_comment_or_reply_self(self, mailoutbox):
        """博主自己评论或者回复自己，不发送任何通知"""
        response = self.client.get(
            reverse("comment-security-data"),
            data={"content_type": self.ct, "object_pk": self.object_pk},
        )
        security_data = response.data
        data = dict(**security_data, comment="test comment")
        token = Token.objects.get(user__username="moderator")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.post(self.url, data=data)
        assert response.status_code == 201
        assert Notification.objects.count() == 0
        assert len(mailoutbox) == 0

        data["parent"] = self.moderator_comment.pk
        response = self.client.post(self.url, data=data)
        assert response.status_code == 201
        assert Notification.objects.count() == 0
        assert len(mailoutbox) == 0

    def test_moderator_reply_other_user(self, mailoutbox):
        """博主回复，只通知被回复者"""
        response = self.client.get(
            reverse("comment-security-data"),
            data={"content_type": self.ct, "object_pk": self.object_pk},
        )
        security_data = response.data
        data = dict(**security_data, comment="test_moderator_reply_other_user")
        data["parent"] = self.user_comment.pk
        token = Token.objects.get(user__username="moderator")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        with ThreadJoiner(5):
            response = self.client.post(self.url, data=data)
        assert response.status_code == 201
        assert Notification.objects.count() == 1
        assert Notification.objects.all().get().recipient == self.user
        assert len(mailoutbox) == 1
        mail = mailoutbox[0]
        assert mail.subject == config.REPLY_EMAIL_SUBJECT
        assert mail.to == [self.user.email]

    def test_user_comment(self, mailoutbox):
        """用户评论，通知博主"""
        response = self.client.get(
            reverse("comment-security-data"),
            data={"content_type": self.ct, "object_pk": self.object_pk},
        )
        security_data = response.data
        data = dict(**security_data, comment="test_user_comment")
        token = Token.objects.get(user__username="test")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        with ThreadJoiner(5):
            response = self.client.post(self.url, data=data)
        assert response.status_code == 201
        assert Notification.objects.count() == 1
        assert Notification.objects.all().get().recipient == self.moderator
        assert len(mailoutbox) == 1
        mail = mailoutbox[0]
        assert mail.to == [admin[-1] for admin in settings.MANAGERS]

    def test_user_reply_other_user(self, mailoutbox):
        """用户回复，通知被回复者和博主"""
        response = self.client.get(
            reverse("comment-security-data"),
            data={"content_type": self.ct, "object_pk": self.object_pk},
        )
        security_data = response.data
        data = dict(**security_data, comment="test_user_reply_other_user")
        data["parent"] = self.other_user_comment.pk
        token = Token.objects.get(user__username="test")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.post(self.url, data=data)
        assert response.status_code == 201
        assert Notification.objects.filter(recipient=self.moderator).count() == 1
        assert Notification.objects.filter(recipient=self.other_user).count() == 1
        assert len(mailoutbox) == 2

    def test_user_reply_self(self, mailoutbox):
        """用户回复自己，仅通知博主"""
        response = self.client.get(
            reverse("comment-security-data"),
            data={"content_type": self.ct, "object_pk": self.object_pk},
        )
        security_data = response.data
        data = dict(**security_data, comment="test_user_reply_self")
        data["parent"] = self.user_comment.pk
        token = Token.objects.get(user__username="test")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        with ThreadJoiner(5):
            response = self.client.post(self.url, data=data)
        assert response.status_code == 201
        assert Notification.objects.count() == 1
        assert Notification.objects.all().get().recipient == self.moderator
        assert len(mailoutbox) == 1
        mail = mailoutbox[0]
        assert mail.to == [admin[-1] for admin in settings.MANAGERS]
