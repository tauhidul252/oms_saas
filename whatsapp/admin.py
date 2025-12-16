from django.contrib import admin
from .models import MessageLog

@admin.register(MessageLog)
class MessageLogAdmin(admin.ModelAdmin):
    list_display = ("customer", "phone", "sent_at", "status")
    search_fields = ("customer__name", "phone", "message")
    list_filter = ("status", "sent_at")
