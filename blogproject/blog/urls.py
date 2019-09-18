from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('category/<slug:slug>/', views.CategoryView.as_view(), name='category'),
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('archives/', views.PostArchivesView.as_view(), name='archives'),
    path('donate/', views.DonateView.as_view(), name='donate'),
    path('search/', views.BlogSearchView(), name='search'),
]
