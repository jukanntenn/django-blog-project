from courses.models import Course, Material
from django.contrib.sitemaps import GenericSitemap

from .models import Category, Post

post_info_dict = {
    "queryset": Post.objects.all(),
    "date_field": "modified_time",
}

category_info_dict = {
    "queryset": Category.objects.all(),
}

course_info_dict = {
    "queryset": Course.objects.all(),
}

material_info_dict = {
    "queryset": Material.objects.all(),
}

sitemaps = {
    "post": GenericSitemap(post_info_dict, priority=0.6),
    "category": GenericSitemap(category_info_dict, priority=1),
    "course": GenericSitemap(course_info_dict, priority=1),
    "material": GenericSitemap(material_info_dict, priority=0.6),
}
