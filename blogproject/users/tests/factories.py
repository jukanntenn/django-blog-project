from typing import Any, Sequence

import factory
from django.utils.crypto import get_random_string
from factory import Faker, post_generation
from factory.django import DjangoModelFactory
from users.models import User


class UserFactory(DjangoModelFactory):
    username = Faker("user_name")
    name = factory.lazy_attribute(lambda o: o.username.lower())
    email = Faker("email")

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = get_random_string()
        self.set_password(password)

    class Meta:
        model = User
        django_get_or_create = ("username",)
