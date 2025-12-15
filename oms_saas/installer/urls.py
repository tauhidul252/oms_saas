from django.urls import path
from . import views

urlpatterns = [
    path('', views.installer_form, name='installer_form'),
]
