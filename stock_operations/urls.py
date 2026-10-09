from django.urls import path, include
from . import views as views
from stock_operations.operations import StockOps

stock_service = StockOps()
app_name = 'stock_operations'

urlpatterns = [
    path('api/check-stock/', views.warning_view, name='check_stock_warning'),
    path("", views.HomeView.as_view(stock_ops=stock_service), name="home_view"),
    path("redirected/", views.redirect_view, name="redirect_view"),
]

