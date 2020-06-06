import factory
from blog.models import Tag
from factory.django import DjangoModelFactory


class TagFactory(DjangoModelFactory):
    name = factory.Faker("word")

    class Meta:
        model = Tag
