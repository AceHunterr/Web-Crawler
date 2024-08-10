from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('crawl/', views.start_crawl, name='start_crawl'),
    path('search/', views.search, name='search'),
    path('search_page/', views.search_page, name='search_page'),
]