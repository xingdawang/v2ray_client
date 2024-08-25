from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Product(models.Model):
    name = models.CharField(_('Product Name'), max_length=255)
    price = models.DecimalField(_('Product Price'), max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
    
    def __str__(self):
        return self.name

class StripePaymentLink(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('User'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Product'))
    checkout_session_id = models.CharField(_('Checkout Session ID'), max_length=255, unique=True)
    payment_intent = models.CharField(_('Payment Intent'), max_length=50, null=True)
    status = models.CharField(_('Status'), max_length=50, null=True)
    amount_total = models.DecimalField(_('Payment Amount'), max_digits=10, null=True, decimal_places=2)
    currency = models.CharField(_('Payment Currency'), max_length=10, null=True)
    created = models.DateTimeField(_('Create Time'), null=True)
    payer_email = models.EmailField(_('Payer Email'), null=True)
    payer_name = models.CharField(_('Payer Name'), max_length=255, null=True)
    payment_method = models.CharField(_('Payment Method'), max_length=50, null=True)

    class Meta:
        verbose_name = _('Stripe Payment Record')
        verbose_name_plural = _('Stripe Payment Records')

    def __str__(self):
        return f"{self.user} - {self.status} - {self.amount_total} - {self.currency}"