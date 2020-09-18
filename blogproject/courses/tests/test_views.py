from courses.models import Material
from courses.tests.factories import CourseFactory, MaterialFactory
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone


def test_auto_set_admin_as_material_author(admin_client, admin_user, course):
    url = reverse("admin:courses_material_add")
    data = {
        "title": "测试标题",
        "body": "测试内容",
        "pub_date": timezone.now(),
        "course": course.pk,
        "rank": 0,
        "status": Material.STATUS.published,
    }
    response = admin_client.post(url, data=data)
    assert response.status_code == 302

    assert Material.objects.count() == 1
    material = Material.objects.all().latest("created")
    assert material.author == admin_user


class CourseListViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse("courses:course_list")

    def test_good_view(self):
        response = self.client.get(self.url)
        assert response.status_code == 200
        self.assertTemplateUsed(response, "courses/course_list.html")


class CourseDetailViewTestCase(TestCase):
    def setUp(self):
        self.course = CourseFactory()
        self.material1 = MaterialFactory(course=self.course, rank=0)
        self.material2 = MaterialFactory(course=self.course, rank=1)

    def test_good_view(self):
        url = self.course.get_absolute_url()
        response = self.client.get(url)
        assert response.status_code == 200
        self.assertTemplateUsed(response, "courses/course_detail.html")
        self.assertIn("next", response.context_data)
        self.assertEqual(
            response.context_data["next"],
            {"title": self.material1.title, "url": self.material1.get_absolute_url()},
        )

    def test_headline(self):
        course_url = self.course.get_absolute_url()
        response = self.client.get(course_url)
        self.assertContains(response, self.course.title)


class MaterialDetailViewTestCase(TestCase):
    def setUp(self):
        self.course = CourseFactory()
        self.material1 = MaterialFactory(course=self.course, rank=0)
        self.material2 = MaterialFactory(course=self.course, rank=1)
        self.material3 = MaterialFactory(course=self.course, rank=2)

    def test_good_view(self):
        url = self.material2.get_absolute_url()
        response = self.client.get(url)
        assert response.status_code == 200
        self.assertTemplateUsed(response, "courses/material_detail.html")
        self.assertIn("course", response.context_data)
        self.assertIn("num_comments", response.context_data)
        self.assertIn("num_comment_participants", response.context_data)
        self.assertIn("prev", response.context_data)
        self.assertIn("next", response.context_data)

    def test_increase_material_views(self):
        url = self.material2.get_absolute_url()
        self.client.get(url)
        self.material2.refresh_from_db()
        assert self.material2.views == 1

    def test_headline(self):
        url = self.material2.get_absolute_url()
        response = self.client.get(url)
        self.assertContains(
            response, "%s_%s" % (self.material2.title, self.material2.course.title)
        )
