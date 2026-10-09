import requests

# Set endpoint URL
ngrok_url = "https://morale-nervy-swooned.ngrok-free.dev/api/stock/Scanner/add/"
url = "http://127.0.0.1:8000/api/stock/Desktop/add/"
get_url = "http://127.0.0.1:8000/api/stock/"
get_reports_url = "http://127.0.0.1:8000/api/stock/get/reports/"
set_status_url = "http://127.0.0.1:8000/api/stock/setstatus/resolved/38/"
# Send POST request with JSON payload
#payload = {"amount": 20}
#response = requests.post(url, json=payload)
#response = requests.get(get_url)
#response = requests.get(get_reports_url)
response = requests.post(set_status_url)
# Verify results
print("Status Code: " + str(response.status_code))
print("Response Body: " + str(response.json()))