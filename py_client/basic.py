import requests

endpoint="http://localhost:8000/api/contacts/"

get_response = requests.get(endpoint, json={"title": "Abc123", "content": "Hello world", "price": "abc134"})
print(get_response.json())