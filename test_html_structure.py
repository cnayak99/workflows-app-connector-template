import requests
import json
import re

# Firecrawl API constants
FIRECRAWL_API_KEY = "fc-1956059de87d45ceba43c29343869685"
FIRECRAWL_BASE_URL = "https://api.firecrawl.dev/v1"

# Set up headers
headers = {
    "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
    "Content-Type": "application/json"
}

# Let's try a request that includes HTML to analyze the page structure
html_payload = {
    "url": "https://www.ycombinator.com/about",
    "formats": ["markdown", "html"]  # Request both markdown and HTML
}

print("=== Fetching page with HTML format to analyze structure ===")
response = requests.post(f"{FIRECRAWL_BASE_URL}/scrape", headers=headers, json=html_payload)
print(f"Status: {response.status_code}")

if response.status_code == 200:
    result = response.json()
    
    # Check if we have HTML data
    if "data" in result and "html" in result["data"]:
        html_content = result["data"]["html"]
        
        # Save the HTML to a file for inspection
        with open("ycombinator_about.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("Saved HTML content to ycombinator_about.html")
        
        # Look for div with id="introduction" or similar
        intro_match = re.search(r'<(div|section|header)([^>]*id\s*=\s*["\']introduction["\']|[^>]*class\s*=\s*["\'][^"\']*introduction[^"\']*["\'])[^>]*>', html_content, re.IGNORECASE)
        if intro_match:
            print(f"Found introduction element: {intro_match.group(0)}")
        else:
            print("No element with id or class 'introduction' found")
            
        # Look for header with "INTRODUCTION" text
        intro_header = re.search(r'<h[1-6][^>]*>.*?INTRODUCTION.*?</h[1-6]>', html_content, re.IGNORECASE)
        if intro_header:
            print(f"Found introduction header: {intro_header.group(0)}")
        else:
            print("No header with 'INTRODUCTION' text found")
            
        # Look for any section that might be the introduction
        sections = re.findall(r'<(div|section|article)([^>]*)>.*?</\1>', html_content, re.DOTALL)
        print(f"Found {len(sections)} major sections in the HTML")
        
    # Check the markdown content
    if "data" in result and "markdown" in result["data"]:
        md_content = result["data"]["markdown"]
        
        # Save the markdown to a file for inspection
        with open("ycombinator_about.md", "w", encoding="utf-8") as f:
            f.write(md_content)
        print("Saved markdown content to ycombinator_about.md")
        
        # Look for INTRODUCTION in the markdown
        intro_section = re.search(r'#{1,6}\s*\*?\*?INTRODUCTION\*?\*?', md_content, re.IGNORECASE)
        if intro_section:
            print(f"Found introduction in markdown: {intro_section.group(0)}")
            
            # Try to identify where the introduction section ends
            lines = md_content.split('\n')
            for i, line in enumerate(lines):
                if intro_section.group(0) in line:
                    print(f"Introduction starts at line {i+1}")
                    # Try to find the next header which would indicate the end of intro
                    for j in range(i+1, len(lines)):
                        if re.match(r'^#{1,6}\s', lines[j]):
                            print(f"Next section starts at line {j+1}: {lines[j]}")
                            
                            # Extract content without introduction
                            content_without_intro = '\n'.join(lines[:i] + lines[j:])
                            print("\nContent without introduction would look like:")
                            print(content_without_intro[:300] + "...")
                            break
                    break
else:
    try:
        print(f"Error: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Error: {response.text[:500]}")

# Now let's try using the "actions" parameter to modify the page before extraction
actions_payload = {
    "url": "https://www.ycombinator.com/about",
    "formats": ["markdown"],
    "actions": [
        {
            "type": "remove",
            "selector": "h3:contains('INTRODUCTION'), h3:contains('Introduction')"
        }
    ]
}

print("\n=== Trying actions parameter to remove introduction ===")
response = requests.post(f"{FIRECRAWL_BASE_URL}/scrape", headers=headers, json=actions_payload)
print(f"Status: {response.status_code}")

if response.status_code == 200:
    result = response.json()
    if "data" in result and "markdown" in result["data"]:
        md_content = result["data"]["markdown"]
        print(f"Content with actions: {md_content[:200]}...")
else:
    try:
        print(f"Error: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Error: {response.text[:500]}")

# Let's try using the extract endpoint directly
extract_payload = {
    "url": "https://www.ycombinator.com/about",
    "formats": ["json"],
    "jsonOptions": {
        "prompt": "Extract the content of the YC About page, excluding the Introduction section. Format as markdown.",
        "mode": "llm"
    }
}

print("\n=== Trying extraction with LLM to exclude introduction ===")
response = requests.post(f"{FIRECRAWL_BASE_URL}/scrape", headers=headers, json=extract_payload)
print(f"Status: {response.status_code}")

if response.status_code == 200:
    result = response.json()
    if "data" in result and "json" in result["data"]:
        json_content = result["data"]["json"]
        print(f"Extracted content: {json.dumps(json_content, indent=2)[:500]}...")
else:
    try:
        print(f"Error: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Error: {response.text[:500]}") 