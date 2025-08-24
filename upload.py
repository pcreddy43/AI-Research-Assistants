import requests

url = "http://127.0.0.1:8000/upload"
headers = {"x-api-key": "localdev123"}
files = {"file": open(r"E:/Movies/Computer_Vision_Object_Detection-Car.pdf", "rb")}

response = requests.post(url, headers=headers, files=files)
print(response.text)
