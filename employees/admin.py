from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "employee_id")
    list_filter = ("role",)
    search_fields = ("user__username", "employee_id")
