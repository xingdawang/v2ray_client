# IP_resource/urls.py

from django.urls import path
from .views import ProtocalConfigAutocomplete

urlpatterns = [
    path('protocol-config-autocomplete/', ProtocalConfigAutocomplete.as_view(), name='protocol-config-autocomplete'),
]
