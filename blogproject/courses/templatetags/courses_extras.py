from core.utils import generate_rich_content
from django import template
from django.urls import reverse

register = template.Library()


@register.inclusion_tag("courses/inclusions/_toc.html")
def show_course_toc(course, current=None):
    material_list = course.material_set.all().values("id", "title", "body")

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
