from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class IpResourceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "IP_resource"
    verbose_name = _('External Resource')
