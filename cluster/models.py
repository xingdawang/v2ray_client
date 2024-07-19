from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

class DbServer(models.Model):
    server_name = models.CharField(_('Server Name'), max_length=100)
    server_ip = models.CharField(_('Server IP'), max_length=100)
    pem_name = models.CharField(_('pem name'), max_length=100)

    class Meta:
        verbose_name = _('Db Server')
        verbose_name_plural = _('Db Servers')

    def __str__(self):
        return self.server_name

class ProtocalConfig(models.Model):

    remark = models.CharField(_('Remark'), max_length=100)
    server_ip = models.CharField(_('Server IP'), max_length=100)
    up = models.IntegerField(_('Up'), default=0, blank=True)
    down = models.IntegerField(_('Down'), default=0, blank=True)
    total = models.IntegerField(_('Total'), default=-1, blank=True)
    enable = models.IntegerField(_('Enable'), default=1, blank=True)
    expiry_time = models.IntegerField(_('Expiry Time'), default=-1, blank=True)
    port = models.IntegerField(_('Port'))
    uuid = models.CharField(_('UUID'), max_length=100)
    alter_id = models.IntegerField(_('Alter ID'))
    network = models.CharField(_('Network'), max_length=100)
    network_type = models.CharField(_('Network Type'), max_length=100)
    protocal = models.CharField(_('Protocol'), max_length=100)
    config_url = models.CharField(_('Config URL'), max_length=300, blank=True)

    class Meta:
        verbose_name = _('Protocal Config')
        verbose_name_plural = _('Protocal Configs')

    def __str__(self):
        return self.remark + '-' + str(self.port)