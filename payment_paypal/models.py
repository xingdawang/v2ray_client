from django.db import models
from django.conf import settings

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name

class PayPalOrder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    # New fields for additional details
    payer_email = models.EmailField()
    payer_name = models.CharField(max_length=255)
    gross_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    paypal_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    net_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    capture_create_time = models.DateTimeField(null=True, blank=True)
    capture_status = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"Order {self.order_id} - {self.status}"