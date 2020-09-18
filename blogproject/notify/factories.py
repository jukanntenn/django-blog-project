import factory
from factory.django import DjangoModelFactory
from notifications.models import Notification
from users.tests.factories import UserFactory


class NotificationFactory(DjangoModelFactory):
    class Meta:
        model = Notification

    recipient = factory.SubFactory(UserFactory)
    actor = factory.SubFactory(UserFactory)
    verb = "notify"
