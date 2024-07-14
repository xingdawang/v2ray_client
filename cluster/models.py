from django.db import models
from django.contrib.auth import get_user_model

class DbServer(models.Model):
    server_name = models.CharField(max_length=100)
    server_ip = models.CharField(max_length=100)

    def __str__(self):
        return self.server_name

class ProtocalConfig(models.Model):

    remark = models.CharField(max_length=100)
    server_ip = models.CharField(max_length=100)
    up = models.IntegerField(default=0, blank=True)
    down = models.IntegerField(default=0, blank=True)
    total = models.IntegerField(default=-1, blank=True)
    enable = models.IntegerField(default=1, blank=True)
    expiry_time = models.IntegerField(default=-1, blank=True)
    port = models.IntegerField()
    uuid = models.CharField(max_length=100)
    alter_id = models.IntegerField()
    network = models.CharField(max_length=100)
    network_type = models.CharField(max_length=100)
    protocal = models.CharField(max_length=100)
    config_url = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.remark + '-' + str(self.port)