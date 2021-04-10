from favorites.models import Issue
from favorites.tests.factories import FavoriteFactory
from tags.tests.factories import TagFactory


def run():
    for issue in Issue.objects.all():
        FavoriteFactory.create_batch(5, issue=issue, tags=[TagFactory(), TagFactory()])
    print("Favorites created!")
