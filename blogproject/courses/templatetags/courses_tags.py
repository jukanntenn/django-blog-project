from django import template
from ..models import Course, Material
import re
from django.urls import reverse

register = template.Library()


@register.inclusion_tag('courses/inclusions/_toc.html')
def build_toc(current):
    if isinstance(current, Course):
        material_list = current.material_set.all()
        context = {
            'material_list': material_list,
            'current_material': None,
            'course': current,
        }
        return context

    if isinstance(current, Material):
        material_list = current.course.material_set.all()
        context = {
            'material_list': material_list,
            'current_material': current,
            'course': current.course,
        }
    return context


@register.filter
def absolutify(value, material):
    def add_url(matchobj):
        return 'href=' + reverse('courses:material_detail',
                                 kwargs={'pk': material.id, 'slug': material.course.slug}) + matchobj.group(
            1)

    return re.sub('href="(.+)"', add_url, value)
