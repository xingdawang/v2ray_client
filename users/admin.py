from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from cluster.models import ProtocalConfig

class CustomUserAdmin(UserAdmin):

    # Display the following fields in the user list in the admin panel
    list_display = ('username', 'date_joined', 'protocol_config')
    # Make 'date_joined' sortable
    # ordering = ('date_joined',)

    # reorder sections
    # Unpack the original fieldsets
    original_fieldsets = UserAdmin.fieldsets

    # Include additional fields in the user detail view
    config_url_fieldsets = ('Config URL', {'fields': ('protocol_config',)})

    # Insert the new fieldset in the second position
    fieldsets = (
        original_fieldsets[0],  # The first original fieldset
        config_url_fieldsets,   # The new fieldset for protocol_config
    ) + original_fieldsets[1:]  # The rest of the original fieldsets

    # Customize the filter
    list_filter = ('date_joined', 'protocol_config')


# Register the customized admin
admin.site.register(CustomUser, CustomUserAdmin)