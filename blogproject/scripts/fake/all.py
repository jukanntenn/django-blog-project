from django.db import transaction

from . import (
    _clean_db,
    _comments,
    _course_categories,
    _courses,
    _favorites,
    _issues,
    _materials,
    _post_categories,
    _posts,
    _superuser,
)


def run():
    with transaction.atomic():
        _clean_db.run()
        _superuser.run()
        _post_categories.run()
        _posts.run()
        _course_categories.run()
        _courses.run()
        _materials.run()
        _comments.run()
        _issues.run()
        _favorites.run()
        print("Done!")
