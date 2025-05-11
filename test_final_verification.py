import requests
import json

def test_firecrawl_api_directly():
    """Test the Firecrawl API directly with the LLM extraction approach."""
    
    # Firecrawl API constants
    FIRECRAWL_API_KEY = "fc-1956059de87d45ceba43c29343869685"
    FIRECRAWL_BASE_URL = "https://api.firecrawl.dev/v1"
    
    # Set up headers
    headers = {
        "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Create the LLM extraction payload 
    llm_payload = {
        "url": "https://www.ycombinator.com/about",
        "formats": ["json"],
        "jsonOptions": {
            "prompt": "Extract the content of this page but exclude any content from sections matching: #introduction. Format the result as clean markdown.",
            "mode": "llm"
        }
    }
    
    print("=== Testing direct API call with LLM extraction ===")
    print(f"Sending payload to Firecrawl API: {json.dumps(llm_payload, indent=2)}")
    
    response = requests.post(f"{FIRECRAWL_BASE_URL}/scrape", headers=headers, json=llm_payload)
    print(f"Response status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("SUCCESS: API call worked")
        
        if "data" in result and "json" in result["data"]:
            json_content = result["data"]["json"]
            print("\nExtracted content from Firecrawl API:")
            if isinstance(json_content, dict):
                # Print pretty JSON
                print(json.dumps(json_content, indent=2)[:500] + "...")
                
                # Check if the content looks correct
                content_text = ""
                for key, value in json_content.items():
                    if isinstance(value, str) and len(value) > 50:
                        content_text = value
                        break
                
                if content_text:
                    print(f"\nContent (first 300 chars): {content_text[:300]}...")
                    
                    # Verify introduction is excluded
                    if "INTRODUCTION" not in content_text and "Introduction" not in content_text:
                        print("\n✅ SUCCESS: API directly returns content without introduction!")
                    else:
                        print("\n❌ FAILURE: API response still contains introduction")
    else:
        print("FAILURE: API call failed")
        try:
            error_data = response.json()
            print(f"Error details: {json.dumps(error_data, indent=2)}")
        except:
            print(f"Error: {response.text[:500]}")

def test_connector():
    """Test the connector with the original parameters that were failing."""
    
    # The original failing request
    original_payload = {
        "url": "https://www.ycombinator.com/about",
        "exclude_tags": "#introduction",
        "extract_main_content": True
    }
    
    print("\n=== Testing connector with original parameters ===")
    print(f"Sending request to connector: {json.dumps(original_payload, indent=2)}")
    
    connector_url = "http://localhost:2003/Firecrawl/v1/execute"
    response = requests.post(connector_url, json=original_payload)
    
    print(f"Response status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("SUCCESS: Connector request worked")
        
        if "result" in result and "data" in result["result"] and "markdown" in result["result"]["data"]:
            markdown_content = result["result"]["data"]["markdown"]
            print(f"\nMarkdown content from connector (first 300 chars): {markdown_content[:300]}...")
            
            # Verify introduction is excluded
            if "INTRODUCTION" not in markdown_content and "Introduction" not in markdown_content:
                print("\n✅ SUCCESS: Connector returns content without introduction!")
            else:
                print("\n❌ FAILURE: Connector response still contains introduction")
            
            # Compare with expected content
            expected_content = "# What Happens at YC"
            if expected_content in markdown_content:
                print("✅ Title is correct")
            else:
                print(f"❌ Title is missing or incorrect (should be '{expected_content}')")
            
            if "### THE YC PROGRAM" in markdown_content:
                print("✅ First section heading is correct")
            else:
                print("❌ First section heading is missing or incorrect (should be '### THE YC PROGRAM')")
    else:
        print("FAILURE: Connector request failed")
        try:
            error_data = response.json()
            print(f"Error details: {json.dumps(error_data, indent=2)}")
        except:
            print(f"Error: {response.text[:500]}")

if __name__ == "__main__":
    # First test the API directly
    test_firecrawl_api_directly()
    
    # Then test the connector
    test_connector() 