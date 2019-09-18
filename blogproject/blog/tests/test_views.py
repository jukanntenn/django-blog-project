from django.test import RequestFactory
from test_plus.test import CBVTestCase, TestCase

from .. import views
from ..factories import CategoryFactory, PostFactory
from ..models import Category, Post


class BasePostListViewCBVTestCase(CBVTestCase):
    def test_get_queryset(self):
        PostFactory.create_batch(10)
        view = self.get_instance(views.BasePostListView)
        posts = view.get_queryset()

        self.assertEqual(posts.count(), 10)
        self.assertTrue(hasattr(posts[0], 'comment_count'))

    def test_get_queryset_num_queries(self):
        PostFactory.create_batch(10)
        view = self.get_instance(views.BasePostListView)

        with self.assertNumQueries(1):
            len(view.get_queryset())


class IndexViewTestCase(TestCase):
    def test_template_used(self):
        self.get('blog:index')
        response = self.response_200()
        self.assertTemplateUsed(response, 'blog/index.html')

    def test_good_view(self):
        """http://django-test-plus.readthedocs.io/en/latest/low_query_counts.html#assertgoodview-url-name-args-kwargs
        """
        self.assertGoodView('blog:index')


class PopularPostListViewTestCase(TestCase):
    def test_template_used(self):
        self.get('blog:popular')
        response = self.response_200()
        self.assertTemplateUsed(response, 'blog/index.html')

    def test_good_view(self):
        """http://django-test-plus.readthedocs.io/en/latest/low_query_counts.html#assertgoodview-url-name-args-kwargs
        """
        self.assertGoodView('blog:index')


class PopularPostListViewCBVTestCase(CBVTestCase):
    def test_get_queryset(self):
        PostFactory.create_batch(10)
        view = self.get_instance(views.BasePostListView)
        posts = view.get_queryset()

        # https://stackoverflow.com/questions/16058571/comparing-querysets-in-django-testcase
        self.assertQuerysetEqual(Post.objects.all().reverse(), map(repr, posts))


class CategoryPostListViewTestCase(TestCase):
    def setUp(self):
        self.category = CategoryFactory()

    def test_template_used(self):
        self.get('blog:category_slug', slug=self.category.slug)
        self.response_200()
        self.assertTemplateUsed(self.last_response, 'blog/category_post_list.html')

    def test_tutorial_category_template_used(self):
        tutorial_category = CategoryFactory(genre=Category.GENRE_CHOICES.tutorial)
        self.get('blog:category_slug', slug=tutorial_category.slug)
        self.assertTemplateUsed(self.last_response, 'blog/tutorial_detail.html')
        self.assertContext('is_paginated', False)

    def test_good_views(self):
        """http://django-test-plus.readthedocs.io/en/latest/low_query_counts.html#assertgoodview-url-name-args-kwargs
        """
        self.assertGoodView('blog:category_slug', slug=self.category.slug)

    def test_redirect_pk_url_to_slug_url(self):
        self.get('blog:category', pk=self.category.pk)
        self.response_301()

        self.get('blog:category', pk='does not exist pk')
        self.response_404()

    def test_404(self):
        self.get('blog:category_slug', slug='dose not exist slug')
        self.response_404()


class CategoryPostListViewCBVTestCase(CBVTestCase):
    def setUp(self):
        self.category = CategoryFactory(genre=Category.GENRE_CHOICES.tutorial)
        self.req = RequestFactory().get(
            self.reverse('blog:category_slug', slug=self.category.slug)
        )
        self.req.user = self.make_user()

    def test_dispatch(self):
        view = self.get_instance(views.CategoryPostListView, slug=self.category.slug, request=self.req)
        view.dispatch(self.req, )
        self.assertEqual(view.category, self.category)
        self.assertEqual(view.template_name, 'blog/tutorial_detail.html')
        self.assertIsNone(view.paginate_by)

    def test_get_queryset(self):
        PostFactory()
        post = PostFactory(category=self.category)
        view = self.get_instance(views.CategoryPostListView, slug=self.category.slug, request=self.req)
        view.dispatch(self.req)
        self.assertQuerysetEqual(view.get_queryset(), [repr(post)])

    def test_context_data(self):
        post_list = [PostFactory(category=self.category), PostFactory(category=self.category)]
        view = self.get_instance(views.CategoryPostListView,
                                 initkwargs={'object_list': post_list},
                                 request=self.req,
                                 slug=self.category.slug
                                 )
        view.dispatch(self.req)
        context = view.get_context_data()
        self.assertEqual(context['category'], self.category)


