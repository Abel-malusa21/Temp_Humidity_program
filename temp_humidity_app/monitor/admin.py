from django.contrib import admin
from .models import TempHumidityRecord

class TempHumidityRecordAdmin(admin.ModelAdmin):
    # Define the fields to be displayed in the list view
    list_display = ('id', 'temperature', 'humidity', 'timestamp')
    
    # Add filters for easy navigation in the admin panel
    list_filter = ('timestamp',)
    
    # Search functionality to find records based on temperature or humidity
    search_fields = ('temperature', 'humidity')
    
    # Define how the records should be ordered
    ordering = ('-timestamp',)  # Most recent records first

    # Optional: Add read-only fields if certain fields should not be edited
    readonly_fields = ('timestamp',)

    # Add additional options for editing in the admin form
    fieldsets = (
        (None, {
            'fields': ('temperature', 'humidity')
        }),
        ('Advanced options', {
            'classes': ('collapse',),  # Collapsible fieldset
            'fields': ('timestamp',),
        }),
    )

# Register the TempHumidityRecord model with the customized admin view
admin.site.register(TempHumidityRecord, TempHumidityRecordAdmin)
