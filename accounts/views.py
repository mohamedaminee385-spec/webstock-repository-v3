from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
import time
# Create your views here.


def register(request):
    if request.method == 'POST':
        # 1. Extract raw POST data
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        # 2. Manual Validation
        errors = []
        if not username or not email or not password:
            errors.append("All fields are required.")

        if password != confirm_password:
            errors.append("Passwords do not match.")

        if User.objects.filter(username=username).exists():
            errors.append("Username is already taken.")

        if User.objects.filter(email=email).exists():
            errors.append("Email is already registered.")

        # 3. Handle Errors or Save User
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'register.html', {
                'username': username,
                'email': email
            })

        # 4. Create User (Always use create_user to properly hash passwords)
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.save()

        #messages.success(request, "Account created successfully! You can now log in.")

        return redirect('accounts:login')


        # GET request: render blank page
    return render(request, 'register.html')
    #return redirect('register_view')

def mylogin(request):
    # Redirect logged-in users away from the login page
    #if request.user.is_authenticated:
    #    return redirect('home_view')

    error_message = None

    if request.method == 'POST':
        # Read raw input from the HTTP request body
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            error_message = "Please enter both username and password."
        else:
            # Check credentials against the database backend
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Create the session and attach user to request
                login(request, user)

                # Handle target redirect if provided, else default to 'home'
                #next_url = request.GET.get('next', 'home')
                return redirect("stock_operations:home_view")
            else:
                error_message = "Invalid username or password."

    return render(request, 'login.html', {'error': error_message})