class PostDetailViewTestCase(TestCase):
    def setUp(self):
        self.first_post = PostFactory(body='**body**')

    def test_template_used(self):
        self.get('blog:detail', pk=self.first_post.pk)
        self.response_200()
        self.assertTemplateUsed(self.last_response, 'blog/detail.html')

    def test_good_views(self):
        """http://django-test-plus.readthedocs.io/en/latest/low_query_counts.html#assertgoodview-url-name-args-kwargs
        """
        self.assertGoodView('blog:detail', pk=self.first_post.pk)

    def test_404(self):
        self.get('blog:detail', pk=self.first_post.pk)
        self.response_200()

        self.get('blog:detail', pk=2)
        self.response_404()
        self.get('blog:detail', pk='a')
        self.response_404()

    def test_increase_post_views(self):
        self.get('blog:detail', pk=self.first_post.pk)
        self.first_post.refresh_from_db()
        self.assertEqual(self.first_post.views, 1)

        self.get('blog:detail', pk=self.first_post.pk)
        self.first_post.refresh_from_db()
        self.assertEqual(self.first_post.views, 2)

    def test_previous_post(self):
        self.get('blog:detail', pk=self.first_post.pk)
        self.assertContext('previous_post', None)

        second_post = PostFactory()
        self.get('blog:detail', pk=second_post.pk)
        self.assertContext('previous_post', self.first_post)

    def test_next_post(self):
        self.get('blog:detail', pk=self.first_post.pk)
        self.assertContext('next_post', None)

        second_post = PostFactory()
        self.get('blog:detail', pk=self.first_post.pk)
        self.assertContext('next_post', second_post)

    def test_mark_post(self):
        self.get('blog:detail', pk=self.first_post.pk)
        self.assertHTMLEqual(self.context['post'].body, "<p><strong>body</strong></p>")

    def test_context(self):
        self.get('blog:detail', pk=self.first_post.pk)
        self.assertContext('post', self.first_post)
        self.assertInContext('previous_post')
        self.assertInContext('next_post')


class TutorialListViewTestCase(TestCase):
    def test_template_used(self):
        self.get('blog:tutorials')
        self.response_200()
        self.assertTemplateUsed(self.last_response, 'blog/tutorial_list.html')

    def test_good_views(self):
        """http://django-test-plus.readthedocs.io/en/latest/low_query_counts.html#assertgoodview-url-name-args-kwargs
        """
        self.assertGoodView('blog:tutorials')


class CategorylListViewTestCase(TestCase):
    def test_template_used(self):
        self.get('blog:categories')
        self.response_200()
        self.assertTemplateUsed(self.last_response, 'blog/category_list.html')

    def test_good_views(self):
        """http://django-test-plus.readthedocs.io/en/latest/low_query_counts.html#assertgoodview-url-name-args-kwargs
        """
        self.assertGoodView('blog:categories')


class PostArchivesViewTestCase(TestCase):
    def test_template_used(self):
        self.get('blog:archives')
        self.response_200()
        self.assertTemplateUsed(self.last_response, 'blog/archives.html')

    def test_good_views(self):
        """http://django-test-plus.readthedocs.io/en/latest/low_query_counts.html#assertgoodview-url-name-args-kwargs
        """
        self.assertGoodView('blog:archives')
