import requests
import json

# Test the fixed connector with the original request that was failing
print("=== Testing the fixed Firecrawl connector with exclude_tags parameter ===")

# The original request that was failing
test_payload = {
    "url": "https://www.ycombinator.com/about",
    "exclude_tags": "#introduction",
    "extract_main_content": True
}

print(f"Sending request with payload: {json.dumps(test_payload, indent=2)}")

# Send to the connector
connector_url = "http://localhost:2003/Firecrawl/v1/execute"
response = requests.post(connector_url, json=test_payload)

print(f"Response status code: {response.status_code}")

if response.status_code == 200:
    result = response.json()
    print("SUCCESS! Request processed correctly")
    
    # Print the structure of the response
    print("\nResponse structure:")
    if "result" in result:
        print(f"Keys in result: {list(result['result'].keys())}")
        if "data" in result["result"]:
            print(f"Data keys: {list(result['result']['data'].keys())}")
    
    # Display the extracted content (should NOT have the INTRODUCTION section)
    if "result" in result and "data" in result["result"] and "markdown" in result["result"]["data"]:
        extracted_content = result["result"]["data"]["markdown"]
        print("\nExtracted content (first 300 chars):")
        print(extracted_content[:300])
        
        # Print the json content for comparison
        if "json" in result["result"]["data"]:
            json_content = result["result"]["data"]["json"]
            print("\nJSON content for comparison:")
            if isinstance(json_content, dict):
                print(json.dumps(json_content, indent=2)[:500])
            else:
                print(json_content[:500])
        
        # Verify introduction is excluded
        if "INTRODUCTION" not in extracted_content and "Introduction" not in extracted_content:
            print("\n✅ SUCCESS: The introduction section has been properly excluded!")
        else:
            print("\n❌ FAILURE: The introduction section is still present in the extracted content")
    else:
        print("\n❌ FAILURE: Could not find expected content in the response")
else:
    print("\n❌ FAILURE: Request failed")
    try:
        error_data = response.json()
        print(f"Error details: {json.dumps(error_data, indent=2)}")
    except:
        print(f"Error response: {response.text[:500]}")

print("\nNOTE: For this test to work, make sure the Firecrawl connector is running (python main.py)") 