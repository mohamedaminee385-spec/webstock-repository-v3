from django.urls import path, include
from . import views as views

app_name = 'orders'

urlpatterns = [
    path("create/", views.create_order, name="create_order"),
    path("success/", views.order_success, name="order_success"),
    path("list/", views.order_list, name="order_list"),
    path('toggle-status/<int:pk>/', views.toggle_order_status, name='toggle_order_status'),
]