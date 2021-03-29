import random

from blog.models import Category
from blog.tests.factories import PostFactory
from users.models import User


def run():
    admin_user = User.objects.get(username="admin")
    for cate in Category.objects.all():
        size = random.randint(10, 20)
        PostFactory.create_batch(size, author=admin_user, category=cate)
    print("Posts created.")
