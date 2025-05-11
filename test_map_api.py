import requests
import json
import sys

# Firecrawl API constants
FIRECRAWL_API_KEY = "fc-1956059de87d45ceba43c29343869685"
FIRECRAWL_BASE_URL = "https://api.firecrawl.dev/v1"

def test_map_api():
    """Test the Firecrawl map API with the specific payload from the user."""
    
    # Set up headers
    headers = {
        "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Build payload with camelCase parameters as required by API
    payload = {
        "url": "https://www.ycombinator.com/library",
        "includeSubdomains": True,
        "ignoreSitemap": False
    }
    
    print(f"Testing map API with payload: {json.dumps(payload, indent=2)}")
    
    # Call Firecrawl API map endpoint
    firecrawl_url = f"{FIRECRAWL_BASE_URL}/map"
    response = requests.post(firecrawl_url, headers=headers, json=payload)
    
    print(f"Response status code: {response.status_code}")
    
    try:
        response_json = response.json()
        if response.status_code != 200:
            print(f"Error response: {json.dumps(response_json, indent=2)}")
        else:
            # Success
            print(f"Success! Found {len(response_json.get('links', []))} links")
            print(f"First 5 links: {json.dumps(response_json.get('links', [])[:5], indent=2)}")
    except:
        print(f"Response content: {response.text[:500]}")

def test_connector():
    """Test the connector API directly."""
    
    # Build payload with the same parameters
    payload = {
        "url": "https://www.ycombinator.com/library",
        "include_subdomains": True,
        "ignore_sitemap": False
    }
    
    print(f"Testing connector API with payload: {json.dumps(payload, indent=2)}")
    
    # Call connector API
    connector_url = "http://localhost:2003/FirecrawlMapping/v1/execute"
    response = requests.post(connector_url, json=payload)
    
    print(f"Response status code: {response.status_code}")
    
    try:
        response_json = response.json()
        print(f"Response: {json.dumps(response_json, indent=2)[:500]}")
    except:
        print(f"Response content: {response.text[:500]}")

if __name__ == "__main__":
    # Get command line argument to determine which test to run
    if len(sys.argv) > 1 and sys.argv[1] == "connector":
        test_connector()
    else:
        test_map_api() 