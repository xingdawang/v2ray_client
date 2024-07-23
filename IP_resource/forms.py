# IP_resource/forms.py

from django import forms
from dal import autocomplete
from cluster.models import DbServer, ProtocalConfig
from .models import IPResource
from django.utils.translation import gettext_lazy as _

class IPResourceForm(forms.ModelForm):
    class Meta:
        model = IPResource
        fields = '__all__'
        widgets = {
            'protocol_config': autocomplete.ModelSelect2(
                url='protocol-config-autocomplete',
                forward=['host_server'],
                attrs={'data-placeholder': _('Select an option or leave blank...')}
            )
        }
