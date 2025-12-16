from django.urls import path
from . import views

urlpatterns = [
    path('', views.employee_list, name='employee_list'),
    path('add/', views.add_employee, name='add_employee'),
    path('edit/<int:pk>/', views.edit_employee, name='edit_employee'),
    path('delete/<int:pk>/', views.delete_employee, name='delete_employee'),
]
