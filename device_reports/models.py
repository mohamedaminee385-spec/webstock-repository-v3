from django.db import models
from django.conf import settings
# Import your existing device model here
from stock_operations.models import Device
from django.urls import reverse_lazy, reverse


class DeviceReport(models.Model):
    class IssueType(models.TextChoices):
        DAMAGED = 'DAMAGED', 'Physical Damage'
        MALFUNCTION = 'MALFUNCTION', 'Hardware Malfunction'
        MISSING = 'MISSING', 'Missing / Unaccounted'
        MAINTENANCE = 'MAINTENANCE', 'Requires Calibration/Service'

    class Status(models.TextChoices):
        OPEN = 'OPEN', 'Open'
        IN_REVIEW = 'IN_REVIEW', 'In Review'
        RESOLVED = 'RESOLVED', 'Resolved'
        REJECTED = 'REJECTED', 'Rejected'

    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='reports')
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    issue_type = models.CharField(max_length=20, choices=IssueType.choices, default=IssueType.MALFUNCTION)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    description = models.TextField()
    attachment = models.ImageField(upload_to='device_issues/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Report #{self.id} - {self.device} ({self.status})"


    def get_absolute_url(self):
        #return reverse_lazy("stock_operations:home_view")
        return reverse("home_view")