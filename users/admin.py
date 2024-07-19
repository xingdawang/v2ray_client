from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from cluster.models import ProtocalConfig
from django.utils.translation import gettext_lazy as _


class CustomUserAdmin(UserAdmin):

    # Display the following fields in the user list in the admin panel
    list_display = ('username', 'date_joined', 'customer_group', 'protocol_config')
    # Make 'date_joined' sortable
    # ordering = ('date_joined',)

    # reorder sections

    fieldsets = (
        (_('Customer Profile'), {
            'fields': ('username', 'first_name', 'last_name', 'email', 'customer_group', 'note')}),
        (_('Config URL'), {
            'fields': ('protocol_config',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined')}),
    )

    # Customize the filter
    list_filter = ('date_joined', 'customer_group')


# Register the customized admin
admin.site.register(CustomUser, CustomUserAdmin)