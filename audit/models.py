from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class StockAuditLog(models.Model):
    class ActionTypes(models.TextChoices):
        ADDITION = 'ADD', 'Addition'
        SUBTRACTION = 'SUB', 'Subtraction'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="User who initiated the change (if available)"
    )

    # Generic relation to log audit history for any inventory model (Item, StockLocation, etc.)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    #object_id = models.PositiveIntegerField()
    object_id = models.CharField(max_length=64)
    content_object = GenericForeignKey('content_type', 'object_id')

    object_repr = models.CharField(max_length=255, help_text="String representation of the item at log time")
    #action = models.CharField(max_length=30, choices=ActionTypes.choices)
    action = models.TextField(max_length=30)

    quantity_change = models.IntegerField(help_text="Positive for addition, negative for subtraction")
    previous_quantity = models.IntegerField()
    new_quantity = models.IntegerField()

    #reason = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['content_type', 'object_id', '-timestamp']),
        ]

    def __str__(self):
        return f"{self.object_repr} | {self.action} | {self.quantity_change:+d} at {self.timestamp.strftime( '%Y-%m-%d %H:%M')}"

