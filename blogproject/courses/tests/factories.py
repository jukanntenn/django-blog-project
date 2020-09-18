import factory
from courses.models import Category, Course, Material
from django.utils import timezone
from factory.django import DjangoModelFactory
from users.tests.factories import UserFactory


class CategoryFactory(DjangoModelFactory):

    name = factory.Faker("name")
    rank = factory.Sequence(lambda n: n)

    class Meta:
        model = Category


class CourseFactory(DjangoModelFactory):

    title = factory.Faker("sentence")
    slug = factory.Sequence(lambda n: f"course-slug-{n}")
    description = factory.Faker("paragraph")
    status = Course.STATUS.finished
    creator = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)
    rank = factory.Sequence(lambda n: n)

    class Meta:
        model = Course


class MaterialFactory(DjangoModelFactory):

    title = factory.Faker("sentence")
    body = factory.Faker("paragraph")
    status = Material.STATUS.published
    pub_date = factory.LazyFunction(timezone.now)
    author = factory.SubFactory(UserFactory)
    rank = factory.Sequence(lambda n: n)
    course = factory.SubFactory(CourseFactory)

    class Meta:
        model = Material
