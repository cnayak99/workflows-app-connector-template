import requests
import json
import sys
import time

# Firecrawl API constants
FIRECRAWL_API_KEY = "fc-1956059de87d45ceba43c29343869685"
FIRECRAWL_BASE_URL = "https://api.firecrawl.dev/v1"
CONNECTOR_BASE_URL = "http://localhost:2003"

def test_extract_api():
    """Test the Firecrawl scrape API with element extraction"""
    
    # Set up headers
    headers = {
        "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Build payload to extract pricing elements from Firecrawl website
    # We'll use the scrape endpoint with actions to achieve similar functionality
    payload = {
        "url": "https://www.firecrawl.dev/pricing",
        "formats": ["json"],
        "jsonOptions": {
            "prompt": "Extract all pricing tiers with names, prices, and features",
            "mode": "llm"
        }
    }
    
    print(f"Testing extract API with payload: {json.dumps(payload, indent=2)}")
    
    # Call Firecrawl API scrape endpoint with extraction
    firecrawl_url = f"{FIRECRAWL_BASE_URL}/scrape"
    response = requests.post(firecrawl_url, headers=headers, json=payload)
    
    print(f"Response status code: {response.status_code}")
    
    # Check if the request was successful
    if response.status_code == 200:
        results = response.json()
        print(f"Success! Extracted data using LLM extraction")
        
        # Print the extraction results
        if "data" in results and "json" in results["data"]:
            extracted_data = results["data"]["json"]
            print(f"\nExtracted data:")
            print(json.dumps(extracted_data, indent=2))
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

def test_connector_api():
    """Test the connector's FirecrawlExtract API implementation."""
    
    # Build payload for connector
    payload = {
        "url": "https://www.firecrawl.dev/pricing",
        "extract_prompt": "Extract all pricing tiers with names, prices, and features",
        "extract_text": True,
        "extract_html": False
    }
    
    print(f"Testing connector API with payload: {json.dumps(payload, indent=2)}")
    
    # Call connector's FirecrawlExtract execute endpoint
    connector_url = f"{CONNECTOR_BASE_URL}/FirecrawlExtract/v1/execute"
    response = requests.post(connector_url, json=payload)
    
    print(f"Response status code: {response.status_code}")
    
    # Check if the request was successful
    if response.status_code == 200:
        results = response.json()
        print(f"Success! Extracted data via connector")
        
        # Print the extraction results
        if "extracted_elements" in results:
            elements = results["extracted_elements"]
            print(f"\nExtracted elements:")
            print(json.dumps(elements, indent=2)[:1000])  # Show first 1000 chars
    else:
        print(f"Error: {response.status_code}")
        try:
            error_data = response.json()
            print(json.dumps(error_data, indent=2))
        except:
            print(response.text)

def test_simple_endpoint():
    """Test the simple test-extract endpoint."""
    
    # Build query params
    url = "https://www.firecrawl.dev/pricing"
    endpoint = f"{CONNECTOR_BASE_URL}/test-extract?url={url}&extract_prompt=Extract all pricing tiers with names, prices, and features"
    
    print(f"Testing simple endpoint: {endpoint}")
    
    # Call simple test endpoint 
    response = requests.get(endpoint)
    
    print(f"Response status code: {response.status_code}")
    
    # Check if the request was successful
    if response.status_code == 200:
        results = response.json()
        print(f"Success! Extracted data via simple endpoint")
        
        # Print extraction results
        print(f"\nExtracted data:")
        print(json.dumps(results, indent=2)[:1000])  # Show first 1000 chars
    else:
        print(f"Error: {response.status_code}")
        try:
            error_data = response.json()
            print(json.dumps(error_data, indent=2))
        except:
            print(response.text)

def test_wildcard_url_direct():
    """Test the Firecrawl scrape API directly with wildcard URLs."""
    
    print("\n===== Testing Firecrawl scrape API with wildcard URL (direct) =====")
    
    # Set up headers
    headers = {
        "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # YC URL with wildcard (this should be handled properly in our modified code)
    url = "https://ycombinator.com/companies/*"
    extract_prompt = "Get me the W24 companies that are on the consumer space"
    
    # Clean URL for the direct API call (removing wildcard)
    clean_url = "https://www.ycombinator.com/companies"
    
    # Build payload
    payload = {
        "url": clean_url,
        "formats": ["json"],
        "jsonOptions": {
            "prompt": extract_prompt,
            "mode": "llm"
        },
        "agent": {
            "model": "FIRE-1",
            "prompt": extract_prompt
        }
    }
    
    print(f"Testing Firecrawl scrape API with payload: {json.dumps(payload, indent=2)}")
    
    start_time = time.time()
    
    # Call Firecrawl API directly
    firecrawl_url = f"{FIRECRAWL_BASE_URL}/scrape"
    response = requests.post(firecrawl_url, headers=headers, json=payload)
    
    execution_time = time.time() - start_time
    print(f"Response status code: {response.status_code}")
    print(f"Execution time: {round(execution_time, 2)} seconds")
    
    # Check if the request was successful
    if response.status_code == 200:
        output = response.json()
        print(f"Success! Response received")
        
        # Extract data
        extracted_data = {}
        if "data" in output and "json" in output["data"]:
            extracted_data = output["data"]["json"]
            
        print("\nExtracted data:")
        print(json.dumps(extracted_data, indent=2)[:1000] + "..." if len(json.dumps(extracted_data)) > 1000 else json.dumps(extracted_data, indent=2))
    else:
        print(f"Error: {response.status_code}")
        try:
            error_data = response.json()
            print(f"Error details: {json.dumps(error_data, indent=2)}")
        except:
            print(response.text[:1000])

def test_connector_extract():
    """Test the connector's extract endpoint with the wildcard URL."""
    
    print("\n===== Testing connector extract endpoint with wildcard URL =====")
    
    # Data to send to connector
    data = {
        "url": "https://ycombinator.com/companies/*",
        "extract_prompt": "Get me the W24 companies that are on the consumer space",
        "enable_agent": True,
        "enable_web_search": False
    }
    
    print(f"Sending data to connector: {json.dumps(data, indent=2)}")
    
    start_time = time.time()
    
    # Call connector endpoint
    connector_url = f"{CONNECTOR_BASE_URL}/FirecrawlExtract/v1/execute"
    response = requests.post(connector_url, json=data)
    
    execution_time = time.time() - start_time
    print(f"Response status code: {response.status_code}")
    print(f"Execution time: {round(execution_time, 2)} seconds")
    
    # Check if the request was successful
    if response.status_code == 200:
        output = response.json()
        print(f"Success! Response received")
        
        print("\nResponse data:")
        print(json.dumps(output, indent=2)[:1000] + "..." if len(json.dumps(output)) > 1000 else json.dumps(output, indent=2))
    else:
        print(f"Error: {response.status_code}")
        try:
            error_data = response.json()
            print(f"Error details: {json.dumps(error_data, indent=2)}")
        except:
            print(response.text[:1000])

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "connector":
        test_connector_api()
    elif len(sys.argv) > 1 and sys.argv[1] == "simple":
        test_simple_endpoint()
    else:
        print("=== Firecrawl Extract API Testing ===")
        
        # Test the direct Firecrawl API
        test_wildcard_url_direct()
        
        # Test the connector endpoint (only if the server is running)
        try:
            test_connector_extract()
        except requests.exceptions.ConnectionError:
            print("\nCould not connect to connector server. Make sure it's running at", CONNECTOR_BASE_URL)
            print("You can start it with: python main.py") 