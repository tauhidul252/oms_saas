from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from employees.utils import has_role
from .models import Product, Category, SubCategory
from .forms import ProductForm, CategoryForm, SubCategoryForm

# ✅ Stock Management View
@login_required
def manage_stock(request):
    if not has_role(request.user, ["Admin"]):
        return render(request, '403.html')

    products = Product.objects.all()

    if request.method == "POST":
        product_id = request.POST['product_id']
        new_stock = int(request.POST['stock'])

        product = get_object_or_404(Product, id=product_id)
        product.stock = new_stock
        product.save()

        messages.success(request, f"{product.name} stock updated to {new_stock}.")
        return redirect('manage_stock')

    return render(request, 'products/manage_stock.html', {'products': products})

# ✅ Product CRUD Views
@login_required
def product_list(request):
    if not has_role(request.user, ["Admin"]):
        return render(request, '403.html')

    products = Product.objects.select_related('category', 'subcategory')
    return render(request, 'products/product_list.html', {'products': products})

@login_required
def product_create(request):
    if not has_role(request.user, ["Admin"]):
        return render(request, '403.html')

    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Product added successfully.")
        return redirect('product_list')

    return render(request, 'products/product_form.html', {'form': form, 'action': 'Create'})

@login_required
def product_edit(request, pk):
    if not has_role(request.user, ["Admin"]):
        return render(request, '403.html')

    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        messages.success(request, "Product updated successfully.")
        return redirect('product_list')

    return render(request, 'products/product_form.html', {'form': form, 'action': 'Edit'})

@login_required
def product_delete(request, pk):
    if not has_role(request.user, ["Admin"]):
        return render(request, '403.html')

    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted.")
        return redirect('product_list')

    return render(request, 'products/product_confirm_delete.html', {'product': product})

# ✅ Category & SubCategory Management View
@login_required
def manage_categories(request):
    if not has_role(request.user, ["Admin"]):
        return render(request, '403.html')

    category_form = CategoryForm(request.POST or None, prefix='cat')
    subcategory_form = SubCategoryForm(request.POST or None, prefix='sub')
    categories = Category.objects.all().prefetch_related('subcategories')

    if request.method == "POST":
        if 'cat-name' in request.POST:  # category form submitted
            if category_form.is_valid():
                category_form.save()
                messages.success(request, "Category added/updated.")
                return redirect('manage_categories')
        elif 'sub-name' in request.POST:  # subcategory form submitted
            if subcategory_form.is_valid():
                subcategory_form.save()
                messages.success(request, "Subcategory added.")
                return redirect('manage_categories')

    return render(request, 'products/manage_categories.html', {
        'category_form': category_form,
        'subcategory_form': subcategory_form,
        'categories': categories
    })
