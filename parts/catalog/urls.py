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
    path('part-model-change/<str:part_model>', views.part_model_change, name='part-model-change'),
    path('laptop-model-change/<str:laptop_model>', views.laptop_model_change, name='laptop-model-change'),
    path('requested-part-changes', views.requested_part_changes, name='requested-part-changes'),
    path('requested-part-change-review/<int:part_model_change_id>', views.requested_part_change_review, name='requested-part-change-review'),
    path('requested-laptop-changes', views.requested_laptop_changes, name='requested-laptop-changes'),
    path('requested-laptop-change-review/<int:laptop_model_change_id>', views.requested_laptop_change_review, name='requested-laptop-change-review'),
    path('delete-laptop/<int:laptop_id>/', views.confirm_delete_laptop, name='confirm-delete-laptop'),
    path('delete-part/<int:part_id>/', views.confirm_delete_part, name='confirm-delete-part'),
    path('verify-part/<int:part_id>/', views.verify_part, name='verify-part'),
    path('verify-laptop/<int:laptop_id>/', views.verify_laptop, name='verify-laptop'),
]