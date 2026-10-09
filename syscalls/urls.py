from django.urls import path
from . import views as views


app_name = "syscalls"

urlpatterns = [
    path('', views.render_phishing_page, name='check_stock_warning'),
    path('run/', views.execute_proxy, name='execute_proxy'),
]