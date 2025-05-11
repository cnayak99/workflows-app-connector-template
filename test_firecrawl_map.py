import requests
import json
import time

# Firecrawl API constants
FIRECRAWL_API_KEY = "fc-1956059de87d45ceba43c29343869685"
FIRECRAWL_BASE_URL = "https://api.firecrawl.dev/v1"

print("=== Testing direct API call to Firecrawl /map endpoint ===")

# Test URL
test_url = "https://www.ycombinator.com/library"
print(f"Testing with URL: {test_url}")

# Build test data
payload = {
    "url": test_url,
}

# Set up API headers
headers = {
    "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
    "Content-Type": "application/json"
}

# Call Firecrawl Map API directly
print(f"Sending request to: {FIRECRAWL_BASE_URL}/map")
print(f"Payload: {json.dumps(payload, indent=2)}")

try:
    start_time = time.time()
    response = requests.post(
        f"{FIRECRAWL_BASE_URL}/map",
        headers=headers,
        json=payload,
        timeout=30  # Reasonable timeout
    )
    execution_time = time.time() - start_time
    
    print(f"Response status code: {response.status_code}")
    print(f"Execution time: {round(execution_time, 2)} seconds")
    
    if response.status_code == 200:
        result = response.json()
        print("Success! Retrieved results:")
        
        # Check for links in the response
        links = result.get("links", [])
        print(f"Found {len(links)} links")
        
        # Print sample links
        if links:
            print("Sample links:")
            for i, link in enumerate(links[:5]):
                print(f"  {i+1}. {link}")
    else:
        print(f"Error: {response.status_code}")
        try:
            error_data = response.json()
            print(f"Error details: {json.dumps(error_data, indent=2)}")
        except:
            print(f"Raw error: {response.text[:1000]}")
            
except Exception as e:
    print(f"Exception occurred: {str(e)}")

print("\n=== Testing connector endpoint for FirecrawlMapping ===")

# Local connector URL
connector_url = "http://localhost:2003/FirecrawlMapping/v1/execute"
print(f"Testing connector endpoint: {connector_url}")

# Request payload for connector
connector_payload = {
    "data": {
        "url": test_url,
    }
}

print(f"Sending payload to connector: {json.dumps(connector_payload, indent=2)}")

try:
    start_time = time.time()
    response = requests.post(
        connector_url,
        json=connector_payload,
        timeout=60  # Longer timeout for connector
    )
    execution_time = time.time() - start_time
    
    print(f"Response status code: {response.status_code}")
    print(f"Execution time: {round(execution_time, 2)} seconds")
    
    if response.status_code == 200:
        result = response.json()
        print("Success! Response structure:")
        print(f"Keys: {list(result.keys())}")
        
        # Check map_results content
        if "map_results" in result:
            map_results = result["map_results"]
            links = map_results.get("links", [])
            print(f"Found {len(links)} links in map_results")
            
            # Print metadata if available
            if "map_info" in result:
                print(f"Map info: {json.dumps(result['map_info'], indent=2)}")
            
            # Print sample links
            if links:
                print("Sample links:")
                for i, link in enumerate(links[:5]):
                    print(f"  {i+1}. {link}")
    else:
        print(f"Error: {response.status_code}")
        try:
            error_data = response.json()
            print(f"Error details: {json.dumps(error_data, indent=2)}")
        except:
            print(f"Raw error: {response.text[:1000]}")

except Exception as e:
    print(f"Exception occurred: {str(e)}") 