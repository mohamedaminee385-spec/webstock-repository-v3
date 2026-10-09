from rest_framework import serializers
from device_reports.models import DeviceReport

class DeviceReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceReport
        fields = ['id', 'device', 'reported_by', 'issue_type', 'status', 'description', 'created_at', 'updated_at']

