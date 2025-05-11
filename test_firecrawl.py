import requests
import json
import time

# Firecrawl API constants
FIRECRAWL_API_KEY = "fc-1956059de87d45ceba43c29343869685"
FIRECRAWL_BASE_URL = "https://api.firecrawl.dev/v1"
CONNECTOR_BASE_URL = "http://localhost:2003"

def test_direct_api():
    """Test calling the Firecrawl API directly"""
    
    # Set up headers
    headers = {
        "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Build a simple payload - ensure "formats" is included and valid
    payload = {
        "url": "https://www.ycombinator.com/about",
        "formats": ["markdown"]  # Valid format values: markdown, html, rawHtml, links, screenshot, etc.
    }
    
    print(f"Testing Firecrawl API directly with payload: {json.dumps(payload, indent=2)}")
    
    # Call Firecrawl API directly
    firecrawl_url = f"{FIRECRAWL_BASE_URL}/scrape"
    response = requests.post(firecrawl_url, headers=headers, json=payload)
    
    print(f"Response status code: {response.status_code}")
    
    # Check if the request was successful
    if response.status_code == 200:
        print(f"Success! Response received")
        result = response.json()
        
        # Print the response keys to understand structure
        print(f"Response keys: {result.keys()}")
        if "data" in result:
            print(f"Data keys: {result['data'].keys()}")
    else:
        print(f"Error: {response.status_code}")
        try:
            error_data = response.json()
            print(f"Error details: {json.dumps(error_data, indent=2)}")
        except:
            print(f"Raw error: {response.text[:1000]}")

def test_connector_api():
    """Test the connector's Firecrawl endpoint"""
    
    # Build payload for connector
    payload = {
        "url": "https://www.ycombinator.com/about",
        "extract_main_content": True
    }
    
    print(f"Testing connector API with payload: {json.dumps(payload, indent=2)}")
    
    # Call connector endpoint
    connector_url = f"{CONNECTOR_BASE_URL}/Firecrawl/v1/execute"
    response = requests.post(connector_url, json=payload)
    
    print(f"Response status code: {response.status_code}")
    
    # Check if the request was successful
    if response.status_code == 200:
        print(f"Success! Response received from connector")
        result = response.json()
        
        # Print the response keys to understand structure
        if "result" in result:
            print(f"Connector result keys: {result['result'].keys()}")
            if "data" in result["result"]:
                print(f"Data keys: {result['result']['data'].keys()}")
    else:
        print(f"Error: {response.status_code}")
        try:
            error_data = response.json()
            print(f"Error details: {json.dumps(error_data, indent=2)}")
        except:
            print(f"Raw error: {response.text[:1000]}")

def test_json_extraction():
    """Test extracting structured data using jsonOptions"""
    
    # Set up headers
    headers = {
        "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Build payload with JSON extraction
    payload = {
        "url": "https://www.ycombinator.com/companies/industry/consumer",
        "formats": ["json"],
        "jsonOptions": {
            "prompt": "Extract the names of YC consumer companies as a list",
            "mode": "llm"
        }
    }
    
    print(f"Testing JSON extraction with payload: {json.dumps(payload, indent=2)}")
    
    # Call Firecrawl API directly
    firecrawl_url = f"{FIRECRAWL_BASE_URL}/scrape"
    response = requests.post(firecrawl_url, headers=headers, json=payload)
    
    print(f"Response status code: {response.status_code}")
    
    # Check if the request was successful
    if response.status_code == 200:
        print(f"Success! Response received")
        result = response.json()
        
        # Print the JSON extraction results
        if "data" in result and "json" in result["data"]:
            extracted_json = result["data"]["json"]
            print(f"Extracted JSON data: {json.dumps(extracted_json, indent=2)}")
    else:
        print(f"Error: {response.status_code}")
        try:
            error_data = response.json()
            print(f"Error details: {json.dumps(error_data, indent=2)}")
        except:
            print(f"Raw error: {response.text[:1000]}")

def test_connector_json_extraction():
    """Test the connector's Firecrawl endpoint with JSON extraction"""
    
    # Build payload for connector
    payload = {
        "url": "https://www.ycombinator.com/companies/industry/consumer",
        "extract_prompt": "Extract the names of YC consumer companies as a list"
    }
    
    print(f"Testing connector API with JSON extraction payload: {json.dumps(payload, indent=2)}")
    
    # Call connector endpoint
    connector_url = f"{CONNECTOR_BASE_URL}/Firecrawl/v1/execute"
    response = requests.post(connector_url, json=payload)
    
    print(f"Response status code: {response.status_code}")
    
    # Check if the request was successful
    if response.status_code == 200:
        print(f"Success! Response received from connector")
        result = response.json()
        
        # Print the extracted JSON if available
        if "result" in result and "data" in result["result"] and "json" in result["result"]["data"]:
            extracted_json = result["result"]["data"]["json"]
            print(f"Extracted JSON data: {json.dumps(extracted_json, indent=2)}")
    else:
        print(f"Error: {response.status_code}")
        try:
            error_data = response.json()
            print(f"Error details: {json.dumps(error_data, indent=2)}")
        except:
            print(f"Raw error: {response.text[:1000]}")

if __name__ == "__main__":
    print("\n=== Testing Firecrawl API Integration ===")
    
    # Test the direct API call first to verify API is working
    print("\n=== Test 1: Direct API Call ===")
    test_direct_api()
    
    # Test the connector endpoint to verify our implementation
    print("\n=== Test 2: Connector API Call ===")
    try:
        test_connector_api()
    except requests.exceptions.ConnectionError:
        print("\nCould not connect to connector server. Make sure it's running at", CONNECTOR_BASE_URL)
        print("You can start it with: python main.py")
    
    # Test JSON extraction directly
    print("\n=== Test 3: Direct JSON Extraction ===")
    test_json_extraction()
    
    # Test JSON extraction via connector
    print("\n=== Test 4: Connector JSON Extraction ===")
    try:
        test_connector_json_extraction()
    except requests.exceptions.ConnectionError:
        print("\nCould not connect to connector server. Make sure it's running at", CONNECTOR_BASE_URL)
        print("You can start it with: python main.py") 