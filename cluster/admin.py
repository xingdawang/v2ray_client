from django.contrib import admin
from .models import DbServer, ProtocalConfig
from datetime import datetime
from django.http import HttpResponse
import openpyxl
from openpyxl.writer.excel import save_virtual_workbook


def export_to_excel(modeladmin, request, queryset):
    # Create a workbook and worksheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "ProtocalConfig"

    # Create headers
    headers = [
        'Remark', 'Server IP', 'Up', 'Down', 'Total', 'Enable',
        'Expiry Time', 'Port', 'UUID', 'Alter ID', 'Network',
        'Network Type', 'Protocal', 'Config URL'
    ]
    ws.append(headers)

    # Write data
    for obj in queryset:
        expiry_time_formatted = ''
        if obj.expiry_time:
            expiry_time_seconds = obj.expiry_time / 1000  # convert to millisecond
            expiry_time_formatted = datetime.fromtimestamp(expiry_time_seconds).strftime('%Y-%m-%d %H:%M:%S')
        
        data = [
            obj.remark, obj.server_ip, obj.up, obj.down, obj.total,
            obj.enable, expiry_time_formatted, obj.port, obj.uuid, obj.alter_id,
            obj.network, obj.network_type, obj.protocal, obj.config_url
        ]
        ws.append(data)

    # get current time and use it for file name
    current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'protocal_config_{current_time}.xlsx'

    # Create an HttpResponse and set the header information
    response = HttpResponse(content=save_virtual_workbook(wb),
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response

export_to_excel.short_description = "Export excel"



class DbServerAdmin(admin.ModelAdmin):
    list_display = ('server_name', 'server_ip')

class ProtocalConfigAdmin(admin.ModelAdmin):
    list_display = ('remark', 'port', 'server_ip', 'expiry_time_formatted')

    def expiry_time_formatted(self, obj):
        # obj 是每一行的 model 实例
        if obj.expiry_time:
            expiry_time_seconds = obj.expiry_time / 1000  # convert to millisecond
            return datetime.fromtimestamp(expiry_time_seconds).strftime('%Y-%m-%d %H:%M:%S')
        else:
            return ''

    expiry_time_formatted.short_description = 'Expiry Time'  # set column name

    # Customize the filter
    list_filter = ('server_ip',)

    # Add the custom action
    actions = [export_to_excel]


admin.site.register(DbServer, DbServerAdmin)
admin.site.register(ProtocalConfig, ProtocalConfigAdmin)