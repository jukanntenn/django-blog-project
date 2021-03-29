from alerts.models import Alert
from blog.models import Category as PostCategory
from blog.models import Post
from comments.models import BlogComment
from courses.models import Category as CourseCategory
from courses.models import Course, Material
from django.conf import settings
from django.contrib.auth import get_user_model
from favorites.models import Favorite, Issue
from friendlinks.models import FriendLink
from newsletters.models import Subscription
from users.models import User

User = get_user_model()


def run():
    if not settings.DEBUG:
        warning_msg = (
            "You are not in development environment. "
            "This script will DELETE ALL DATA in your database. "
            "If you really want to continue this script, please input 'yEs'. "
            "Make sure you know what you are doing!"
        )
        print(warning_msg)
        prompt = input("Please input 'yEs' to continue")
        if prompt != "yEs":
            print("Unexpected input, return!")
            return

    User.objects.all().delete()
    PostCategory.objects.all().delete()
    Post.objects.all().delete()
    CourseCategory.objects.all().delete()
    Course.objects.all().delete()
    Material.objects.all().delete()
    Issue.objects.all().delete()
    Favorite.objects.all().delete()
    FriendLink.objects.all().delete()
    Subscription.objects.all().delete()
    print("Database cleaned.")
