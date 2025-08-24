import requests

url = "http://127.0.0.1:8000/ask_multi"
headers = {
    "Content-Type": "application/json",
    "x-api-key": "localdev123"
}
data = {
    "question": "Summarize my uploaded doc and compare with latest web findings",
    "session_id": "demo1"
}
response = requests.post(url, headers=headers, json=data)
print(response.text)
