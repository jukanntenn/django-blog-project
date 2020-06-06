from django.utils import timezone

import factory
from factory.django import DjangoModelFactory
from favorites.models import Favorite, Issue
from users.tests.factories import UserFactory


class IssueFactory(DjangoModelFactory):
    number = factory.Sequence(lambda n: n)
    pub_date = factory.LazyFunction(timezone.now)
    description = factory.Faker("paragraph")
    creator = factory.SubFactory(UserFactory)

    class Meta:
        model = Issue

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for tag in extracted:
                self.tags.add(tag)


class FavoriteFactory(DjangoModelFactory):
    issue = factory.SubFactory(IssueFactory)
    title = factory.Faker("sentence")
    description = factory.Faker("paragraph")
    url = factory.Faker("uri")
    rank = factory.Sequence(lambda n: n)

    class Meta:
        model = Favorite

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for tag in extracted:
                self.tags.add(tag)
