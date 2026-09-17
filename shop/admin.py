from django.contrib import admin
from .models import Category, Product
from .models import Order

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'available']
    list_filter = ['available', 'category']
    list_editable = ['price', 'available']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'customer_phone', 'customer_address', 'product', 'created_at', 'status']
    list_filter = ['status', 'created_at']
    list_editable = ['status']
