from test_plus import TestCase

from ..factories import BlogCommentFactory


class BlogCommentTestCase(TestCase):
    def test_get_descendants_reversely(self):
        parent = BlogCommentFactory()
        descendants = BlogCommentFactory.create_batch(10, parent=parent)
        self.assertEqual(parent.get_descendants_reversely().count(), 10)
        self.assertQuerysetEqual(parent.get_descendants_reversely(), map(repr, descendants))
