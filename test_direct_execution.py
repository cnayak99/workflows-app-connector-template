import requests
import json

# Test the connector directly with the parameters from the user
print("=== Testing Firecrawl Connector with Updated Prompt ===")

# The input payload
payload = {
    "url": "https://www.ycombinator.com/about",
    "exclude_tags": "#introduction",
    "extract_main_content": True
}

print(f"Sending request with: {json.dumps(payload, indent=2)}")

# Make the request to the connector
connector_url = "http://localhost:2003/Firecrawl/v1/execute"
response = requests.post(connector_url, json=payload)

print(f"Response status: {response.status_code}")

if response.status_code == 200:
    # Parse the response
    result = response.json()
    
    # Extract the content
    if "result" in result and "data" in result["result"] and "markdown" in result["result"]["data"]:
        content = result["result"]["data"]["markdown"]
        
        # Print the content
        print("\nExtracted content (first 300 chars):")
        print(content[:300])
        
        # Check if title is present
        has_title = "# What Happens at YC" in content
        has_intro = "INTRODUCTION" in content
        
        if has_title and not has_intro:
            print("\n✅ SUCCESS: Title is preserved and introduction is excluded!")
        elif has_title:
            print("\n❌ Title is preserved but introduction is still present")
        elif not has_intro:
            print("\n❌ Introduction is excluded but title is missing")
        else:
            print("\n❌ Both title and introduction checks failed")
            
        # Compare with expected result
        expected_output = "# What Happens at YC\n\nPeople often ask us what happens at Y Combinator. Here is an overview of what happens during the YC program and the benefits you get as a YC founder."
        
        # Check if the expected output is in the content
        lines = content.split('\n')
        first_paragraph = '\n'.join(lines[:3])
        if expected_output in first_paragraph:
            print("\n✅ SUCCESS: The output matches the expected format!")
        else:
            print("\n❌ Output doesn't match expected format")
            print("Expected:\n" + expected_output)
            print("Actual:\n" + first_paragraph)
    else:
        print("\n❌ Failed to find markdown content in the response")
else:
    print("\n❌ Request failed")
    try:
        error = response.json()
        print(json.dumps(error, indent=2))
    except:
        print(response.text[:500]) 