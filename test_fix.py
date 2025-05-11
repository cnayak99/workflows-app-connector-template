import requests
import json
import time

# Create a minimal test to verify Firecrawl API and our connector

base_url = "http://localhost:2003"

# First, test the connector's direct Firecrawl endpoint
url1 = "https://www.ycombinator.com/companies/industry/consumer"
url2 = "https://www.ycombinator.com/library"

print("\n===== TEST 1: YC Consumer URL directly with Firecrawl API =====")

# Build Firecrawl API payload
FIRECRAWL_API_KEY = "fc-1956059de87d45ceba43c29343869685"
payload1 = {
    "url": url1,
    "formats": ["json", "markdown"],
    "jsonOptions": {
        "prompt": "Get me the W24 companies that are on the consumer space",
        "mode": "llm"
    }
}

# Call Firecrawl API directly
print(f"Calling Firecrawl API directly with URL: {url1}")
response = requests.post(
    "https://api.firecrawl.dev/v1/scrape",
    headers={
        "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
        "Content-Type": "application/json"
    },
    json=payload1,
    timeout=30
)

print(f"Status code: {response.status_code}")
if response.status_code == 200:
    try:
        result = response.json()
        if "data" in result and "json" in result["data"]:
            json_data = result["data"]["json"]
            if isinstance(json_data, list) and len(json_data) > 0:
                print(f"Found {len(json_data)} companies. First few:")
                for i, company in enumerate(json_data[:5]):
                    if isinstance(company, dict):
                        name = company.get("name", "Unknown")
                        batch = company.get("batch", "Unknown")
                        print(f"  {i+1}. {name} ({batch})")
    except Exception as e:
        print(f"Error parsing response: {e}")
else:
    print(f"Error response: {response.text[:500]}")

print("\n===== TEST 2: Library URL with the mapping endpoint =====")
print(f"Calling /FirecrawlMapping/v1/execute with URL: {url2}")

# Test the mapping endpoint
try:
    response = requests.post(
        f"{base_url}/FirecrawlMapping/v1/execute",
        json={"data": {"url": url2}},
        timeout=60
    )
    
    print(f"Status code: {response.status_code}")
    try:
        result = response.json()
        print(f"Response keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
        
        if isinstance(result, dict) and "map_results" in result:
            map_results = result["map_results"]
            if "links" in map_results:
                links = map_results["links"]
                print(f"Found {len(links)} links.")
                for i, link in enumerate(links[:5]):
                    print(f"  {i+1}. {link}")
        elif isinstance(result, dict) and "error" in result:
            print(f"Error: {result.get('error')}")
            print(f"Details: {json.dumps(result, indent=2)}")
    except Exception as e:
        print(f"Error parsing response: {e}")
        print(f"Raw response: {response.text[:500]}")
except Exception as e:
    print(f"Request failed: {e}")

print("\n===== TEST 3: Directly call the Firecrawl API's /map endpoint =====")
print(f"Calling Firecrawl API directly with URL: {url2}")

# Call map API directly
payload3 = {"url": url2}
response = requests.post(
    "https://api.firecrawl.dev/v1/map",
    headers={
        "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
        "Content-Type": "application/json"
    },
    json=payload3,
    timeout=30
)

print(f"Status code: {response.status_code}")
if response.status_code == 200:
    try:
        result = response.json()
        links = result.get("links", [])
        print(f"Found {len(links)} links. First few:")
        for i, link in enumerate(links[:5]):
            print(f"  {i+1}. {link}")
    except Exception as e:
        print(f"Error parsing response: {e}")
else:
    print(f"Error response: {response.text[:500]}") 