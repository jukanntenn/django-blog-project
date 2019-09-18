from notifications.models import Notification
from test_plus import TestCase

from blog.factories import PostFactory

from ..factories import BlogCommentFactory
from ..moderation import BlogCommentModerator


class BlogCommentModeratorTestCase(TestCase):
    def setUp(self):
        self.author = self.make_user(username='author')
        self.commenter = self.make_user(username='commenter')
        self.post = PostFactory(author=self.author)

    def test_comment_post_notify_author(self):
        comment = BlogCommentFactory(user=self.commenter)
        moderator = BlogCommentModerator(model=self.post)
        moderator.reply(comment, self.post, None)
        self.assertEqual(Notification.objects.count(), 1)

    def test_comment_post_by_author(self):
        comment = BlogCommentFactory(user=self.author)
        moderator = BlogCommentModerator(model=self.post)
        moderator.reply(comment, self.post, None)
        self.assertEqual(Notification.objects.count(), 0)

    def test_reply_by_other_notify_commenter(self):
        parent_comment = BlogCommentFactory(user=self.commenter)
        other_user = self.make_user(username='otheruser')
        child_comment = BlogCommentFactory(user=other_user, parent=parent_comment)

        moderator = BlogCommentModerator(model=self.post)
        moderator.reply(child_comment, self.post, None)
        self.assertEqual(Notification.objects.count(), 2)

    def test_reply_by_author_notify_commenter(self):
        parent_comment = BlogCommentFactory(user=self.commenter)
        child_comment = BlogCommentFactory(user=self.author, parent=parent_comment)

        moderator = BlogCommentModerator(model=self.post)
        moderator.reply(child_comment, self.post, None)
        self.assertEqual(Notification.objects.count(), 1)

    def test_reply_self(self):
        parent_comment = BlogCommentFactory(user=self.author)
        child_comment = BlogCommentFactory(user=self.author, parent=parent_comment)

        moderator = BlogCommentModerator(model=self.post)
        moderator.reply(child_comment, self.post, None)
        self.assertEqual(Notification.objects.count(), 0)
