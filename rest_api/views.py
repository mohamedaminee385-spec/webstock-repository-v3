from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import rest_framework
from device_reports.models import DeviceReport
from stock_operations.models import Device
from .serializers import StockItemSerializer, StockActionSerializer, DeviceReportSerializer
from strategy.save_records import SaveRestApiRecords, ContextSaving


# Endpoint 1: Get full status of all stock items
@api_view(['GET'])
def get_stock_status(request):
    try:
        items = Device.objects.all()
        serializer = StockItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response("", rest_framework.status.HTTP_401_UNAUTHORIZED)


# Endpoint 2: Add elements to stock
@api_view(['POST'])
def add_stock(request, device):
    item = get_object_or_404(Device, name=device)
    prev_qty = item.stock_number
    serializer = StockActionSerializer(data=request.data)

    if serializer.is_valid():
        amount = serializer.validated_data['amount']
        item.stock_number += amount
        item.save()
        new_qty = prev_qty + amount
        context = ContextSaving(SaveRestApiRecords(item=item,
                                                action="Addition",
                                                change=amount,
                                                count=0,
                                                prev_qty=prev_qty,
                                                new_qty=new_qty))
        context.record()
        return Response(StockItemSerializer(item).data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Endpoint 3: Subtract elements from stock
@api_view(['POST'])
def subtract_stock(request, device):
    item = get_object_or_404(Device, name=device)
    serializer = StockActionSerializer(data=request.data)
    prev_qty = item.stock_number
    if serializer.is_valid():
        amount = serializer.validated_data['amount']
        if item.stock_number < amount:
            return Response(
                {"error": "Insufficient stock available"},
                status=status.HTTP_400_BAD_REQUEST
            )

        item.stock_number -= amount
        item.save()
        new_qty = prev_qty - amount
        context = ContextSaving(SaveRestApiRecords(item=item,
                                                   action="Subtraction",
                                                   change=-amount,
                                                   count=0,
                                                   prev_qty=prev_qty,
                                                   new_qty=new_qty))
        context.record()
        return Response(StockItemSerializer(item).data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_devices_reports(request):
    try:
        reports = DeviceReport.objects.all()
        serializer = DeviceReportSerializer(reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response("", rest_framework.status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def set_status(request, status, report):
    try:
        rep = get_object_or_404(DeviceReport, id=report)
        if status == "open":
            st = DeviceReport.Status.OPEN
        elif status == "in_review":
            st = DeviceReport.Status.IN_REVIEW
        elif status == "resolved":
            st = DeviceReport.Status.RESOLVED
        else:
            st = DeviceReport.Status.REJECTED
        rep.status = st
        rep.save()
        return Response(DeviceReportSerializer(rep).data, status=rest_framework.status.HTTP_200_OK)
    except Exception as e:
        return Response("", rest_framework.status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
def getdata(request):
    print("Received Data")
    raw_data = request.data
    print(raw_data)
    return Response({"message": "Data received", "data": raw_data}, status=status.HTTP_200_OK)
