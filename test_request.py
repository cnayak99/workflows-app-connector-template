import requests
import json

# The payload to send
payload = {
    "data": {
        "url": "https://www.ycombinator.com/",
        "extract_main_content": True
    }
}

# Print what we're sending
print(f"Sending payload: {json.dumps(payload, indent=2)}")

# Send the request
url = "http://localhost:2003/Firecrawl/v1/execute"
headers = {"Content-Type": "application/json"}
response = requests.post(url, json=payload, headers=headers)

# Print the response
print(f"Status code: {response.status_code}")
try:
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except:
    print(f"Raw response: {response.text}") 