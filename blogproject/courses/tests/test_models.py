from datetime import timedelta

import pytest
from courses.models import Material
from courses.tests.factories import MaterialFactory
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.utils import timezone


@pytest.mark.django_db
class TestCourse:
    def test_get_absolute_url(self, course):
        assert course.get_absolute_url() == f"/courses/{course.slug}/"

    def test_first_material(self, course):
        material1 = MaterialFactory(course=course)
        MaterialFactory(course=course)
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

    def test_invalid_toc_cache_if_save(self, course):
        key = make_template_fragment_key("course_toc", [course.pk])
        cache.set(key, "cached toc", timeout=300)
        assert cache.get(key) is not None
        course.save()
        assert cache.get(key) is None


@pytest.mark.django_db
class TestMaterialQuerySetAndIndexManager:
    def setup_method(self):
        after_3_days = timezone.now() + timedelta(days=3)

        self.published_material = MaterialFactory(
            status=Material.STATUS.published,
            show_on_index=True,
            pub_date=timezone.now(),
        )
        self.draft_material = MaterialFactory(
            status=Material.STATUS.draft,
            show_on_index=True,
        )
        self.writing_material = MaterialFactory(
            status=Material.STATUS.writing,
            show_on_index=True,
        )
        self.hidden_material = MaterialFactory(
            status=Material.STATUS.hidden,
            show_on_index=True,
        )
        self.future_publishing_material = MaterialFactory(
            status=Material.STATUS.published,
            show_on_index=True,
            pub_date=after_3_days,
        )
        self.future_draft_material = MaterialFactory(
            status=Material.STATUS.draft,
            show_on_index=True,
            pub_date=after_3_days,
        )
        self.hide_on_index_published_material = MaterialFactory(
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

    def test_invalid_toc_cache_if_save(self, material):
        key = make_template_fragment_key("course_toc", [material.course_id])
        cache.set(key, "cached course toc", timeout=300)
        assert cache.get(key) is not None
        material.save()
        assert cache.get(key) is None
