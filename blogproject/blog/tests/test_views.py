import pytest
from blog.models import Category, Post
from blog.tests.factories import CategoryFactory as PostCategoryFactory
from blog.tests.factories import PostFactory
from blog.views import BlogSearchView
from courses.models import Category as CourseCategory
from courses.models import Course, Material
from courses.tests.factories import CategoryFactory as CourseCategoryFactory
from courses.tests.factories import CourseFactory, MaterialFactory
from django.http.response import Http404
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django_dynamic_fixture import G
from pure_pagination.paginator import Paginator
from users.models import User


def test_auto_set_admin_as_post_author(admin_client, admin_user):
    url = reverse("admin:blog_post_add")
    data = {
        "title": "测试标题",
        "body": "测试内容",
        "status": Post.STATUS_CHOICES.published,
    }
    response = admin_client.post(url, data=data)
    assert response.status_code == 302

    assert Post.objects.count() == 1
    post = Post.objects.all().latest("created")
    assert post.author == admin_user


class IndexViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse("blog:index")

    def test_good_view(self):
        response = self.client.get(self.url)
        assert response.status_code == 200
        self.assertTemplateUsed(response, "blog/index.html")

    def test_entries_display(self):
        course = CourseFactory()
        pinned_post = PostFactory(
            pinned=True,
            show_on_index=True,
            status=Post.STATUS_CHOICES.published,
        )
        material = MaterialFactory(
            course=course,
            show_on_index=True,
            status=Material.STATUS.published,
            pub_date=timezone.now(),
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "[置顶] " + pinned_post.title)
        self.assertContains(response, pinned_post.brief)

        self.assertContains(response, material.title)
        self.assertContains(response, "系列教程")


class PostDetailViewTestCase(TestCase):
    def setUp(self):
        category = PostCategoryFactory()
        self.index_post = PostFactory(
            show_on_index=True,
            status=Post.STATUS_CHOICES.published,
            category=category,
        )
        self.not_index_post = PostFactory(
            show_on_index=False,
            status=Post.STATUS_CHOICES.published,
            category=None,
        )
        self.draft_post = PostFactory(
            show_on_index=True, status=Post.STATUS_CHOICES.draft
        )

    def test_good_view(self):
        url = self.index_post.get_absolute_url()

        response = self.client.get(url)
        assert response.status_code == 200
        self.assertTemplateUsed(response, "blog/detail.html")
        self.assertIn("num_comments", response.context_data)
        self.assertIn("num_comment_participants", response.context_data)

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
        self.assertContains(
            response, "%s_%s" % (self.index_post.title, self.index_post.category)
        )

        response = self.client.get(no_category_post_url)
        self.assertContains(response, "%s" % (self.not_index_post.title,))


class CategoryViewTestCase(TestCase):
    def setUp(self):
        self.category = PostCategoryFactory()
        self.category_post1 = PostFactory(
            title="Category Post1",
            show_on_index=True,
            status=Post.STATUS_CHOICES.published,
            category=self.category,
        )
        self.category_post2 = PostFactory(
            title="Category Post2",
            show_on_index=True,
            status=Post.STATUS_CHOICES.published,
            category=self.category,
        )
        self.no_category_post = PostFactory(
            title="No Category Post",
            show_on_index=False,
            status=Post.STATUS_CHOICES.published,
            category=None,
        )

    def test_good_view(self):
        url = self.category.get_absolute_url()

        response = self.client.get(url)
        assert response.status_code == 200
        self.assertTemplateUsed(response, "blog/category.html")
        self.assertIn("entry_list", response.context_data)

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
        self.assertContains(response, "%s" % (self.category,))


class CategoryListViewTestCase(TestCase):
    def setUp(self):
        self.category1 = PostCategoryFactory(name="cate1")
        self.category2 = PostCategoryFactory(name="cate2")
        self.post = PostFactory(
            title="Post",
            show_on_index=True,
            status=Post.STATUS_CHOICES.published,
            category=self.category1,
        )

    def test_good_view(self):
        url = reverse("blog:categories")
        response = self.client.get(url)
        assert response.status_code == 200
        self.assertTemplateUsed(response, "blog/category_list.html")

    def test_categories(self):
        url = reverse("blog:categories")
        response = self.client.get(url)

        self.assertContains(response, self.category1)
        self.assertContains(response, self.category2)
        self.assertContains(response, f"{self.category1}（1）")
        self.assertContains(response, f"{self.category2}（0）")


class PostArchivesViewTestCase(TestCase):
    def test_good_view(self):
        url = reverse("blog:archives")
        response = self.client.get(url)
        assert response.status_code == 200
        self.assertTemplateUsed(response, "blog/archives.html")


class DonateViewTestCase(TestCase):
    def test_good_view(self):
        url = reverse("blog:donate")
        response = self.client.get(url)
        assert response.status_code == 200
        self.assertTemplateUsed(response, "blog/donate.html")


@pytest.mark.django_db
def test_blog_search_view_paginator(rf):
    url = reverse("blog:search")
    request = rf.get(url)
    view = BlogSearchView()
    view.request = request
    paginator, page = view.build_page()
    assert isinstance(paginator, Paginator)


@pytest.mark.django_db
def test_blog_search_view_invalid_page_number(rf):
    url = reverse("blog:search")
    request = rf.get(url, data={"page": "a"})
    view = BlogSearchView()
    view.request = request
    with pytest.raises(Http404):
        assert view.build_page()

    request = rf.get(url, data={"page": -1})
    view = BlogSearchView()
    view.request = request
    with pytest.raises(Http404):
        assert view.build_page()

    # Always redirect to page 1
    request = rf.get(url, data={"page": 99999})
    view = BlogSearchView()
    view.request = request
    paginator, page = view.build_page()
    assert page.number == 1
