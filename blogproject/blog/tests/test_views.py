from blog.models import Post
from courses.models import Material
from django.test import TestCase
from django.urls import reverse
from django_dynamic_fixture import G


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
        self.assertContains(response, '%s' % (self.index_post.title,))
