from django.db import models
from django.conf import settings

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name

class StripePaymentLink(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Added ForeignKey to Product
    checkout_session_id = models.CharField(max_length=255, unique=True)
    payment_intent = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=50, null=True)
    amount_total = models.DecimalField(max_digits=10, null=True, decimal_places=2)
    currency = models.CharField(max_length=10, null=True)
    created = models.DateTimeField(null=True)
    payer_email = models.EmailField(null=True)
    payer_name = models.CharField(max_length=255, null=True)
    payment_method = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"{self.user} - {self.status} - {self.amount_total} - {self.currency}"