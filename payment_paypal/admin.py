from django.contrib import admin
from .models import PayPalOrder, Product

class PayPalOrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_id', 'status', 'amount', 'currency', 'payer_email', 'payer_name', 'gross_amount', 'paypal_fee', 'net_amount', 'capture_create_time')
    list_filter = ('status', 'currency', 'capture_create_time')
    search_fields = ('order_id', 'payer_email', 'payer_name')
    ordering = ('-capture_create_time',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)

admin.site.register(PayPalOrder, PayPalOrderAdmin)
admin.site.register(Product, ProductAdmin)
