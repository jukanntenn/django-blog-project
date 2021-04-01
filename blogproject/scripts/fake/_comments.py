import random

from blog.models import Post
from comments.tests.factories import BlogCommentFactory
from courses.models import Material
from django.contrib.sites.models import Site


def run():
    first_post = Post.index.all().order_by("-pinned", "-pub_date").first()
    site = Site.objects.get(name="example.com")
    for _ in range(30):
        root_comment = BlogCommentFactory(
            is_public=True, is_removed=False, site=site, content_object=first_post
        )
        children_size = random.randint(3, 10)
        for _ in range(children_size):
            root_comment = BlogCommentFactory(
                is_public=True,
                is_removed=False,
                site=site,
                content_object=first_post,
                parent=root_comment,
            )

    first_material = Material.index.all().order_by("-pub_date").first()
    for _ in range(30):
        root_comment = BlogCommentFactory(
            is_public=True, is_removed=False, site=site, content_object=first_material
        )
        children_size = random.randint(3, 10)
        for _ in range(children_size):
            root_comment = BlogCommentFactory(
                is_public=True,
                is_removed=False,
                site=site,
                content_object=first_material,
                parent=root_comment,
            )

    print("Comments created.")
