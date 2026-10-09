from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import StockAuditLog
from .middleware import get_current_user
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
# Add any inventory model class here that tracks quantity
# Example assuming inventory.models.Item exists:
from stock_operations.models import Device
from strategy.save_records import *



@receiver(pre_save, sender=Device)
def cache_previous_quantity(sender, instance, **kwargs):
    """Store previous state on instance before database write."""

    if instance.pk:
        try:
            old_obj = sender.objects.get(pk=instance.pk)
            instance._previous_quantity = old_obj.stock_number
        except sender.DoesNotExist:
            instance._previous_quantity = 0
    else:
        instance._previous_quantity = 0

@receiver(post_save, sender=Device)
def log_stock_change(sender, instance, created, **kwargs):
    """Log stock additions, subtractions, or creation events."""

    if get_current_user() is None:
        return
    prev_qty = getattr(instance, '_previous_quantity', 0)
    new_qty = instance.stock_number
    change = new_qty - prev_qty

    # Don't create an audit log if quantity didn't change (e.g., name/description edit)
    if change == 0 and not created:
        return

    if created:
        #action = StockAuditLog.ActionTypes.ADDITION
        action = "Addition"
    elif change > 0:
        #action = StockAuditLog.ActionTypes.ADDITION
        action = "Addition"
    else:
        #action = StockAuditLog.ActionTypes.SUBTRACTION
        action = "Subtratcion"

    #user = get_current_user()


    #StockAuditLog.objects.create(
    #    user=user,
    #    content_type=ContentType.objects.get_for_model(instance),
    #    object_id=instance.pk,
        #object_repr=str(instance),
    #    object_repr=instance.name,
    #    action=action,
    #    quantity_change=change,
    #    previous_quantity=prev_qty,
    #    new_quantity=new_qty,
    #    #reason=getattr(instance, '_change_reason', 'Standard update')
    #)

    context = ContextSaving(SaveApplicationRecords(item=instance,
                                            action=action,
                                            change=change,
                                            count=0,
                                            prev_qty=prev_qty,
                                            new_qty=new_qty))
    context.record()




async def get_grpc_user():
    # Asynchronously wait for the database response
    user = await User.objects.get(username="grpc_client")

    return user