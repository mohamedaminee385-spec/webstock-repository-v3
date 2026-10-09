from abc import ABC, abstractmethod
from django.db import transaction
from audit.models import StockAuditLog
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from audit.middleware import get_current_user
from django import db
from stock_operations.models import Device
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


class SaveRecordsStrategy(ABC):

    @abstractmethod
    def save_record(self, *args, **kwargs):
        pass


class SaveGrpcRecords(SaveRecordsStrategy):

    def __init__(self, item, change, count, prev_qty, new_qty, action):
        self.item = item
        self.change = change
        self.count = count
        self.prev_qty = prev_qty
        self.new_qty = new_qty
        self.action = action

    def save_record(self):
        with transaction.atomic():
            StockAuditLog.objects.create(
                user=User.objects.get(username="grpc_client"),
                content_type=ContentType.objects.get_for_model(self.item),
                object_id=self.item.pk,
                # object_repr=str(instance),
                object_repr=self.item.name,
                action=self.action,
                quantity_change=self.change,
                previous_quantity=self.prev_qty,
                new_quantity=self.new_qty,
                # reason=getattr(instance, '_change_reason', 'Standard update')
            )
            #db.connections.close_all()


class SaveApplicationRecords(SaveRecordsStrategy):

    def __init__(self, item, change, count, prev_qty, new_qty, action):
        self.item = item
        self.change = change
        self.count = count
        self.prev_qty = prev_qty
        self.new_qty = new_qty
        self.action = action


    def save_record(self):

        user = get_current_user()
        with transaction.atomic():
            StockAuditLog.objects.create(
                user=user,
                content_type=ContentType.objects.get_for_model(self.item),
                object_id=self.item.pk,
                # object_repr=str(instance),
                object_repr=self.item.name,
                action=self.action,
                quantity_change=self.change,
                previous_quantity=self.prev_qty,
                new_quantity=self.new_qty,
                # reason=getattr(instance, '_change_reason', 'Standard update')
            )
            #db.connections.close_all()


class SaveRestApiRecords(SaveRecordsStrategy):

    def __init__(self, item, change, count, prev_qty, new_qty, action):
        self.item = item
        self.change = change
        self.count = count
        self.prev_qty = prev_qty
        self.new_qty = new_qty
        self.action = action


    def save_record(self):
        with transaction.atomic():
            StockAuditLog.objects.create(
                user=User.objects.get(username="rest_api"),
                content_type=ContentType.objects.get_for_model(self.item),
                object_id=self.item.pk,
                # object_repr=str(instance),
                object_repr=self.item.name,
                action=self.action,
                quantity_change=self.change,
                previous_quantity=self.prev_qty,
                new_quantity=self.new_qty,
                # reason=getattr(instance, '_change_reason', 'Standard update')
            )
            #db.connections.close_all()


class ContextSaving:

    def __init__(self, saving_strategy: SaveRecordsStrategy):
        self.saving_strategy = saving_strategy

    def record(self):
        if self.saving_strategy:
            self.saving_strategy.save_record()
