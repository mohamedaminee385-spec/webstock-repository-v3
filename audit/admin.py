from django.contrib import admin
from .models import StockAuditLog

@admin.register(StockAuditLog)
class StockAuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'object_repr', 'action', 'quantity_change', 'previous_quantity', 'new_quantity', 'user')
    list_filter = ('action', 'timestamp', 'content_type')
    search_fields = ('object_repr', 'user__username', 'reason')
    date_hierarchy = 'timestamp'

    # Prevent admin modification or creation of logs
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
