# IP_resource/views.py

from dal import autocomplete
from django.http import JsonResponse
from cluster.models import DbServer, ProtocalConfig

class ProtocalConfigAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        host_server_id = self.forwarded.get('host_server', None)

        if not host_server_id:
            return ProtocalConfig.objects.none()

        try:
            host_server = DbServer.objects.get(id=host_server_id)
            return ProtocalConfig.objects.filter(server_ip=host_server.server_ip)
        except DbServer.DoesNotExist:
            return ProtocalConfig.objects.none()
