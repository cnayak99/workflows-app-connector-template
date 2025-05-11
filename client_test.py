import requests
import json

# Simple client to test the FirecrawlExtract endpoint
base_url = "http://localhost:2003"
endpoint = f"{base_url}/FirecrawlExtract/v1/execute"

# Test data
test_data = {
    "data": {
        "url": "https://www.ycombinator.com/companies/industry/consumer",
        "extract_prompt": "Get me the W24 companies that are on the consumer space",
        "enable_agent": True
    }
}

print(f"Sending request to: {endpoint}")
print(f"Test data: {json.dumps(test_data, indent=2)}")

try:
    # Make request to the endpoint
    response = requests.post(endpoint, json=test_data)
    
    # Print response details
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("Success! Response structure:")
        print(f"Response keys: {list(result.keys())}")
        
        # Print extracted elements if available
        if "extracted_elements" in result:
            elements = result["extracted_elements"]
            print(f"Extracted elements type: {type(elements)}")
            print(f"Extracted elements: {json.dumps(elements, indent=2)[:1000]}")
    else:
        print("Error response:")
        try:
            error_data = response.json()
            print(json.dumps(error_data, indent=2))
        except:
            print(f"Raw response: {response.text[:1000]}")
except Exception as e:
    print(f"Request failed: {e}") 