from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.template.defaultfilters import lower
from django.views.decorators.http import require_POST

from orders.models import Order
from stock_operations.models import Device
from .forms import OrderForm

def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

@user_passes_test(is_admin, login_url='/admin/login/')
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.created_by = request.user
            order.save()
            return redirect('orders:order_success')
    else:
        form = OrderForm()

    return render(request, 'create_order.html', {'form': form})


def order_success(request):
    return render(request, "order_success.html", {})


@user_passes_test(is_admin, login_url='/admin/login/')
def order_list(request):
    #status_filter = request.GET.get('status', '')

    orders = Order.objects.all().order_by('-created_at')

    #if status_filter in [Order.STATUS_PENDING, Order.STATUS_FINALIZED]:
    #    orders = orders.filter(status=status_filter)

    #context = {
    #    'orders': orders,
    #    'current_status': status_filter,
    #    'status_pending': Order.STATUS_PENDING,
    #    'status_finalized': Order.STATUS_FINALIZED,
    #}
    context = {
        'orders': orders
    }
    return render(request, 'order_list.html', context)


@user_passes_test(is_admin, login_url='/admin/login/')
@require_POST
def toggle_order_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    print(order)
    category = lower(order.category)
    res = category[:1].upper() + category[1:]
    print(category)

    if order.status == Order.STATUS_PENDING:
        # 1. Update order status
        order.status = Order.STATUS_FINALIZED
        order.save()

        # 2. Safely get the matching Device instance
        try:
            # If Device.name matches category key (e.g., 'DESKTOP')

            device_obj = Device.objects.get(name=res)
            #print(device_obj)
            # If Device.name matches display name (e.g., 'Desktop'), use this instead:
            #device_obj = Device.objects.get(name=order.get_category_display())

            device_obj.stock_number += order.quantity
            device_obj.save()
        except Device.DoesNotExist:
            messages.error(request, f"Device type '{order.category}' not found in inventory.")

    else:
        # Logic when reopening from Finalized back to Pending
        order.status = Order.STATUS_PENDING
        order.save()

        try:
            device_obj = Device.objects.get(name=res)
            device_obj.stock_number -= order.quantity  # Revert stock if needed
            device_obj.save()
        except Device.DoesNotExist:
            pass

    return redirect('orders:order_list')