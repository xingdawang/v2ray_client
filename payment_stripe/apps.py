from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class PaymentStripeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "payment_stripe"
    verbose_name = _('Stripe Payment')
