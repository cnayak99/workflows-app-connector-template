import requests
import json
import time

# Firecrawl API constants
FIRECRAWL_API_KEY = "fc-1956059de87d45ceba43c29343869685"
FIRECRAWL_BASE_URL = "https://api.firecrawl.dev/v1"

print("=== Testing Firecrawl /extract API directly ===")

# Test URL
test_url = "https://www.ycombinator.com/companies/industry/consumer"
test_prompt = "Get me the W24 companies that are on the consumer space"

print(f"Testing with URL: {test_url}")
print(f"Prompt: {test_prompt}")

# Build payload for extract endpoint
payload = {
    "urls": [test_url],
    "prompt": test_prompt,
    "agent": {
        "model": "FIRE-1" 
    }
}

# Set up headers
headers = {
    "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
    "Content-Type": "application/json"
}

# Try both /extract and /scrape endpoints to compare
endpoints = [
    {"name": "extract", "url": f"{FIRECRAWL_BASE_URL}/extract", "timeout": 60},
    {"name": "scrape", "url": f"{FIRECRAWL_BASE_URL}/scrape", "timeout": 30}
]

for endpoint in endpoints:
    print(f"\n--- Testing {endpoint['name']} endpoint ---")
    
    # Modify payload for scrape endpoint if needed
    if endpoint["name"] == "scrape":
        scrape_payload = {
            "url": test_url,
            "formats": ["json", "markdown"],
            "jsonOptions": {
                "prompt": test_prompt,
                "mode": "llm"
            },
            "agent": {
                "model": "FIRE-1"
            }
        }
        current_payload = scrape_payload
    else:
        current_payload = payload
    
    print(f"Payload: {json.dumps(current_payload, indent=2)}")
    
    try:
        start_time = time.time()
        response = requests.post(
            endpoint["url"],
            headers=headers,
            json=current_payload,
            timeout=endpoint["timeout"]
        )
        execution_time = time.time() - start_time
        
        print(f"Response status code: {response.status_code}")
        print(f"Execution time: {round(execution_time, 2)} seconds")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Response structure: {list(result.keys())}")
            
            # Process based on endpoint type
            if endpoint["name"] == "extract":
                if result.get("status") == "processing":
                    print(f"Extract job is still processing with ID: {result.get('id')}")
                    print(f"Expires at: {result.get('expiresAt')}")
                elif result.get("success") and "data" in result:
                    print("Data successfully extracted:")
                    print(json.dumps(result["data"], indent=2)[:1000])
            else:  # scrape
                if "data" in result and "json" in result["data"]:
                    print("JSON data extracted:")
                    print(json.dumps(result["data"]["json"], indent=2)[:1000])
        else:
            print(f"Error response: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error details: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Raw error response: {response.text[:1000]}")
    
    except Exception as e:
        print(f"Exception occurred: {str(e)}")

# Now create a test client for the FirecrawlExtract endpoint
print("\n=== Testing FirecrawlExtract endpoint in the connector ===")

# Local connector URL
base_url = "http://localhost:2003"
connector_url = f"{base_url}/FirecrawlExtract/v1/execute"

# Test data using the @URL syntax
test_data = {
    "data": {
        "extract_prompt": f"@{test_url} {test_prompt}",
        "enable_agent": True
    }
}

print(f"Testing connector URL: {connector_url}")
print(f"Payload: {json.dumps(test_data, indent=2)}")

try:
    start_time = time.time()
    response = requests.post(
        connector_url,
        json=test_data,
        timeout=60
    )
    execution_time = time.time() - start_time
    
    print(f"Response status code: {response.status_code}")
    print(f"Execution time: {round(execution_time, 2)} seconds")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Response structure: {list(result.keys())}")
        
        if "extracted_elements" in result:
            elements = result["extracted_elements"]
            print(f"Extracted elements: {json.dumps(elements, indent=2)[:1000]}")
    else:
        print(f"Error response: {response.status_code}")
        try:
            error_data = response.json()
            print(f"Error details: {json.dumps(error_data, indent=2)}")
        except:
            print(f"Raw error response: {response.text[:1000]}")

except Exception as e:
    print(f"Exception occurred: {str(e)}") 