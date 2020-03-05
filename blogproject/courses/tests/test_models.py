from datetime import timedelta

import pytest
from django.utils import timezone
from django_dynamic_fixture import G

from courses.models import Category, Course, Material
from courses.tests.factories import CategoryFactory, CourseFactory, MaterialFactory


@pytest.mark.django_db
class TestCourse:
    def test_get_absolute_url(self, course):
        assert course.get_absolute_url() == f"/courses/{course.slug}/"

    def test_first_material(self, course):
        material1 = MaterialFactory(course=course)
        material2 = MaterialFactory(course=course)
        assert course.first_material == material1

    def test_rich_content(self, course):
        assert course.rich_content == {
            "content": "<p><strong>教程</strong></p>",
            "toc": "",
        }


@pytest.mark.django_db
class TestMaterial:
    def test_get_absolute_url(self, material):
        assert (
            material.get_absolute_url()
            == f"/courses/{material.course.slug}/materials/{material.pk}/"
        )

    def test_type(self, material):
        assert material.type == "m"

    def test_prev(self, course):
        material = MaterialFactory(course=course, rank=1)
        assert material.prev is None
        prev_material = MaterialFactory(course=course, rank=0)
        assert Material.objects.get(pk=material.pk).prev == {
            "course__slug": course.slug,
            "id": prev_material.pk,
            "title": prev_material.title,
        }

    def test_next(self, course):
        material = MaterialFactory(course=course)
        assert material.next is None
        next_material = MaterialFactory(course=course)
        assert Material.objects.get(pk=material.pk).next == {
            "course__slug": course.slug,
            "id": next_material.pk,
            "title": next_material.title,
        }


@pytest.mark.django_db
class TestMaterialQuerySetAndIndexManager:
    def setup_method(self):
        after_3_days = timezone.now() + timedelta(days=3)

        self.published_material = G(
            Material,
            status=Material.STATUS.published,
            show_on_index=True,
            pub_date=timezone.now(),
        )
        self.draft_material = G(
            Material,
            status=Material.STATUS.draft,
            show_on_index=True,
            ignore_fields=["pub_date"],
        )
        self.writing_material = G(
            Material,
            status=Material.STATUS.writing,
            show_on_index=True,
            ignore_fields=["pub_date"],
        )
        self.hidden_material = G(
            Material,
            status=Material.STATUS.hidden,
            show_on_index=True,
            ignore_fields=["pub_date"],
        )
        self.future_publishing_material = G(
            Material,
            status=Material.STATUS.published,
            show_on_index=True,
            pub_date=after_3_days,
        )
        self.future_draft_material = G(
            Material,
            status=Material.STATUS.draft,
            show_on_index=True,
            pub_date=after_3_days,
        )
        self.hide_on_index_published_material = G(
            Material,
            status=Material.STATUS.published,
            show_on_index=False,
            pub_date=timezone.now(),
        )

    def test_published(self):
        materials = Material.objects.published()
        assert materials.count() == 3
        # Note the ordering
        assert list(materials) == [
            self.published_material,
            self.future_publishing_material,
            self.hide_on_index_published_material,
        ]

    def test_draft(self):
        materials = Material.objects.draft()
        assert materials.count() == 2
        # Note the ordering
        assert list(materials) == [self.draft_material, self.future_draft_material]

    def test_hidden(self):
        materials = Material.objects.hidden()
        assert materials.count() == 1
        assert list(materials) == [self.hidden_material]

    def test_writing(self):
        materials = Material.objects.writing()
        assert materials.count() == 1
        assert list(materials) == [self.writing_material]

    def test_searchable(self):
        materials = Material.objects.searchable()
        assert materials.count() == 2
        # Note the ordering
        assert list(materials) == [
            self.published_material,
            self.hide_on_index_published_material,
        ]

    def test_index_manager_get_queryset(self):
        materials = Material.index.all()
        assert materials.count() == 1
        assert list(materials) == [self.published_material]
