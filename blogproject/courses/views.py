from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse
from django.views import generic

from braces.views import SelectRelatedMixin, SetHeadlineMixin

from .models import Course, Material


class CourseListView(SetHeadlineMixin, generic.ListView):
    model = Course
    template_name = "courses/course_list.html"
    headline = "教程"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(total_views=Coalesce(Sum("material__views"), 0))
            .select_related("category")
            .order_by("category", "rank", "-created")
        )


class CourseDetailView(SetHeadlineMixin, generic.DetailView):
    model = Course
    template_name = "courses/course_detail.html"

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        course = self.object

        first_material = course.first_material
        if first_material:
            context["next"] = {
                "title": first_material.title,
                "url": first_material.get_absolute_url(),
            }
        return context

    def get_headline(self):
        return self.object.title


class MaterialDetailView(SetHeadlineMixin, SelectRelatedMixin, generic.DetailView):
    model = Material
    template_name = "courses/material_detail.html"
    select_related = ("course",)

    def get(self, request, *args, **kwargs):
        response = super().get(request, *kwargs, **kwargs)
        self.object.increase_views()
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        material = self.object

        context["course"] = material.course
        context["num_comments"] = material.num_comments
        context["num_comment_participants"] = material.num_comment_participants

        material_prev = material.prev
        material_next = material.next
        if material_prev:
            context["prev"] = {
                "title": material_prev["title"],
                "url": reverse(
                    "courses:material_detail",
                    kwargs={
                        "pk": material_prev["id"],
                        "slug": material_prev["course__slug"],
                    },
                ),
            }
        if material_next:
            context["next"] = {
                "title": material_next["title"],
                "url": reverse(
                    "courses:material_detail",
                    kwargs={
                        "pk": material_next["id"],
                        "slug": material_next["course__slug"],
                    },
                ),
            }
        return context

    def get_headline(self):
        return "{}_{}".format(self.object.title, self.object.course.title)
