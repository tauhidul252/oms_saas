from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),
    
    # App routes
    path('install/', include('installer.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('orders/', include('orders.urls')),
    path('products/', include('products.urls')),
    path('employees/', include('employees.urls')),
    path('invoice/', include('invoice.urls')),
    path('whatsapp/', include('whatsapp.urls')),
    path('core/', include('core.app_urls')),
    
    # Root redirect to installer (will redirect to dashboard if already installed)
    path('', lambda request: redirect('installer_form')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


