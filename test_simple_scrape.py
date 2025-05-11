import requests
import json

# Test the Firecrawl connector with a simple URL scraping request
print("=== Testing Firecrawl Connector with Simple URL Scraping ===")

# Basic payload with just the URL
simple_payload = {
    "url": "https://www.ycombinator.com/about"
}

print(f"Sending simple request with: {json.dumps(simple_payload, indent=2)}")

# Make the request to the connector
connector_url = "http://localhost:2003/Firecrawl/v1/execute"
response = requests.post(connector_url, json=simple_payload)

print(f"Response status: {response.status_code}")

if response.status_code == 200:
    result = response.json()
    print("\nSuccess! Response received.")
    
    # Print the structure of the response
    if "result" in result:
        print(f"Keys in result: {list(result['result'].keys())}")
        if "data" in result["result"]:
            print(f"Data keys: {list(result['result']['data'].keys())}")
    
    # Print the content
    if "result" in result and "data" in result["result"] and "markdown" in result["result"]["data"]:
        content = result["result"]["data"]["markdown"]
        print(f"\nContent sample (first 300 chars):")
        print(content[:300])
    else:
        print("\n❌ No markdown content found in the response")
else:
    print("\n❌ Request failed")
    try:
        error = response.json()
        print(json.dumps(error, indent=2))
    except:
        print(response.text[:500])

# Test with exclude_tags parameter
exclude_payload = {
    "url": "https://www.ycombinator.com/about",
    "exclude_tags": "#introduction"
}

print("\n=== Testing with exclude_tags parameter ===")
print(f"Sending request with exclude_tags: {json.dumps(exclude_payload, indent=2)}")

response = requests.post(connector_url, json=exclude_payload)
print(f"Response status: {response.status_code}")

if response.status_code == 200:
    result = response.json()
    print("\nSuccess! Response received.")
    
    # Print the content
    if "result" in result and "data" in result["result"] and "markdown" in result["result"]["data"]:
        content = result["result"]["data"]["markdown"]
        print(f"\nContent sample with exclude_tags (first 300 chars):")
        print(content[:300])
        
        # Check if INTRODUCTION is excluded
        if "INTRODUCTION" not in content:
            print("\n✅ Success: 'INTRODUCTION' section is excluded")
        else:
            print("\n❌ 'INTRODUCTION' section is still present")
    else:
        print("\n❌ No markdown content found in the response")
else:
    print("\n❌ Request failed")
    try:
        error = response.json()
        print(json.dumps(error, indent=2))
    except:
        print(response.text[:500]) 