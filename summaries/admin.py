from django.contrib import admin
from .models import Summary


@admin.register(Summary)
class SummaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'audio_file', 'created_at')
    readonly_fields = ('transcript', 'summary', 'action_items')
