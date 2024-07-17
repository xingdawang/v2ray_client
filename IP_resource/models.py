from django.db import models
from cluster.models import DbServer, ProtocalConfig
from django.utils.translation import gettext_lazy as _

class IPResource(models.Model):

    ip_address = models.CharField(_('IP Address'), max_length=15)
    port = models.IntegerField(_('Port'))
    username = models.CharField(_('Username'), max_length=100)
    password = models.CharField(_('Password'), max_length=100)
    expire_date = models.DateTimeField(_('Expire Date'), null=True, blank=True)
    host_server = models.ForeignKey(DbServer, on_delete=models.SET_NULL, null=True, blank=True, related_name='users', verbose_name=_('Host Server'))
    protocol_config = models.ForeignKey(ProtocalConfig, on_delete=models.SET_NULL, null=True, blank=True, related_name='ip_resources', verbose_name=_('Protocal Config'))
    note = models.TextField(_('Note'), null=True, blank=True)

    class Meta:
        verbose_name = _('IP Resource')
        verbose_name_plural = _('IP Resources')

    def __str__(self):
        return self.ip_address