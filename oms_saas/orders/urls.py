from django.urls import path
from .views import multi_invoice_print

from .views import (
    create_order,
    order_list,
    order_detail,
    order_edit,
    order_delete,
)

urlpatterns = [
    path('create/', create_order, name='create_order'),
    path('list/', order_list, name='order_list'),
    path('detail/<str:order_id>/', order_detail, name='order_detail'),
    path('edit/<str:order_id>/', order_edit, name='order_edit'),
    path('delete/<str:order_id>/', order_delete, name='order_delete'),
]

urlpatterns += [
    path('multi-print/', multi_invoice_print, name='multi_invoice_print'),
]