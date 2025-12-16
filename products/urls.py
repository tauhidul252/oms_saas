from django.urls import path
from .views import manage_stock

from .views import (
    manage_stock, product_list, product_create, product_edit, product_delete,
    manage_categories
)

urlpatterns = [
    path('manage-stock/', manage_stock, name='manage_stock'),
    path('list/', product_list, name='product_list'),
    path('add/', product_create, name='product_create'),
    path('edit/<int:pk>/', product_edit, name='product_edit'),
    path('delete/<int:pk>/', product_delete, name='product_delete'),
    path('categories/', manage_categories, name='manage_categories'),
]
