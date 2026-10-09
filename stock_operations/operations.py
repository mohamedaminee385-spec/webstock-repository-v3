from django.db import transaction
from .models import  Device
from django.contrib import messages
from abc import ABC, abstractmethod


class StockOpsService(ABC):

    @abstractmethod
    def add(self, sc: str, n: int, request):
        pass

    @abstractmethod
    def subtract(self, sc: str, n: int, request):
        pass


class StockOps(StockOpsService):

    def add(self, sc, n, request):
        with transaction.atomic():
            try:
                device = Device.objects.get(name=sc)
                device.stock_number = device.stock_number + n
                device.save()
                print("Device updated successfully!")
            except Device.DoesNotExist:
                print("Device not found.")


    def subtract(self, sc, n, request):
        with transaction.atomic():
            try:
                device = Device.objects.get(name=sc)
                if device.stock_number < n:
                    messages.error(request, "The quantity to subtruct is greater than stock quantity")
                    return
                device.stock_number = device.stock_number - n
                device.save()
                print("Device updated successfully!")
            except Device.DoesNotExist:
                print("Out of stock or device not found.")


def add(sc, n, request):
    with transaction.atomic():
        try:
            device = Device.objects.get(name=sc)
            device.stock_number = device.stock_number + n
            device.save()
            print("Device updated successfully!")
        except Device.DoesNotExist:
            print("Device not found.")


def substruct(sc, n, request):
    with transaction.atomic():
        try:
            device = Device.objects.get(name=sc)
            if device.stock_number < n:
                messages.error(request, "The quantity to subtruct is greater than stock quantity")
                return
            device.stock_number = device.stock_number - n
            device.save()
            print("Device updated successfully!")
        except Device.DoesNotExist:
            print("Out of stock or device not found.")