import factory
from blog.models import Category, Post, Tag
from factory.django import DjangoModelFactory
from users.tests.factories import UserFactory


class PostFactory(DjangoModelFactory):
    title = factory.Faker("sentence")
    body = factory.Faker("paragraph")
    brief = factory.Faker("sentence")
    status = Post.STATUS_CHOICES.published
    author = factory.SubFactory(UserFactory)

    class Meta:
        model = Post


class CategoryFactory(DjangoModelFactory):
    name = factory.Faker("word")
    slug = factory.LazyAttribute(lambda c: c.name)
    creator = factory.SubFactory(UserFactory)

    class Meta:
        model = Category


class TagFactory(DjangoModelFactory):
    name = factory.Faker("word")

    class Meta:
        model = Tag
