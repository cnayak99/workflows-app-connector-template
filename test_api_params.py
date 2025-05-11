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

# Test with different parameter approaches
print("=== Testing Firecrawl API with different parameter structures ===")

# Approach 1: Try excludeSelectors
payload1 = {
    "url": "https://www.ycombinator.com/about",
    "formats": ["markdown"],
    "excludeSelectors": ["#introduction"]
}

print("\nTesting with excludeSelectors:")
print(json.dumps(payload1, indent=2))
response = requests.post(f"{FIRECRAWL_BASE_URL}/scrape", headers=headers, json=payload1)
print(f"Response status: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    if "data" in result and "markdown" in result["data"]:
        md_content = result["data"]["markdown"]
        print(f"Content preview (excludeSelectors):\n{md_content[:200]}...")
else:
    try:
        print(f"Error: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Error: {response.text[:500]}")

# Approach 2: Try exclude_selectors (snake_case version)
payload2 = {
    "url": "https://www.ycombinator.com/about",
    "formats": ["markdown"],
    "exclude_selectors": ["#introduction"]
}

print("\nTesting with exclude_selectors:")
print(json.dumps(payload2, indent=2))
response = requests.post(f"{FIRECRAWL_BASE_URL}/scrape", headers=headers, json=payload2)
print(f"Response status: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    if "data" in result and "markdown" in result["data"]:
        md_content = result["data"]["markdown"]
        print(f"Content preview (exclude_selectors):\n{md_content[:200]}...")
else:
    try:
        print(f"Error: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Error: {response.text[:500]}")

# Approach 3: Try selector parameter
payload3 = {
    "url": "https://www.ycombinator.com/about",
    "formats": ["markdown"],
    "selector": "body > *:not(#introduction)"
}

print("\nTesting with selector:")
print(json.dumps(payload3, indent=2))
response = requests.post(f"{FIRECRAWL_BASE_URL}/scrape", headers=headers, json=payload3)
print(f"Response status: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    if "data" in result and "markdown" in result["data"]:
        md_content = result["data"]["markdown"]
        print(f"Content preview (selector):\n{md_content[:200]}...")
else:
    try:
        print(f"Error: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Error: {response.text[:500]}")

# Approach 4: Try removeSelectors
payload4 = {
    "url": "https://www.ycombinator.com/about",
    "formats": ["markdown"],
    "removeSelectors": ["#introduction"]
}

print("\nTesting with removeSelectors:")
print(json.dumps(payload4, indent=2))
response = requests.post(f"{FIRECRAWL_BASE_URL}/scrape", headers=headers, json=payload4)
print(f"Response status: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    if "data" in result and "markdown" in result["data"]:
        md_content = result["data"]["markdown"]
        print(f"Content preview (removeSelectors):\n{md_content[:200]}...")
else:
    try:
        print(f"Error: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Error: {response.text[:500]}")

# Approach 5: Try mainContentSelector with custom formatter
payload5 = {
    "url": "https://www.ycombinator.com/about",
    "formats": ["markdown"],
    "mainContentSelector": "body",
    "removeSelectors": ["#introduction"]
}

print("\nTesting with mainContentSelector + removeSelectors:")
print(json.dumps(payload5, indent=2))
response = requests.post(f"{FIRECRAWL_BASE_URL}/scrape", headers=headers, json=payload5)
print(f"Response status: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    if "data" in result and "markdown" in result["data"]:
        md_content = result["data"]["markdown"]
        print(f"Content preview (mainContentSelector + removeSelectors):\n{md_content[:200]}...")
else:
    try:
        print(f"Error: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Error: {response.text[:500]})") 