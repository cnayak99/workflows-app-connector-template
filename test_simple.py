import requests
import json

# Test Firecrawl endpoint with correct format
payload = {
    "url": "https://www.ycombinator.com/about",
    "formats": ["markdown"]
}

print("Testing Firecrawl endpoint with formats parameter...")
response = requests.post("http://localhost:2003/Firecrawl/v1/execute", json=payload)
print(f"Status code: {response.status_code}")

if response.status_code == 200:
    print("Success! Response:")
    result = response.json()
    print(json.dumps(result, indent=2)[:500] + "...")
else:
    print("Error response:")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text[:1000])

# Test with JSON extraction
extract_payload = {
    "url": "https://www.ycombinator.com/companies/industry/consumer",
    "extract_prompt": "Extract a list of YC consumer companies"
}

print("\nTesting with extract_prompt parameter...")
response = requests.post("http://localhost:2003/Firecrawl/v1/execute", json=extract_payload)
print(f"Status code: {response.status_code}")

if response.status_code == 200:
    print("Success! Response:")
    result = response.json()
    if "result" in result and "data" in result["result"] and "json" in result["result"]["data"]:
        print("Extracted JSON:")
        print(json.dumps(result["result"]["data"]["json"], indent=2)[:500] + "...")
    else:
        print("Response structure:")
        print(json.dumps(result, indent=2)[:500] + "...")
else:
    print("Error response:")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text[:1000]) 