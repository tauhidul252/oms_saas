from django.shortcuts import render
from orders.models import Order
from django.db.models import Sum, Count
from django.utils.timezone import now
from employees.utils import has_role
from datetime import date

def dashboard_view(request):
    if not has_role(request.user, ["Viewer", "Operator", "Manager", "Admin"]):
        return render(request, '403.html')

    today = date.today()
    total_orders = Order.objects.count()
    today_orders = Order.objects.filter(date__date=today).count()
    total_revenue = Order.objects.aggregate(Sum('grand_total'))['grand_total__sum'] or 0

    status_count = Order.objects.values('status').annotate(count=Count('id'))
    status_dict = {item['status']: item['count'] for item in status_count}

    recent_orders = Order.objects.all().order_by('-date')[:10]

    return render(request, 'dashboard/dashboard.html', {
        'total_orders': total_orders,
        'today_orders': today_orders,
        'total_revenue': total_revenue,
        'status_dict': status_dict,
        'recent_orders': recent_orders
    })
