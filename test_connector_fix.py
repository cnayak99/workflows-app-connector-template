import requests
import json

# Test the original request that was failing
print("=== Testing the fix for Firecrawl connector ===")

# Original payload with the problematic parameters
original_payload = {
    "url": "https://www.ycombinator.com/about",
    "exclude_tags": "#introduction",
    "extract_main_content": True
    # Missing "formats" parameter
}

print("Sending request with original problematic payload:")
print(json.dumps(original_payload, indent=2))

# Send to the connector (which should now handle this correctly)
connector_url = "http://localhost:2003/Firecrawl/v1/execute"
response = requests.post(connector_url, json=original_payload)

print(f"Response status code: {response.status_code}")

try:
    result = response.json()
    print("Response:")
    print(json.dumps(result, indent=2)[:1000])
    
    if response.status_code == 200:
        print("\nSUCCESS: The connector fix is working! It's handling the request correctly.")
        
        # Verify that the result contains the expected data
        if "result" in result and "data" in result["result"] and "markdown" in result["result"]["data"]:
            print("Content was successfully extracted.")
            # Print a snippet of the content
            print("\nContent snippet:")
            print(result["result"]["data"]["markdown"][:200] + "...")
        else:
            print("Warning: Response format is not as expected.")
    else:
        print("\nFAILURE: The connector is still returning an error.")
        print("Check if the connector is running and the fix has been applied.")
except Exception as e:
    print(f"Error parsing response: {str(e)}")
    print(f"Raw response: {response.text[:1000]}") 