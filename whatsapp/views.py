from django.shortcuts import render, redirect
from django.contrib import messages
from customers.models import Customer
from orders.models import Order
from core.models import OMSSettings
from .models import MessageLog
from .utils import replace_shortcodes
import requests

def send_whatsapp_message(phone, message, token, api_url):
    payload = {
        'phone': phone,
        'message': message,
        'token': token
    }
    try:
        response = requests.post(api_url, data=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print("WhatsApp Error:", e)
        return False

def send_bulk_message(request):
    settings = OMSSettings.objects.first()
    token = settings.whatsapp_token
    api_url = settings.whatsapp_api_url

    if request.method == "POST":
        message_text = request.POST.get("message")
        tag = request.POST.get("tag")  # 'All' or 'VIP'

        if tag == "VIP":
            customers = Customer.objects.filter(tag="VIP")
        else:
            customers = Customer.objects.all()

        success_count = 0

        for customer in customers:
            latest_order = Order.objects.filter(customer=customer).order_by('-date').first()

            data = {
                "name": customer.name,
                "order_id": latest_order.order_id if latest_order else "N/A",
                "status": latest_order.status if latest_order else "N/A"
            }

            personalized_message = replace_shortcodes(message_text, data)

            sent = send_whatsapp_message(customer.phone, personalized_message, token, api_url)

            # ✅ Save to message log
            MessageLog.objects.create(
                customer=customer,
                phone=customer.phone,
                message=personalized_message,
                status="Sent" if sent else "Failed"
            )

            if sent:
                success_count += 1

        messages.success(request, f"{success_count} message(s) sent successfully.")
        return redirect("send_bulk_message")

    return render(request, "whatsapp/send_message.html")
