from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ClusterConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cluster"
    verbose_name = _('Cluster')
