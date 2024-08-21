from django.contrib import admin
from .models import StripePaymentLink, Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

class StripePaymentLinkAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'status', 'amount_total', 'created', 'payer_email', 'payment_method')
    readonly_fields = ('user', 'product', 'checkout_session_id', 'payment_intent', 'status', 'amount_total', 
        'currency', 'created', 'payer_name', 'payer_email', 'payment_method')
    list_filter = ('status', 'currency', 'created')
    search_fields = ('status', 'user')
    ordering = ('-created',)

admin.site.register(StripePaymentLink, StripePaymentLinkAdmin)
admin.site.register(Product, ProductAdmin)
