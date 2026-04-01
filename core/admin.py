from django.contrib import admin
from core.models import MFAResetEvent, MitIDLoginEvent


@admin.register(MitIDLoginEvent)
class MitIDLoginEventAdmin(admin.ModelAdmin):
    list_display = ("created_at", "username", "status", "ticket_present", "ip_address")
    list_filter = ("status", "ticket_present", "created_at")
    search_fields = ("username", "failure_reason", "ip_address")
    readonly_fields = (
        "created_at",
        "username",
        "status",
        "service_url",
        "failure_reason",
        "ticket_present",
        "session_key",
        "ip_address",
        "user_agent",
    )


@admin.register(MFAResetEvent)
class MFAResetEventAdmin(admin.ModelAdmin):
    list_display = ("created_at", "username", "status", "ip_address")
    list_filter = ("status", "created_at")
    search_fields = ("username", "failure_reason", "result_message", "ip_address")
    readonly_fields = (
        "created_at",
        "username",
        "status",
        "attempted_methods",
        "existing_methods",
        "result_message",
        "failure_reason",
        "session_key",
        "ip_address",
        "user_agent",
    )
