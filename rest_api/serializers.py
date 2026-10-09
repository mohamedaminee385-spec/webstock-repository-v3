from rest_framework import serializers

from device_reports.models import DeviceReport
from stock_operations.models import Device

class StockItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'name', 'stock_number']

class StockActionSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1, help_text="Amount to add or subtract")


class DeviceReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceReport
        fields = ['id', 'device', 'reported_by', 'issue_type', 'status', 'description', 'created_at', 'updated_at']
