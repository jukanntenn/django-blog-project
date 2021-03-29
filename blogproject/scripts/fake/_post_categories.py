from blog.tests.factories import CategoryFactory
from users.models import User


def run():
    admin_user = User.objects.get(username="admin")
    CategoryFactory.create_batch(10, creator=admin_user)
    print("Post categories created.")
