import random

from courses.models import Course, Material
from courses.tests.factories import MaterialFactory
from users.models import User


def run():
    admin_user = User.objects.get(username="admin")
    for course in Course.objects.all():
        size = random.randint(10, 20)
        MaterialFactory.create_batch(size,author=admin_user, course=course)
    print("Materials created.")
