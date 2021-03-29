from courses.models import Category
from courses.tests.factories import CourseFactory
from users.models import User


def run():
    categories = Category.objects.all()
    admin_user = User.objects.get(username="admin")
    for cate in categories:
        CourseFactory(category=cate, creator=admin_user)
    print("Courses created.")
