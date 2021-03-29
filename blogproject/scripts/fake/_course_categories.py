from courses.tests.factories import CategoryFactory


def run():
    CategoryFactory.create_batch(3)
    print("Course categories created.")
