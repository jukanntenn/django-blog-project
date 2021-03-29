import factory
from blog.tests.factories import TagFactory
from favorites.tests.factories import IssueFactory


def run():
    # with factory.Faker.override_default_locale("zh_CN"):
    # IssueFactory.create_batch(40, tags=[TagFactory(), TagFactory()])
    print("Issues created!")
