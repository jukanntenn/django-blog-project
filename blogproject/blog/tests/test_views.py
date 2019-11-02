import pytest
from blog.models import Category, Post
from blog.views import BlogSearchView
from courses.models import Material
from django.test import TestCase
from django.urls import reverse
from django_dynamic_fixture import G
from pure_pagination.paginator import Paginator


def test_auto_set_admin_as_post_author(admin_client, admin_user):
    url = reverse('admin:blog_post_add')
    data = {
        'title': '测试标题',
        'body': '测试内容',
        'status': Post.STATUS_CHOICES.published,
    }
    response = admin_client.post(url, data=data)
    assert response.status_code == 302

    assert Post.objects.count() == 1
    post = Post.objects.all().latest('created')
    assert post.author == admin_user


class IndexViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse('blog:index')

    def test_good_view(self):
        response = self.client.get(self.url)
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'blog/index.html')

    def test_entries_display(self):
        pinned_post = G(Post, pinned=True, show_on_index=True, status=Post.STATUS_CHOICES.published)
        material = G(Material, show_on_index=True, status=Material.STATUS.published)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '[置顶] ' + pinned_post.title)
        self.assertContains(response, pinned_post.brief)

        self.assertContains(response, material.title)
        self.assertContains(response, '系列教程')


class PostDetailViewTestCase(TestCase):
    def setUp(self):
        self.index_post = G(Post, show_on_index=True, status=Post.STATUS_CHOICES.published)
        self.not_index_post = G(Post, show_on_index=False, status=Post.STATUS_CHOICES.published, category=None)
        self.draft_post = G(Post, show_on_index=True, status=Post.STATUS_CHOICES.draft)

    def test_good_view(self):
        url = self.index_post.get_absolute_url()

        response = self.client.get(url)
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'blog/detail.html')
        self.assertIn('num_comments', response.context_data)
        self.assertIn('num_comment_participants', response.context_data)

    def test_only_public_posts_are_available(self):
        available_url1 = self.index_post.get_absolute_url()
        available_url2 = self.not_index_post.get_absolute_url()
        unavailable_url = self.draft_post.get_absolute_url()

        response = self.client.get(available_url1)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(available_url2)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(unavailable_url)
        self.assertEqual(response.status_code, 404)

    def test_headline(self):
        category_post_url = self.index_post.get_absolute_url()
        no_category_post_url = self.not_index_post.get_absolute_url()

        response = self.client.get(category_post_url)
        self.assertContains(response, '%s_%s' % (self.index_post.title, self.index_post.category))

        response = self.client.get(no_category_post_url)
        self.assertContains(response, '%s' % (self.not_index_post.title,))


class CategoryViewTestCase(TestCase):
    def setUp(self):
        self.category = G(Category)
        self.category_post1 = G(Post, title='Category Post1', show_on_index=True, status=Post.STATUS_CHOICES.published,
                                category=self.category)
        self.category_post2 = G(Post, title='Category Post2', show_on_index=True, status=Post.STATUS_CHOICES.published,
                                category=self.category)
        self.no_category_post = G(Post, title='No Category Post', show_on_index=False,
                                  status=Post.STATUS_CHOICES.published, category=None)

    def test_good_view(self):
        url = self.category.get_absolute_url()

        response = self.client.get(url)
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'blog/category.html')
        self.assertIn('entry_list', response.context_data)

    def test_category_posts(self):
        url = self.category.get_absolute_url()
        response = self.client.get(url)
        assert response.status_code == 200
        self.assertContains(response, self.category_post1.title)
        self.assertContains(response, self.category_post2.title)
        self.assertNotContains(response, self.no_category_post.title)

    def test_headline(self):
        url = self.category.get_absolute_url()
        response = self.client.get(url)
        self.assertContains(response, '%s' % (self.category,))


class CategoryListViewTestCase(TestCase):
    def setUp(self):
        self.category1 = G(Category, name='cate1')
        self.category2 = G(Category, name='cate2')
        self.post = G(Post, title='Post', show_on_index=True, status=Post.STATUS_CHOICES.published,
                      category=self.category1)

    def test_good_view(self):
        url = reverse('blog:categories')
        response = self.client.get(url)
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'blog/category_list.html')

    def test_categories(self):
        url = reverse('blog:categories')
        response = self.client.get(url)

        self.assertContains(response, self.category1)
        self.assertContains(response, self.category2)
        self.assertContains(response, f'{self.category1}（1）')
        self.assertContains(response, f'{self.category2}（0）')


class PostArchivesViewTestCase(TestCase):
    def test_good_view(self):
        url = reverse('blog:archives')
        response = self.client.get(url)
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'blog/archives.html')


class DonateViewTestCase(TestCase):
    def test_good_view(self):
        url = reverse('blog:donate')
        response = self.client.get(url)
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'blog/donate.html')


@pytest.mark.django_db
def test_blog_search_view_paginator(rf):
    url = reverse('blog:search')
    request = rf.get(url)
    view = BlogSearchView()
    view.request = request
    paginator, page = view.build_page()
    assert isinstance(paginator, Paginator)
