from django.urls import path
from .views import print_invoice, print_multiple_invoices

urlpatterns = [
    path('print/<str:order_id>/', print_invoice, name='print_invoice'),
    path('print-multiple/', print_multiple_invoices, name='print_multiple_invoices'),
]
