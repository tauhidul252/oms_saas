from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from decimal import Decimal
from .models import Customer, Order, OrderItem
from employees.utils import has_role
from django.http import HttpResponseForbidden
from django.db.models import Q
from core.models import OMSSettings
from products.models import Product
from django.views.decorators.http import require_POST

# ✅ Order Create View
def create_order(request):
    if not has_role(request.user, ["Operator", "Manager", "Admin"]):
        return HttpResponseForbidden("❌ You are not authorized to create orders.")

    products = Product.objects.all()

    if request.method == "POST":
        phone = request.POST['customer_phone']
        name = request.POST['customer_name']
        address = request.POST['customer_address']
        product_id = request.POST['product_id']
        qty = int(request.POST['quantity'])
        discount = Decimal(request.POST.get('discount_amount', 0))
        tracking = request.POST.get('tracking_number', '')

        product = get_object_or_404(Product, id=product_id)
        price = product.price

        # ✅ Stock Check
        if product.stock < qty:
            return render(request, 'orders/order_form.html', {
                'products': products,
                'error': f"❌ Not enough stock for {product.name}. Available: {product.stock}"
            })

        subtotal = qty * price
        total = subtotal - discount

        # ✅ Apply rounding if enabled
        settings = OMSSettings.objects.first()
        if settings and settings.rounding_enabled:
            total = round(total)

        # ✅ Category Prefix Based Order ID
        prefix = product.category.prefix
        today = timezone.now().date()
        count = Order.objects.filter(date__date=today).count() + 1
        order_id = f"{prefix}-{today.strftime('%Y-%m-%d')}-{count:04d}"

        customer, created = Customer.objects.get_or_create(
            phone=phone, defaults={'name': name, 'address': address}
        )
        if not created:
            customer.name = name
            customer.address = address
            customer.save()

        order = Order.objects.create(
            customer=customer,
            order_id=order_id,
            tracking_number=tracking,
            discount_amount=discount,
            grand_total=total,
            status="Pending"
        )

        OrderItem.objects.create(
            order=order,
            product_name=product.name,
            quantity=qty,
            unit_price=price
        )

        product.stock -= qty
        product.save()

        return redirect('print_invoice', order_id=order.order_id)

    return render(request, 'orders/order_form.html', {'products': products})

# ✅ Order List View
def order_list(request):
    if not has_role(request.user, ["Viewer", "Operator", "Manager", "Admin"]):
        return HttpResponseForbidden("❌ You are not authorized to view orders.")

    query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')

    orders = Order.objects.all().order_by('-date')

    if query:
        orders = orders.filter(
            Q(order_id__icontains=query) |
            Q(customer__phone__icontains=query) |
            Q(customer__name__icontains=query)
        )

    if status_filter:
        orders = orders.filter(status=status_filter)

    return render(request, 'orders/order_list.html', {
        'orders': orders,
        'query': query,
        'status_filter': status_filter
    })

# ✅ Order Detail View
def order_detail(request, order_id):
    if not has_role(request.user, ["Viewer", "Operator", "Manager", "Admin"]):
        return HttpResponseForbidden("❌ Not allowed")

    order = get_object_or_404(Order, order_id=order_id)
    return render(request, 'orders/order_detail.html', {'order': order})

# ✅ Order Edit View (with rounding)
def order_edit(request, order_id):
    if not has_role(request.user, ["Manager", "Admin"]):
        return HttpResponseForbidden("❌ Not allowed")

    order = get_object_or_404(Order, order_id=order_id)
    item = order.items.first()

    if request.method == "POST":
        item.product_name = request.POST['product_name']
        item.quantity = int(request.POST['quantity'])
        item.unit_price = Decimal(request.POST['unit_price'])
        item.save()

        order.tracking_number = request.POST.get('tracking_number', '')
        order.discount_amount = Decimal(request.POST.get('discount_amount', 0))
        order.status = request.POST.get('status', 'Pending')
        order.grand_total = item.quantity * item.unit_price - order.discount_amount

        settings = OMSSettings.objects.first()
        if settings and settings.rounding_enabled:
            order.grand_total = round(order.grand_total)

        order.save()

        return redirect('order_detail', order_id=order.order_id)

    return render(request, 'orders/order_edit.html', {
        'order': order,
        'item': item
    })

# ✅ Order Delete
def order_delete(request, order_id):
    if not has_role(request.user, ["Admin"]):
        return HttpResponseForbidden("❌ Not allowed")

    order = get_object_or_404(Order, order_id=order_id)
    if request.method == "POST":
        order.delete()
        return redirect('order_list')

    return render(request, 'orders/order_confirm_delete.html', {'order': order})

# ✅ Multiple Invoice Print View
@require_POST
def multi_invoice_print(request):
    order_ids = request.POST.getlist('order_ids')
    orders = Order.objects.filter(order_id__in=order_ids)
    return render(request, 'invoice/multi_invoice.html', {'orders': orders})
