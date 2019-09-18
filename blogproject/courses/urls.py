from django.urls import path

from . import views

app_name = 'courses'
urlpatterns = [
    path('<slug:slug>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('<slug:slug>/materials/<int:pk>/', views.MaterialDetailView.as_view(), name='material_detail'),
    path('', views.CourseListView.as_view(), name='course_list')
]
