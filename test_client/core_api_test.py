import requests

core_endpoint="http://localhost:8000/api/contacts/"

get_response = requests.get(core_endpoint, json={})
print(get_response.json())