from django.shortcuts import render
from django.db import connection
from django.core.management import call_command
from django.contrib.auth.models import User
from core.models import OMSSettings
import os

def installer_form(request):
    message = ""
    
    # যদি আগে থেকেই ইনস্টল হয়ে থাকে, তাহলে redirect
    if OMSSettings.objects.exists():
        return redirect('dashboard')

    if request.method == "POST":
        db_name = request.POST.get("db_name")
        db_user = request.POST.get("db_user")
        db_pass = request.POST.get("db_pass")
        db_host = request.POST.get("db_host")
        db_port = request.POST.get("db_port")
        admin_user = request.POST.get("admin_user")
        admin_email = request.POST.get("admin_email")
        admin_pass = request.POST.get("admin_pass")
        brand = request.POST.get("brand")
        logo = request.FILES.get("logo")

        # ✅ .env ফাইল লেখা (development/auto install only)
        with open(".env", "w") as env:
            env.write(f"DB_NAME={db_name}\n")
            env.write(f"DB_USER={db_user}\n")
            env.write(f"DB_PASSWORD={db_pass}\n")
            env.write(f"DB_HOST={db_host}\n")
            env.write(f"DB_PORT={db_port}\n")
            env.write("SECRET_KEY=django-insecure-abc123\nDEBUG=True\n")

        # ✅ মাইগ্রেশন চালানো
        os.system("python manage.py makemigrations")
        os.system("python manage.py migrate")

        # ✅ এডমিন ইউজার তৈরি
        if not User.objects.filter(username=admin_user).exists():
            User.objects.create_superuser(admin_user, admin_email, admin_pass)
            message = "✅ Installation successful! Admin created."
        else:
            message = "⚠️ Admin user already exists."

        # ✅ Brand & Logo সংরক্ষণ
        if not OMSSettings.objects.exists():
            OMSSettings.objects.create(brand_name=brand, logo=logo)

        return redirect('login')

    return render(request, "installer/installer_form.html", {"message": message})