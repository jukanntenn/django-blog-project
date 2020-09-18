import factory
from core.tests.models import Entry, RankableEntry
from factory.django import DjangoModelFactory
from users.tests.factories import UserFactory


class EntryFactory(DjangoModelFactory):
    title = factory.Faker("sentence")
    body = factory.Faker("paragraph")
    brief = factory.Faker("sentence")
    author = factory.SubFactory(UserFactory)

    class Meta:
        model = Entry


class RankableEntryFactory(EntryFactory):
    rank = factory.Sequence(lambda n: n)

    class Meta:
        model = RankableEntry
