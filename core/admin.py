from django.contrib import admin

from core.models import FunnelLead, FunnelLeadAttachment


class FunnelLeadAttachmentInline(admin.TabularInline):
    model = FunnelLeadAttachment
    extra = 0
    readonly_fields = ("original_name", "uploaded_at")


@admin.register(FunnelLead)
class FunnelLeadAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "full_name",
        "telephone",
        "city",
        "delivery_preference",
        "dent_count",
        "utm_source",
        "email_sent",
        "created_at",
    )
    list_filter = ("email_sent", "language", "utm_source", "created_at")
    search_fields = ("email", "full_name", "telephone", "city")
    readonly_fields = ("created_at",)
    inlines = [FunnelLeadAttachmentInline]
