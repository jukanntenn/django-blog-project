from django.core import mail
from test_plus.test import TestCase


class SubscriptionCreateViewTestCase(TestCase):
    def setUp(self) -> None:
        pass

    def test_subscribe(self):
        response = self.post(
            "newsletters:subscription", data={"email": "test@example.com"}, follow=True
        )
        self.response_200(response)
        self.assertEqual(len(mail.outbox), 1)
