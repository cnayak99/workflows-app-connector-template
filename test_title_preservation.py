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

# Test different prompts to see which works best for title preservation
prompts = [
    "Extract the content of this page, including the main h1 title '# What Happens at YC', but exclude any content from sections matching #introduction. Format as clean markdown.",
    "Extract the content of this page starting with the title '# What Happens at YC' but exclude any section with the heading 'INTRODUCTION'. Format as clean markdown.",
    "Extract all content from this page, starting with the title '# What Happens at YC' but skipping the introduction section. Format as clean markdown.",
    "Extract the title '# What Happens at YC' and all content except the introduction section from this page. Format as clean markdown."
]

for i, prompt in enumerate(prompts):
    print(f"\n=== Testing prompt {i+1} ===")
    print(f"Prompt: {prompt}")
    
    # Create test payload
    payload = {
        "url": "https://www.ycombinator.com/about",
        "formats": ["json"],
        "jsonOptions": {
            "prompt": prompt,
            "mode": "llm"
        }
    }
    
    # Call Firecrawl API
    response = requests.post(f"{FIRECRAWL_BASE_URL}/scrape", headers=headers, json=payload)
    print(f"Response status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        
        if "data" in result and "json" in result["data"]:
            json_content = result["data"]["json"]
            
            # Extract the content
            content_text = ""
            if isinstance(json_content, str):
                content_text = json_content
            elif isinstance(json_content, dict):
                for key, value in json_content.items():
                    if isinstance(value, str) and len(value) > 50:
                        content_text = value
                        break
            
            # Check if title and intro are correctly handled
            if content_text:
                print(f"\nExtracted content (first 300 chars):")
                print(content_text[:300])
                
                # Check for title and intro
                has_title = "# What Happens at YC" in content_text
                has_intro = "INTRODUCTION" in content_text
                
                if has_title and not has_intro:
                    print(f"✅ SUCCESS: Title preserved and introduction excluded")
                elif has_title:
                    print(f"❌ Title preserved but introduction is still present")
                elif not has_intro:
                    print(f"❌ Introduction excluded but title is missing")
                else:
                    print(f"❌ Both title and introduction handling failed")
    else:
        print(f"❌ API call failed: {response.status_code}")
        try:
            print(response.json())
        except:
            print(response.text[:500])

# After finding the best prompt, update the connector with it and test 