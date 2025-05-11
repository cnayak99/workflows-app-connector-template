import requests
import json

def test_direct_connection():
    """Test direct connection to the Firecrawl API with the specific payload from the user."""
    
    # Firecrawl API constants
    FIRECRAWL_API_KEY = "fc-1956059de87d45ceba43c29343869685"
    FIRECRAWL_BASE_URL = "https://api.firecrawl.dev/v1"
    
    # Set up authentication headers
    headers = {
        "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Original payload with the issues
    original_payload = {
        "url": "https://www.ycombinator.com/about",
        "exclude_tags": "#introduction",
        "extract_main_content": True
    }
    
    # Fixed payload with correct structure for the API
    fixed_payload = {
        "url": "https://www.ycombinator.com/about",
        "formats": ["markdown"]  # This is the required parameter!
    }
    
    print("=== Testing Direct Connection to Firecrawl API ===")
    print(f"Calling API with fixed payload: {json.dumps(fixed_payload, indent=2)}")
    
    # Make the API call
    response = requests.post(f"{FIRECRAWL_BASE_URL}/scrape", headers=headers, json=fixed_payload)
    
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 200:
        print("SUCCESS: API call worked with the fixed payload")
        data = response.json()
        
        # Print some information about the response
        print(f"Response keys: {list(data.keys())}")
        if "data" in data:
            print(f"Data keys: {list(data['data'].keys())}")
            
            # Print a small sample of the markdown content
            if "markdown" in data["data"]:
                print("\nSample of markdown content:")
                print(data["data"]["markdown"][:200] + "...")
    else:
        print("ERROR: API call failed")
        try:
            print(json.dumps(response.json(), indent=2))
        except:
            print(response.text[:500])

def test_connector_fix():
    """How the connector should be fixed to handle parameter translation."""
    
    # This shows how the connector should process the parameters
    print("\n=== Simulating the Connector Fix ===")
    
    # User's original request with deprecated parameters
    user_request = {
        "url": "https://www.ycombinator.com/about",
        "exclude_tags": "#introduction",
        "extract_main_content": True
    }
    
    # How the connector should transform this
    api_payload = {
        "url": user_request["url"],
        "formats": ["markdown"]  # Add the required formats parameter
    }
    
    # Note: The problematic parameters should be removed or mapped properly
    # Since our testing showed they aren't accepted by the API
    
    print("User request:")
    print(json.dumps(user_request, indent=2))
    
    print("\nProcessed payload for API:")
    print(json.dumps(api_payload, indent=2))
    
    print("\nSuggested fixes for the connector:")
    print("1. Always include 'formats' parameter, defaulting to ['markdown'] if not provided")
    print("2. Remove or properly map 'exclude_tags' and 'extract_main_content' parameters")
    print("3. Add better error handling to provide more detailed error messages")
    print("4. Consider updating parameter names in your connector's documentation")

if __name__ == "__main__":
    test_direct_connection()
    test_connector_fix() 