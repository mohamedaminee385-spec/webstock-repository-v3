from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DeviceReport

@receiver(post_save, sender=DeviceReport)
def update_device_status_on_report(sender, instance, created, **kwargs):
    if created and instance.status == DeviceReport.Status.OPEN:
        # Change status or flag on your inventory model
        device = instance.device
        device.is_available = False
        device.save(update_fields=['is_available'])