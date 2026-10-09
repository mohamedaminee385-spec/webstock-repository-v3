from django.urls import path
from . import views

urlpatterns = [
    # Full stock status
    path('', views.get_stock_status, name='stock-status'),
    path('<str:device>/add/', views.add_stock, name='add-stock'),
    path('<str:device>/subtract/', views.subtract_stock, name='subtract-stock'),
    path('get/reports/', views.get_devices_reports, name='get-reports'),
    path('setstatus/<str:status>/<int:report>/', views.set_status, name='set-status'),
    path('wait/keypress/', views.getdata, name='get-data')
]