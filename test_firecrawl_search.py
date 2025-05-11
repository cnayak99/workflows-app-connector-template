import requests
import json
import sys

# Firecrawl API constants
FIRECRAWL_API_KEY = "fc-1956059de87d45ceba43c29343869685"
FIRECRAWL_BASE_URL = "https://api.firecrawl.dev/v1"
CONNECTOR_BASE_URL = "http://localhost:2003"

def test_search_api():
    """Test the Firecrawl search API directly."""
    
    # Set up headers
    headers = {
        "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Build payload
    payload = {
        "query": "firecrawl web scraping",
        "limit": 3,
        "lang": "en",
        "country": "us",
        "scrapeOptions": {
            "formats": ["markdown", "links"]
        }
    }
    
    print(f"Testing search API with payload: {json.dumps(payload, indent=2)}")
    
    # Call Firecrawl API search endpoint
    firecrawl_url = f"{FIRECRAWL_BASE_URL}/search"
    response = requests.post(firecrawl_url, headers=headers, json=payload)
    
    print(f"Response status code: {response.status_code}")
    
    # Check if the request was successful
    if response.status_code == 200:
        results = response.json()
        print(f"Success! Found {len(results.get('data', []))} search results")
        
        # Print the first result title and URL
        if results.get('data') and len(results.get('data')) > 0:
            first_result = results['data'][0]
            print("\nFirst result:")
            print(f"Title: {first_result.get('title', 'No title')}")
            print(f"URL: {first_result.get('url', 'No URL')}")
            print(f"Description: {first_result.get('description', 'No description')[:100]}...")
            
            # Print a snippet of content
            if first_result.get('content') and first_result['content'].get('markdown'):
                content = first_result['content']['markdown']
                print(f"Markdown content: {content[:100]}...")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

def test_connector_api():
    """Test the connector's FirecrawlSearch API implementation."""
    
    # Build payload for connector
    payload = {
        "query": "firecrawl web scraping", 
        "lang": "en",
        "country": "us",
        "scrape_results": True
    }
    
    print(f"Testing connector API with payload: {json.dumps(payload, indent=2)}")
    
    # Call connector's FirecrawlSearch execute endpoint
    connector_url = f"{CONNECTOR_BASE_URL}/FirecrawlSearch/v1/execute"
    response = requests.post(connector_url, json=payload)
    
    print(f"Response status code: {response.status_code}")
    
    # Check if the request was successful
    if response.status_code == 200:
        results = response.json()
        result_count = len(results.get('search_results', []))
        print(f"Success! Found {result_count} search results")
        
        # Print the first result title and URL
        if results.get('search_results') and len(results.get('search_results')) > 0:
            first_result = results['search_results'][0]
            print("\nFirst result:")
            print(f"Title: {first_result.get('title', 'No title')}")
            print(f"URL: {first_result.get('url', 'No URL')}")
            print(f"Description: {first_result.get('description', 'No description')[:100]}...")
            
            # Print a snippet of content
            if first_result.get('content') and first_result['content'].get('markdown'):
                content = first_result['content']['markdown']
                print(f"Markdown content: {content[:100]}...")
    else:
        print(f"Error: {response.status_code}")
        try:
            error_data = response.json()
            print(json.dumps(error_data, indent=2))
        except:
            print(response.text)

def test_simple_endpoint():
    """Test the simple test-search endpoint."""
    
    # Build query params
    query = "firecrawl web scraping"
    endpoint = f"{CONNECTOR_BASE_URL}/test-search?q={query}&limit=3&lang=en&country=us"
    
    print(f"Testing simple endpoint: {endpoint}")
    
    # Call simple test endpoint 
    response = requests.get(endpoint)
    
    print(f"Response status code: {response.status_code}")
    
    # Check if the request was successful
    if response.status_code == 200:
        results = response.json()
        result_count = results.get('result_count', 0)
        print(f"Success! Found {result_count} search results")
        
        # Print the first result title and URL
        if results.get('results') and len(results.get('results')) > 0:
            first_result = results['results'][0]
            print("\nFirst result:")
            print(f"Title: {first_result.get('title', 'No title')}")
            print(f"URL: {first_result.get('url', 'No URL')}")
            print(f"Description: {first_result.get('description', 'No description')[:100]}...")
    else:
        print(f"Error: {response.status_code}")
        try:
            error_data = response.json()
            print(json.dumps(error_data, indent=2))
        except:
            print(response.text)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "connector":
        test_connector_api()
    elif len(sys.argv) > 1 and sys.argv[1] == "simple":
        test_simple_endpoint()
    else:
        test_search_api() 