from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from test_plus import TestCase

from notify.context_processors import notification_count

from .factories import NotificationFactory


class NotificationUtilsTestCase(TestCase):
    def setUp(self):
        # request conflicts with request method of test_plus TestCase
        self.req = RequestFactory().get('/')
        self.user = self.make_user()

    def test_anonymous_user(self):
        anonymous_user = AnonymousUser()
        self.req.user = anonymous_user
        result = notification_count(self.req)
        self.assertDictEqual(result, {'unread_count': None})

    def test_authenticated_user_does_not_have_notifications_unread(self):
        self.login(self.user)
        self.req.user = self.user
        result = notification_count(self.req)
        self.assertDictEqual(result, {'unread_count': 0})

    def test_authenticated_user_has_notifications_unread(self):
        NotificationFactory.create_batch(3, recipient=self.user)
        self.login(self.user)
        self.req.user = self.user
        result = notification_count(self.req)
        self.assertDictEqual(result, {'unread_count': 3})
