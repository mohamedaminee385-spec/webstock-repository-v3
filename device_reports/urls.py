from django.urls import path
from .views import CreateDeviceReportView, DeviceReportListView, DeviceReportDetailView

app_name = 'device_reports'

urlpatterns = [
    path('', CreateDeviceReportView.as_view(), name='report_create'),
    path('reports/', DeviceReportListView.as_view(), name='reports_list'),
    path('reports/<int:pk>/', DeviceReportDetailView.as_view(), name='report_detail'),
]