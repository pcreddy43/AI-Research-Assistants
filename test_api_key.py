import requests

API_URL = "http://localhost:8000/test_parallel"
API_KEY = "localdev123"  # Replace with your actual key if different

payload = {
    "question": "What is the capital of France?",
    "session_id": "test"
}
headers = {
    "x-api-key": API_KEY
}

response = requests.post(API_URL, json=payload, headers=headers)
print("Status Code:", response.status_code)
print("Raw Response:", response.text)
try:
    print("JSON Response:", response.json())
except Exception as e:
    print("Error decoding JSON:", e)
