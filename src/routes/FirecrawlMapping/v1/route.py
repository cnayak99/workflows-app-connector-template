from workflows_cdk import Response, Request
from flask import request as flask_request
import requests
import sys
import os
import json
import time

# Add the project root to the path so we can import from main
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))
from main import router, app

# Firecrawl API constants
FIRECRAWL_API_KEY = "fc-1956059de87d45ceba43c29343869685"
FIRECRAWL_BASE_URL = "https://api.firecrawl.dev/v1"

@router.route("/execute", methods=["GET", "POST"])
def execute():
    """
    Website URL mapper using Firecrawl API:
    - Discover all URLs on a website
    - Get a complete sitemap without full crawling
    - Efficiently map large websites
    """
    print("======== Firecrawl Mapping endpoint called ========")
    request = Request(flask_request)
    print(f"Request method: {flask_request.method}")
    print(f"Content-Type: {flask_request.headers.get('Content-Type')}")
    
    data = request.data
    print(f"Extracted data: {data}")
    print(f"Raw data type: {type(data)}")
    
    # Check if data is nested inside a 'data' field
    if 'data' in data and isinstance(data['data'], dict):
        data = data['data']
        print(f"Using nested data: {data}")
    
    # Add timestamp for tracking
    start_time = time.time()
    
    # Set up Firecrawl API request
    headers = {
        "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        # Get URL (required)
        url = data.get("url")
        print(f"URL: {url}")
        
        if not url:
            print("URL is missing")
            return Response(
                data={"error": "URL is required"},
                status_code=400
            )

        # Print full data for debugging
        print(f"Full form data: {json.dumps(data, indent=2)}")
        
        # Build API payload
        payload = {
            "url": url
        }
        
        # Search Beta - now a text input
        search_beta = data.get("search_beta")
        if search_beta and isinstance(search_beta, str) and search_beta.strip():
            payload["search"] = search_beta.strip()
        
        # Include subdomains
        include_subdomains = data.get("include_subdomains")
        if include_subdomains is not None and include_subdomains:
            payload["includeSubdomains"] = True
        
        # Ignore sitemap
        ignore_sitemap = data.get("ignore_sitemap")
        if ignore_sitemap is not None and ignore_sitemap:
            payload["ignoreSitemap"] = True
            
        # Handle extract_main_content parameter - this is meant for scrape, not map
        # If user provides this parameter, inform them it's not applicable to mapping
        extract_main_content = data.get("extract_main_content")
        if extract_main_content is not None:
            print("WARNING: extract_main_content parameter provided but not applicable to mapping endpoint.")
            print("This parameter is meant for content extraction, not URL mapping.")
        
        print(f"Final Firecrawl map payload: {json.dumps(payload, indent=2)}")
        
        # Add timeout parameters to prevent request hanging
        timeout_seconds = 60  # Default 60 second timeout 
        
        # Implement retry logic with exponential backoff
        max_retries = 3
        retry_delay = 2
        response = None
        last_error = None
        
        for retry_attempt in range(max_retries):
            try:
                # Call Firecrawl API map endpoint with timeout
                firecrawl_url = f"{FIRECRAWL_BASE_URL}/map"
                print(f"Calling API: {firecrawl_url} (Attempt {retry_attempt + 1}/{max_retries})")
                response = requests.post(
                    firecrawl_url, 
                    headers=headers, 
                    json=payload, 
                    timeout=timeout_seconds
                )
                
                print(f"Response status: {response.status_code}")
                try:
                    response_content = response.text[:1000]
                    print(f"Response preview: {response_content}")
                    
                    # Try to parse JSON if available
                    try:
                        response_json = response.json()
                        print(f"Response JSON: {json.dumps(response_json)}")
                    except:
                        print("Response is not JSON format")
                except:
                    print("Could not print response content")
                
                # Break out of retry loop if successful
                if response.status_code == 200:
                    break
                    
                # If we get a 408 timeout or 429 rate limit, retry with backoff
                if response.status_code in [408, 429]:
                    wait_time = retry_delay * (2 ** retry_attempt)
                    print(f"Request {response.status_code} error, retrying after {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                    
                # For other error codes, raise exception
                response.raise_for_status()
                    
            except requests.exceptions.Timeout:
                wait_time = retry_delay * (2 ** retry_attempt)
                print(f"Request timed out, retrying after {wait_time} seconds...")
                time.sleep(wait_time)
                last_error = f"Request timed out after {timeout_seconds} seconds"
                
            except requests.exceptions.RequestException as e:
                last_error = str(e)
                if retry_attempt < max_retries - 1:
                    wait_time = retry_delay * (2 ** retry_attempt)
                    print(f"Request failed: {str(e)}, retrying after {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    break
        
        # Check if we have a response after retries
        if response is None:
            raise Exception(f"Failed to get response after {max_retries} attempts: {last_error}")
                
        # Raise an exception if the response status is not successful
        response.raise_for_status()
        output = response.json()
        
        # Add execution metadata
        execution_time = time.time() - start_time
        
        # Format response
        result = {
            "map_results": output,
            "map_info": {
                "start_url": url,
                "urls_found": len(output.get("links", [])) if isinstance(output.get("links"), list) else 0,
                "parameters": payload,
                "execution_time_seconds": round(execution_time, 2)
            }
        }
        
        print(f"Returning success response with {len(output.get('links', [])) if isinstance(output.get('links'), list) else 0} URLs mapped")
        return Response(
            data=result,
            metadata={"source": "Firecrawl API", "operation": "map"}
        )
        
    except Exception as e:
        print(f"Error in map endpoint: {str(e)}")
        error_message = str(e)
        error_data = {"error": error_message}
        
        try:
            if hasattr(e, 'response') and e.response:
                error_response = e.response.json() 
                error_data = {
                    "error": error_response.get('error', error_message),
                    "status_code": e.response.status_code,
                    "details": error_response
                }
                
                # Add specific error messaging for common issues
                if hasattr(e.response, 'status_code'):
                    status_code = e.response.status_code
                    if status_code == 408:
                        error_data["user_message"] = "The request timed out. The mapping operation for this URL is taking too long to complete. Try with a more specific URL or disable 'include_subdomains' to reduce scope."
        except:
            pass
            
        # Check if extract_main_content was provided, as this is a common mistake
        if data.get("extract_main_content") is not None:
            error_data["user_message"] = "The 'extract_main_content' parameter is not applicable to the mapping endpoint. If you want to extract content from a webpage, please use the FirecrawlExtract endpoint instead."
        
        # Add execution metadata to error response
        execution_time = time.time() - start_time
        error_data["execution_metadata"] = {
            "execution_time_seconds": round(execution_time, 2),
            "success": False
        }
        
        print(f"Returning error response: {error_data}")
        return Response(
            data=error_data,
            status_code=500
        )

@router.route("/content", methods=["GET", "POST"])
def content():
    """
    This function provides dynamic content options for form fields.
    Currently not used as all fields are static.
    """
    request = Request(flask_request)
    data = request.data
    content_objects = []
    
    return Response(data={"content_objects": content_objects}) 