from django.db import models
from cluster.models import DbServer, ProtocalConfig

class IPResource(models.Model):

    ip_address = models.CharField(max_length=15)
    port = models.IntegerField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    expire_date = models.DateTimeField(null=True, blank=True)
    host_server = models.ForeignKey(DbServer, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    protocol_config = models.ForeignKey(ProtocalConfig, on_delete=models.SET_NULL, null=True, blank=True, related_name='ip_resources')
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.ip_address