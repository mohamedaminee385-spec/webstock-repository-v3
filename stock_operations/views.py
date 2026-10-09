from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import  Device
from django.views.decorators.csrf import csrf_protect
from django.middleware.csrf import get_token
from django.contrib import messages
from django.db import transaction
from typing import Optional
import uuid
from django.contrib.auth.decorators import login_required
from .utils import Awaitable
from django.contrib import messages
from .operations import add, substruct, StockOps, StockOpsService
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
import os
# Create your views here.

devices = ["Scanner", "Monitor", "Desktop", "Laptop", "Printer"]

@csrf_protect
def home3(request):
    if request.method == "POST":
        action = request.POST.get('action')
        sc = request.POST.get('selected_device')
        n = int(request.POST.get('entry_value'))
        if action == 'add':
            add(sc, n)
        elif action == 'substruct':
            substruct(sc, n)
        return redirect("redirect_view")
    items = Device.objects.all()
    return render(request, "home.html", {"devices": devices, "items": items, "bg": "#f9f9f9"})


def home2(request):
    if request.method == "POST":
        action = request.POST.get('action')
        sc = request.POST.get('selected_device')
        n = int(request.POST.get('entry_value'))
        if action == 'add':
            add(sc, n)
        elif action == 'substruct':
            substruct(sc, n)
    items = Device.objects.all()
    return render(request, "home.html", {"devices": devices, "items": items, "bg": "#f9f9f9"})


class HomeView(LoginRequiredMixin, View):
    template_name = "home1.html"
    stock_ops: Optional[StockOpsService] = None

    def __init__(self, stock_ops: Optional[StockOpsService] = None, **kwargs):
        super().__init__(**kwargs)
        # Fall back to default instance if none was injected
        self.stock_ops = stock_ops or self.stock_ops or StockOps()

    def _generate_form_token(self, request):
        """Helper method to generate and set a new session form token."""
        token = str(uuid.uuid4())
        request.session['form_token'] = token
        return token

    def get_context_data(self, request):
        """Helper method to construct consistent context data."""
        items = Device.objects.all()
        return {
            "devices": devices,  # Note: ensure 'devices' is defined in your scope/module
            "items": items,
            "form_token": self._generate_form_token(request),
        }

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        submitted_token = request.POST.get('form_token')
        stored_token = request.session.pop('form_token', None)

        # Check for invalid/missing token (double submit protection)
        if not stored_token or submitted_token != stored_token:
            print("#########")
            print(submitted_token)
            print(stored_token)
            context = self.get_context_data(request)
            return render(request, self.template_name, context)

        action = request.POST.get('action')
        sc = request.POST.get('selected_device')
        n = int(request.POST.get('entry_value'))

        if action == 'add':
            self.stock_ops.add(sc, n, request)
        elif action == 'substruct':  # Note: keep spelling aligned with your existing function
            self.stock_ops.subtract(sc, n, request)

        context = self.get_context_data(request)
        return render(request, self.template_name, context)

@login_required
def home(request):
    if request.method == "POST":
        submitted_token = request.POST.get('form_token')
        stored_token = request.session.pop('form_token', None)

        if not stored_token or submitted_token != stored_token:
            #messages.warning(request, "Form already submitted or session expired.")
            #return redirect("redirected/")
            print("#########")
            print(submitted_token)
            print(stored_token)
            items = Device.objects.all()
            token = str(uuid.uuid4())
            request.session['form_token'] = token
            return render(request, "home.html", {"devices": devices, "items": items, "bg": "#f9f9f9", "form_token": request.session.get('form_token')})
        action = request.POST.get('action')
        sc = request.POST.get('selected_device')
        n = int(request.POST.get('entry_value'))
        if action == 'add':
            add(sc, n, request)
        elif action == 'substruct':
            substruct(sc, n, request)
            #return redirect("redirected/")

    token = str(uuid.uuid4())
    request.session['form_token'] = token
    items = Device.objects.all()
    return render(request, "home.html", {"devices": devices, "items": items, "bg": "#f9f9f9", "form_token": request.session.get('form_token')})


def redirect_view(request):
    return render(request, "redirected.html")


def warning_view(request):
    print("####RUN####")
    obj = Awaitable()
    warning_msg = obj.waiter()
    #return render(request, "warning.html", {"warning": warning})
    return JsonResponse({"has_warning": True, "message": warning_msg})
