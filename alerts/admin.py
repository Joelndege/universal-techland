from django.contrib import admin
from .models import Alert

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    def short_desc(self, obj):
        return obj.description[:50]
    short_desc.short_description = 'Description (short)'

    list_display = ('id', 'title', 'priority', 'severity', 'status', 'location', 'short_desc', 'created_at')
    readonly_fields = ('created_at',)
