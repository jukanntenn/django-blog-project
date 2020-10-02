from core.utils import generate_rich_content
from django import template
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.urls import reverse

register = template.Library()


@register.inclusion_tag("courses/inclusions/_toc.html")
def show_course_toc(course, current=None):
    material_list = course.material_set.all().values("id", "title", "body")

    key = make_template_fragment_key("course_toc", [course.pk])
    result = cache.get(key)
    # if not cached, regenerate the course's toc
    if result is None:
        # attach toc to material
        for material in material_list:
            toc_url = reverse(
                "courses:material_detail",
                kwargs={"slug": course.slug, "pk": material["id"]},
            )
            material["toc"] = generate_rich_content(material["body"], toc_url=toc_url)[
                "toc"
            ]

    context = {
        "material_list": material_list,
        "course": course,
        "current": current,
    }
    return context
