import requests
import json
import time

# Test the FirecrawlExtract endpoint with YC consumer companies request
base_url = "http://localhost:2003"

print("=== Testing FirecrawlExtract endpoint for YC W24 consumer companies ===")

# Test data
test_data = {
    "data": {
        "extract_prompt": "@https://www.ycombinator.com/companies/ Get me the W24 companies that are on the consumer space"
    }
}

print(f"Sending request to: {base_url}/FirecrawlExtract/v1/execute")
print(f"Test data: {json.dumps(test_data, indent=2)}")

try:
    start_time = time.time()
    response = requests.post(
        f"{base_url}/FirecrawlExtract/v1/execute",
        json=test_data,
        timeout=30
    )
    execution_time = time.time() - start_time
    
    print(f"Status code: {response.status_code}")
    print(f"Execution time: {round(execution_time, 2)} seconds")
    
    if response.status_code == 200:
        result = response.json()
        print("Success! Response structure:")
        print(f"Keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
        
        # Extract and display the actual company data
        if "extracted_elements" in result:
            elements = result["extracted_elements"]
            if isinstance(elements, list):
                print(f"Found {len(elements)} companies:")
                for i, company in enumerate(elements[:10]):  # Show first 10
                    if isinstance(company, dict):
                        name = company.get("name", company.get("company", "Unknown"))
                        batch = company.get("batch", "Unknown")
                        print(f"  {i+1}. {name} ({batch})")
                    else:
                        print(f"  {i+1}. {company}")
            elif isinstance(elements, dict) and "companies" in elements:
                companies = elements["companies"]
                print(f"Found {len(companies)} companies:")
                for i, company in enumerate(companies[:10]):  # Show first 10
                    if isinstance(company, dict):
                        name = company.get("name", company.get("company", "Unknown"))
                        batch = company.get("batch", "Unknown")
                        print(f"  {i+1}. {name} ({batch})")
                    else:
                        print(f"  {i+1}. {company}")
            else:
                print(f"Extracted elements structure: {json.dumps(elements, indent=2)}")
            
        # Show extraction info if available
        if "extraction_info" in result:
            print(f"Extraction info: {json.dumps(result['extraction_info'], indent=2)}")
    else:
        print("Error response:")
        try:
            error_data = response.json()
            print(json.dumps(error_data, indent=2))
        except:
            print(f"Raw response: {response.text[:1000]}")
            
except Exception as e:
    print(f"Exception occurred: {str(e)}") 