import requests
import json

core_endpoint="http://localhost:8000/contacts/"

response = requests.get(core_endpoint)

print(response.json())