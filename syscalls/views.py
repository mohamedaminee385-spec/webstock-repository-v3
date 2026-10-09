from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import requests
import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@login_required
def render_phishing_page(request):
    return render(request, "phishing_page.html", {})


@csrf_exempt
def execute_proxy(request):
    # 1. Handle browser CORS / PNA preflight checks
    if request.method == "OPTIONS":
        response = HttpResponse(status=200)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, X-CSRFToken, ngrok-skip-browser-warning"
        response["Access-Control-Allow-Private-Network"] = "true"
        return response

    # 2. Process actual POST request from JavaScript
    if request.method == "POST":
        try:
            body = json.loads(request.body.decode('utf-8'))

            # Forward payload locally to your Flask agent
            flask_response = requests.post(
                "http://127.0.0.1:5000/run",
                json=body,
                timeout=10
            )

            response = JsonResponse(flask_response.json(), status=flask_response.status_code)
            response["Access-Control-Allow-Origin"] = "*"
            return response

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)