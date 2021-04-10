from favorites.tests.factories import IssueFactory
from tags.tests.factories import TagFactory


def run():
    IssueFactory.create_batch(40, tags=[TagFactory(), TagFactory()])
    print("Issues created!")
