from django.shortcuts import render, get_object_or_404
from orders.models import Order
from core.models import OMSSettings

# Single invoice print
def print_invoice(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    settings = OMSSettings.objects.first()
    return render(request, 'invoice_template.html', {
        'order': order,
        'settings': settings
    })

# ✅ Multiple invoice print
def print_multiple_invoices(request):
    orders = []
    settings = OMSSettings.objects.first()

    if request.method == "POST":
        raw_ids = request.POST.get("order_ids")
        id_list = [x.strip() for x in raw_ids.replace("\n", ",").split(",") if x.strip()]
        orders = Order.objects.filter(order_id__in=id_list)

    return render(request, "multi_invoice_print.html", {
        "orders": orders,
        "settings": settings
    })
