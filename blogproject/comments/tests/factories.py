from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

import factory
from comments.models import BlogComment
from factory.django import DjangoModelFactory
from users.tests.factories import UserFactory


class BlogCommentFactory(DjangoModelFactory):

    object_pk = factory.SelfAttribute("content_object.id")
    content_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.content_object)
    )
    user = factory.SubFactory(UserFactory)
    comment = factory.Faker("sentence")
    submit_date = factory.LazyFunction(timezone.now)

    class Meta:
        model = BlogComment
