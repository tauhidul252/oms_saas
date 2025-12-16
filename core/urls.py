from django.urls import path
from .views import system_settings

urlpatterns = [
    path('settings/', system_settings, name='system_settings'),
]
