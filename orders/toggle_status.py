import requests

# 1. Base configuration
BASE_URL = "http://127.0.0.1:8000"  # Change to your host/port
LOGIN_URL = f"{BASE_URL}/admin/login/"
TOGGLE_URL_TEMPLATE = f"{BASE_URL}/orders/toggle-status/{{order_id}}/"

# Admin credentials
USERNAME = "moham"
PASSWORD = "Pass!@12"

# Use a Session instance to persist cookies automatically
session = requests.Session()

# 2. Get the initial login page to retrieve the CSRF token cookie
login_page_response = session.get(LOGIN_URL)
csrf_token = session.cookies.get("csrftoken")

# 3. Authenticate with the Django admin login
login_data = {
    "username": USERNAME,
    "password": PASSWORD,
    "csrfmiddlewaretoken": csrf_token,
    "next": "/admin/",
}

# Standard Django forms require the Referer header during login POST
headers = {"Referer": LOGIN_URL}

login_response = session.post(LOGIN_URL, data=login_data, headers=headers)

# Check if authentication succeeded
if login_response.status_code == 200 and "sessionid" in session.cookies:
    print("Authentication successful!")
else:
    print("Failed to authenticate. Check your credentials.")
    exit()

# 4. Toggle order status for a specific order (e.g., ID = 1)
order_id = 16
toggle_url = TOGGLE_URL_TEMPLATE.format(order_id=order_id)

# Update CSRF token from active cookies
csrf_token = session.cookies.get("csrftoken")

# Set required headers for Django POST requests
post_headers = {
    "Referer": toggle_url,
    "X-CSRFToken": csrf_token,
}

toggle_data = {
    "csrfmiddlewaretoken": csrf_token,
}

# Execute POST request to toggle status
response = session.post(
    toggle_url,
    data=toggle_data,
    headers=post_headers,
    allow_redirects=True,
)

if response.status_code == 200:
    print(f"Successfully toggled status for Order #{order_id}!")
else:
    print(
        f"Failed to toggle status. HTTP Status Code: {response.status_code}"
    )