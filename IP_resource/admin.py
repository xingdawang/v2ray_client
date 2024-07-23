# admin.py

from django.contrib import admin
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
import json
from .models import IPResource
from .forms import IPResourceForm
from django.utils.translation import gettext_lazy as _

class IPResourceAdmin(admin.ModelAdmin):
    form = IPResourceForm

    list_display = ('ip_address', 'port', 'username', 'expire_date', 'host_server', 'protocol_config')

    # Customize the filter
    list_filter = ('host_server',)

    def get_custom_template(self, ip_resources):

        template = {'api': {'services': ['HandlerService', 'LoggerService', 'StatsService'],
          'tag': 'api'},
         'inbounds': [{'listen': '127.0.0.1',
           'port': 62789,
           'protocol': 'dokodemo-door',
           'settings': {'address': '127.0.0.1'},
           'tag': 'api'}],
         'outbounds': [{'protocol': 'freedom', 'settings': {}},
          {'protocol': 'blackhole', 'settings': {}, 'tag': 'blocked'}],
         'policy': {'system': {'statsInboundDownlink': True,
           'statsInboundUplink': True}},
         'routing': {'rules': [{'inboundTag': ['api'],
            'outboundTag': 'api',
            'type': 'field'},
           {'ip': ['geoip:private'], 'outboundTag': 'blocked', 'type': 'field'},
           {'outboundTag': 'blocked', 'protocol': ['bittorrent'], 'type': 'field'}]},
         'stats': {}}

        for ip_resource in ip_resources:

            # unpack
            ip_address = ip_resource['ip_address']
            port = ip_resource['port']
            username = ip_resource['username']
            password = ip_resource['password']
            config_port = ip_resource['protocol_config__port']

            # add routing rules
            routing_rule = {'type': 'field', 'inboundTag': 'inbound-' + str(config_port), 'outboundTag': str(config_port)+'-warp'}
            template['routing']['rules'].append(routing_rule)

            # add outbounds
            outbound_rule = {'tag': str(config_port) + '-warp', 'protocol': 'http',
                             'settings': {'servers': [{'address': ip_address,'port': port,'users': [{'user': username, 'pass': password}]}]}}
            template['outbounds'].insert(0, outbound_rule)
        return template


    # Define custom admin action to generate JSON data and open it in a new tab
    def export_to_json(self, request, queryset):
        ip_resources = list(queryset.values('ip_address', 'port', 'username', 'password', 'expire_date', 'protocol_config__port'))
        print(ip_resources)

        # Convert datetime objects to ISO 8601 strings
        for resource in ip_resources:
            resource['expire_date'] = resource['expire_date'].isoformat() if resource['expire_date'] else None
            resource['protocol_config__port'] = resource['protocol_config__port'] if resource['protocol_config__port'] else 0

        json_data = self.get_custom_template(ip_resources) # {'server': ip_resources}

        # Serialize JSON data
        json_str = json.dumps(json_data, cls=DjangoJSONEncoder, indent=4)

        # Return JSON response with appropriate content type
        response = HttpResponse(json_str, content_type='application/json')

        return response

    export_to_json.short_description = _("Show X-UI config template")

    # Add admin action to actions list
    actions = ['export_to_json']


admin.site.register(IPResource, IPResourceAdmin)