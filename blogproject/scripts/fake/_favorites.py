import factory
from blog.tests.factories import TagFactory
from favorites.models import Favorite, Issue
from favorites.tests.factories import FavoriteFactory


def run():
    print("Creating favorites...")
    with factory.Faker.override_default_locale("zh_CN"):
        for issue in Issue.objects.all():
            FavoriteFactory.create_batch(
                5, issue=issue, tags=[TagFactory(), TagFactory()]
            )
    print("Favorites creation done!")
