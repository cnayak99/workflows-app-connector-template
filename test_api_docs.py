import requests
import json

# Firecrawl API constants
FIRECRAWL_API_KEY = "fc-1956059de87d45ceba43c29343869685"
FIRECRAWL_BASE_URL = "https://api.firecrawl.dev/v1"

# Set up headers
headers = {
    "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
    "Content-Type": "application/json"
}

# Try to fetch API documentation
print("=== Attempting to fetch Firecrawl API documentation ===")

# Try different documentation endpoints
endpoints = [
    f"{FIRECRAWL_BASE_URL}/",
    f"{FIRECRAWL_BASE_URL}/docs",
    f"{FIRECRAWL_BASE_URL}/schema",
    f"{FIRECRAWL_BASE_URL}/openapi.json"
]

for endpoint in endpoints:
    try:
        print(f"\nFetching documentation from: {endpoint}")
        response = requests.get(endpoint, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"Documentation found at {endpoint}")
                # Check if there's information about the scrape endpoint
                if "paths" in data and "/scrape" in str(data["paths"]):
                    print("Found scrape endpoint documentation!")
                    # Try to find parameter details
                    scrape_info = data["paths"].get("/scrape", {})
                    if scrape_info:
                        print("Parameters for /scrape:")
                        for method, details in scrape_info.items():
                            if "parameters" in details:
                                for param in details["parameters"]:
                                    print(f"- {param.get('name')}: {param.get('description')}")
                            if "requestBody" in details:
                                print("Request body schema:")
                                schema = details["requestBody"].get("content", {}).get("application/json", {}).get("schema", {})
                                if "properties" in schema:
                                    for prop_name, prop_details in schema["properties"].items():
                                        print(f"- {prop_name}: {prop_details.get('description', 'No description')}")
            except:
                print(f"Could not parse JSON response: {response.text[:500]}")
        else:
            print(f"Failed to get documentation: {response.text[:500]}")
    except Exception as e:
        print(f"Error fetching {endpoint}: {str(e)}")

# Let's try a minimal request and print ALL the response data to see what we get
minimal_payload = {
    "url": "https://www.ycombinator.com/about",
    "formats": ["markdown"]
}

print("\n=== Making a minimal request to analyze response metadata ===")
print(f"Payload: {json.dumps(minimal_payload, indent=2)}")

response = requests.post(f"{FIRECRAWL_BASE_URL}/scrape", headers=headers, json=minimal_payload)
print(f"Status: {response.status_code}")

if response.status_code == 200:
    result = response.json()
    print("Response keys:", list(result.keys()))
    
    # Check for metadata which might contain info on available parameters
    if "data" in result:
        print("Data keys:", list(result["data"].keys()))
        if "metadata" in result["data"]:
            print("\nMetadata from response:")
            print(json.dumps(result["data"]["metadata"], indent=2))
    
    # Check for any markdown content
    if "data" in result and "markdown" in result["data"]:
        md_content = result["data"]["markdown"]
        print(f"\nMarkdown preview (first 100 chars): {md_content[:100]}...")
else:
    try:
        print(f"Error: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Error: {response.text[:500]}") 