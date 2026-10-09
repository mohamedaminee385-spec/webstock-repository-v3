from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from rest_framework import status
from rest_framework.response import Response
from device_reports.serializers import DeviceReportSerializer
from .forms import DeviceReportForm
from .models import DeviceReport
from rest_framework.decorators import api_view

class CreateDeviceReportView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = DeviceReport
    form_class = DeviceReportForm
    template_name = 'report_form.html'
    #success_url = reverse_lazy('device_reports:report_list')
    success_url = "/report/new/reports/"
    success_message = "Your report for %(device)s has been submitted successfully."

    def form_valid(self, form):
        # Automatically attach the currently logged-in user
        form.instance.reported_by = self.request.user
        return super().form_valid(form)


class DeviceReportListView(LoginRequiredMixin, ListView):
    model = DeviceReport
    template_name = 'device_report_list.html'  # Adjust path to match your app template structure
    context_object_name = 'reports'
    paginate_by = 10  # Optional: limits records per page

    def get_queryset(self):
        # Optimizes database query by prefetching related foreign key objects
        return (
            super()
            .get_queryset()
            .select_related('device', 'reported_by')
            .order_by('-created_at')
        )


class DeviceReportDetailView(LoginRequiredMixin, DetailView):
    model = DeviceReport
    template_name = 'device_report_detail.html'
    context_object_name = 'report'

    def get_queryset(self):
        # Prefetch related data to optimize the detail query
        return super().get_queryset().select_related('device', 'reported_by')