from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from cluster.models import ProtocalConfig
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    
    protocol_config = models.ForeignKey('cluster.ProtocalConfig', on_delete=models.SET_NULL, null=True, blank=True, related_name='users', verbose_name=_('Protocal Config'))
    customer_group = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('Customer Group'))
    note = models.TextField(_('Note'), null=True, blank=True)

    reset_token = models.CharField(max_length=32, null=True, blank=True)
    reset_token_expiry = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _('Custom User')
        verbose_name_plural = _('Custom Users')

    def generate_reset_token(self):
        token = get_random_string(length=32)
        self.reset_token = token
        self.reset_token_expiry = timezone.now() + timedelta(minutes=10)
        self.save()
        return token
