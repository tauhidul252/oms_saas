from django import forms
from .models import Product
from .models import Category, SubCategory

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'subcategory', 'price', 'stock']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'prefix']

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['name', 'category']