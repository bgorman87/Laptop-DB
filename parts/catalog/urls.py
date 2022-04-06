from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('search/', views.search_results, name='search-results'),
    path('add-data/', views.add_data, name='add-data'),
    path('add-parts/<str:laptop_model>/', views.add_parts, name='add-parts'),
    path('item/<str:model_number>/', views.item_page, name='item-page'),
    path('laptop/<str:laptop_model>/', views.laptop_page, name='laptop-page')
]