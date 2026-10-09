from django.urls import path
from .views import get_logs, export_audit_pdf

app_name = "audit"

urlpatterns = [
    path("", get_logs, name="get_logs"),
    path("rows/", export_audit_pdf, name="export_audit_pdf"),

]

