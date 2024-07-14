from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    registration_time = models.DateTimeField(default=timezone.now)
    connection_url = models.URLField(max_length=200, blank=True)
    usage = models.IntegerField(default=0)