import os

from django.test import TestCase
from django.urls import reverse

from ..factories import CategoryFactory, PostFactory, TagFactory
from ..models import Category, Post, post_cover_path


class TagTestCase(TestCase):
    def setUp(self):
        self.tag = TagFactory()
        self.tag2 = TagFactory(name='another tag')

    def test_str(self):
        self.assertEqual(str(self.tag), 'tag')
        self.assertEqual(str(self.tag2), 'another tag')


class CategoryTestCase(TestCase):
    def setUp(self):
        self.category = CategoryFactory()
        self.titled_category = CategoryFactory(title='titled category')

    def test_str(self):
        self.assertEqual(str(self.category), 'category')

    def test_populate_title_from_name(self):
        self.assertEqual(self.category.title, 'category')
        self.assertEqual(self.titled_category.title, 'titled category')

    def test_get_absolute_url(self):
        self.assertEqual(self.category.get_absolute_url(),
                         reverse('blog:category_slug', kwargs={'slug': self.category.slug}))

    def test_total_views(self):
        self.assertEqual(self.category.total_views()['category_views'], 0)

        post1 = PostFactory(category=self.category, views=1000)
        post2 = PostFactory(category=self.category, views=1000)
        post3 = PostFactory(category=self.titled_category, views=1000)

        self.assertEqual(self.category.total_views()['category_views'], post1.views + post2.views)
        self.assertEqual(self.titled_category.total_views()['category_views'], post3.views)

    def test_last_modified(self):
        # TODO: find a way to override post modified_time for last_modified test
        self.assertIsNone(self.category.last_modified()['last_modified'])

        PostFactory(category=self.category)
        post2 = PostFactory(category=self.category)
        post3 = PostFactory(category=self.titled_category)

        self.assertEqual(self.category.last_modified()['last_modified'], post2.modified_time)
        self.assertEqual(self.titled_category.last_modified()['last_modified'],
                         post3.modified_time)


class PostTestCase(TestCase):
    def setUp(self):
        self.post = PostFactory()
        self.published_post = PostFactory(status=Post.STATUS_CHOICES.published)

    def test_post_cover_path(self):
        self.assertEqual(post_cover_path(self.post, 'cover.jpg'),
                         os.path.join('posts', str(self.post.pk), 'cover.jpg'))

    def test_str(self):
        self.assertEqual(str(self.post), 'post title')

    def test_excerpt_from_body(self):
        self.assertEqual(self.post.excerpt, 'post body')

    def test_set_pub_date(self):
        self.assertIsNone(self.post.pub_date)
        self.assertEqual(self.published_post.pub_date, self.published_post.created_time)

    def test_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(),
                         reverse('blog:detail', kwargs={'pk': self.post.pk}))

    def test_increase_views(self):
        self.assertEqual(self.post.views, 0)

        self.post.increase_views()
        self.assertEqual(self.post.views, 1)

        self.post.increase_views()
        self.assertEqual(self.post.views, 2)

    def test_word_count(self):
        self.assertEqual(self.post.word_count(), 9)

    def test_is_tutorial(self):
        tutorial_category = CategoryFactory(genre=Category.GENRE_CHOICES.tutorial)
        tutorial_category_post = PostFactory(category=tutorial_category)

        self.assertTrue(tutorial_category_post.is_tutorial())
        self.assertFalse(self.post.is_tutorial())

    def test_root_comments(self):
        # TODO
        pass
