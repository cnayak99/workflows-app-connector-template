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

# Print debug information
print(f"Firecrawl route module loaded. Router: {router}")

# Firecrawl API constants
FIRECRAWL_API_KEY = "fc-5e15dc8f86e8483eaf4b66459fb97fcb"
FIRECRAWL_BASE_URL = "https://api.firecrawl.dev/v1"

@router.route("/execute", methods=["GET", "POST"])
def execute():
    """
    Simple Firecrawl website scraper with advanced options:
    - Exclude specific HTML tags
    - Include only specific HTML tags
    - Wait for JavaScript to load
    - Set request timeout
    - Extract only main content
    - Use stealth mode
    """
    print("======== Firecrawl scraper endpoint called via router ========")
    request = Request(flask_request)
    print(f"Request method via router: {flask_request.method}")
    print(f"Content-Type via router: {flask_request.headers.get('Content-Type')}")
    
    data = request.data
    print(f"Extracted data via router: {data}")
    
    # Check if data is nested inside a 'data' field
    if 'data' in data and isinstance(data['data'], dict):
        data = data['data']
        print(f"Using nested data via router: {data}")
    
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
        print(f"URL via router: {url}")
        
        if not url:
            print("URL is missing in router endpoint")
            return Response(
                data={"error": "URL is required"},
                status_code=400
            )
        
        # Build payload with all options
        payload = {
            "url": url
        }
        
        # Add optional parameters if they exist
        exclude_tags = data.get("exclude_tags")
        if exclude_tags:
            payload["excludeTags"] = [tag.strip() for tag in exclude_tags.split(",")]
        
        include_only_tags = data.get("include_only_tags")
        print(f"Raw include_only_tags: {include_only_tags!r}, type: {type(include_only_tags)}")
        if include_only_tags:
            # Simplify the logic to ensure we get a proper array
            if isinstance(include_only_tags, list):
                tags_array = include_only_tags
            else:
                # Convert to string, then handle as a single item
                include_only_tags_str = str(include_only_tags).strip()
                # Check if it's a comma-separated list
                if "," in include_only_tags_str:
                    tags_array = [tag.strip() for tag in include_only_tags_str.split(",") if tag.strip()]
                else:
                    # Just a single tag, add as-is to the array
                    tags_array = [include_only_tags_str]
                
            # Ensure we have a valid array that won't cause API errors
            if not tags_array:
                # Don't add empty array
                print("Not adding empty includeOnlyTags array")
            else:
                payload["includeOnlyTags"] = tags_array
                print(f"Final includeOnlyTags value: {payload['includeOnlyTags']!r}, type: {type(payload['includeOnlyTags'])}")
        
        wait_for = data.get("wait_for")
        if wait_for is not None:
            payload["waitFor"] = int(wait_for)
        
        timeout = data.get("timeout")
        if timeout is not None:
            payload["timeout"] = int(timeout)
        
        # New parameters
        extract_main_content = data.get("extract_main_content")
        print(f"extract_main_content via router: {extract_main_content}, type: {type(extract_main_content)}")
        
        if extract_main_content is not None and (extract_main_content is True or extract_main_content == "true" or extract_main_content == "True" or extract_main_content == "1"):
            payload["onlyMainContent"] = True
            print("Extract main content enabled via router")
        
        stealth_mode = data.get("stealth_mode")
        if stealth_mode is not None and (stealth_mode is True or stealth_mode == "true" or stealth_mode == "True" or stealth_mode == "1"):
            payload["stealthMode"] = True
        
        print(f"Final Firecrawl payload via router: {payload}")
        
        # Call Firecrawl API
        firecrawl_url = f"{FIRECRAWL_BASE_URL}/scrape"
        # Debug the exact JSON being sent
        print(f"Sending to {firecrawl_url} with exact JSON payload: {json.dumps(payload)}")
        
        response = requests.post(firecrawl_url, headers=headers, json=payload)
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {response.headers}")
        
        try:
            print(f"Response content: {response.content[:500]}")  # First 500 chars
        except:
            print("Could not print response content")
        
        response.raise_for_status()
        output = response.json()
        
        # Add execution metadata
        execution_time = time.time() - start_time
        
        # Format response
        result = {
            "result": output,
            "extraction_info": {
                "url": url,
                "type": "scrape",
                "parameters": payload,
                "execution_time_seconds": round(execution_time, 2)
            }
        }
        
        print(f"Returning success response via router")
        return Response(
            data=result,
            metadata={"source": "Firecrawl API", "operation": "scrape"}
        )
        
    except Exception as e:
        print(f"Error in router endpoint: {str(e)}")
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
        except:
            pass
        
        # Add execution metadata to error response
        execution_time = time.time() - start_time
        error_data["execution_metadata"] = {
            "execution_time_seconds": round(execution_time, 2),
            "success": False
        }
        
        print(f"Returning error response via router: {error_data}")
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

# Add a test utility route to validate the API directly
@router.route("/test_api", methods=["GET", "POST"])
def test_api():
    """Test the Firecrawl API with controlled parameters"""
    request = Request(flask_request)
    
    # Hardcoded test payload that should work
    test_payload = {
        "url": "https://www.ycombinator.com/about",
        "includeOnlyTags": ["article", "main"],  # Using known good tags
        "onlyMainContent": True
    }
    
    headers = {
        "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        print(f"Testing API with payload: {test_payload}")
        firecrawl_url = f"{FIRECRAWL_BASE_URL}/scrape"
        response = requests.post(firecrawl_url, headers=headers, json=test_payload)
        response.raise_for_status()
        
        return Response(
            data={
                "message": "API test successful",
                "status_code": response.status_code,
                "test_payload": test_payload,
                "response_snippet": response.text[:1000] if response.text else "No text response"
            }
        )
    except Exception as e:
        print(f"API test error: {str(e)}")
        return Response(
            data={
                "error": str(e),
                "test_payload": test_payload
            },
            status_code=500
        ) 