# Catalog urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('search/', views.search_results, name='search-results'),
    path('add-laptop/', views.add_laptop, name='add-laptop'),
    path('edit-laptop/<str:laptop_model>/', views.edit_laptop, name='edit-laptop'),
    path('item/<str:model_number>/', views.item_page, name='item-page'),
    path('laptop/<str:laptop_model>/', views.laptop_page, name='laptop-page'),
    path('part-upvote/', views.part_upvote, name='part-upvote'),
    path('laptop-upvote/', views.laptop_upvote, name='laptop-upvote'),
    path('laptop-downvote/', views.laptop_downvote, name='laptop-downvote'),
    path('part-downvote/', views.part_downvote, name='part-downvote'),
]