from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Employee
from .forms import EmployeeForm

# List Employees
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'accounts/employee_list.html', {'employees': employees})

# Add Employee
def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Employee added successfully.")
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'accounts/add_employee.html', {'form': form})

# Edit Employee
def edit_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Employee updated.")
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'accounts/add_employee.html', {'form': form})

# Delete Employee
def delete_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        messages.success(request, "🗑 Employee deleted.")
        return redirect('employee_list')
    return render(request, 'accounts/confirm_delete.html', {'employee': employee})
