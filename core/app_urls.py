from django.urls import path
from .views import system_settings

app_name = 'core'

urlpatterns = [
    path('settings/', system_settings, name='system_settings'),
]
