import requests

url = "http://127.0.0.1:8000/team_ask"
headers = {
    "Content-Type": "application/json",
    "x-api-key": "localdev123"
}
data = {
    "question": "Summarize recent agentic AI research and provide 5 takeaways",
    "session_id": "team1"
}
response = requests.post(url, headers=headers, json=data)
print(response.text)
