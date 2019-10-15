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
