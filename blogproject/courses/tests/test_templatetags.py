from datetime import timedelta

import pytest
from courses.templatetags.courses_extras import show_course_toc
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.utils import timezone
from freezegun import freeze_time

from .factories import MaterialFactory


@pytest.mark.django_db
def test_generate_toc_if_no_cache(course):
    MaterialFactory(course=course)
    MaterialFactory(course=course)
    context = show_course_toc(course)
    material_list = context["material_list"]
    assert all("toc" in m for m in material_list)


@pytest.mark.django_db
def test_do_not_generate_toc_if_cache(course):
    key = make_template_fragment_key("course_toc", [course.pk])
    cache.set(key, "cached toc", timeout=300)
    assert cache.get(key) is not None
    context = show_course_toc(course)
    material_list = context["material_list"]
    assert all("toc" not in m for m in material_list)


@pytest.mark.django_db
def test_generate_toc_if_cache_expired(course):
    key = make_template_fragment_key("course_toc", [course.pk])
    cache.set(key, "cached toc", timeout=300)
    assert cache.get(key) is not None

    with freeze_time(timezone.now() + timedelta(seconds=301)):
        context = show_course_toc(course)
        material_list = context["material_list"]
        assert all("toc" in m for m in material_list)
