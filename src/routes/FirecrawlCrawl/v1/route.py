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
    Advanced website crawler using Firecrawl API:
    - Crawl multiple pages from a starting URL
    - Control crawl parameters like max pages, domain restriction
    - Filter content with CSS selectors
    - Wait for JavaScript, handle timeouts
    - Use stealth mode to avoid detection
    """
    print("======== Firecrawl Crawler endpoint called ========")
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
        
        # Build API payload with correct structure for Firecrawl API
        payload = {
            "url": url,
            "limit": int(data.get("max_pages", 10))
        }
        
        # Create scrapeOptions for parameters that should be nested
        scrape_options = {}
        
        # Handle boolean parameters with appropriate mapping to API format
        # stay_on_domain → inverse of allowExternalLinks (root level)
        stay_on_domain = data.get("stay_on_domain")
        if stay_on_domain is not None:
            if stay_on_domain is True or stay_on_domain == "true" or stay_on_domain == "True" or stay_on_domain == "1":
                payload["allowExternalLinks"] = False
            else:
                payload["allowExternalLinks"] = True
        
        # follow_links → allowBackwardLinks (root level)
        follow_links = data.get("follow_links")
        if follow_links is not None:
            if follow_links is True or follow_links == "true" or follow_links == "True" or follow_links == "1":
                payload["allowBackwardLinks"] = True
            else:
                payload["allowBackwardLinks"] = False
        
        # extract_main_content → onlyMainContent (in scrapeOptions)
        extract_main_content = data.get("extract_main_content")
        if extract_main_content is not None:
            if extract_main_content is True or extract_main_content == "true" or extract_main_content == "True" or extract_main_content == "1":
                scrape_options["onlyMainContent"] = True
            else:
                scrape_options["onlyMainContent"] = False
        
        # stealth_mode is not supported by the API, so we'll ignore it
        # No longer adding stealth_mode to scrapeOptions
        
        # Handle URL path filters
        # include_only_urls → includePaths (root level)
        include_only_urls = data.get("include_only_urls")
        if include_only_urls and isinstance(include_only_urls, list) and len(include_only_urls) > 0:
            payload["includePaths"] = include_only_urls
        
        # exclude_urls → excludePaths (root level)
        exclude_urls = data.get("exclude_urls")
        if exclude_urls and isinstance(exclude_urls, list) and len(exclude_urls) > 0:
            payload["excludePaths"] = exclude_urls
        
        # Handle tag filters (CSS selectors)
        # include_only_tags → includeTags (in scrapeOptions)
        include_only_tags = data.get("include_only_tags")
        if include_only_tags:
            tags_array = []
            # Convert to array if it's a string
            if isinstance(include_only_tags, str) and include_only_tags.strip():
                # Check if it's a comma-separated list
                if "," in include_only_tags:
                    tags_array = [tag.strip() for tag in include_only_tags.split(",") if tag.strip()]
                else:
                    tags_array = [include_only_tags.strip()]
            elif isinstance(include_only_tags, list):
                tags_array = include_only_tags
            
            if tags_array:
                # Use the documented API parameter name
                scrape_options["includeTags"] = tags_array
        
        # exclude_tags → excludeTags (in scrapeOptions)
        exclude_tags = data.get("exclude_tags")
        if exclude_tags:
            tags_array = []
            # Convert to array if it's a string
            if isinstance(exclude_tags, str) and exclude_tags.strip():
                # Check if it's a comma-separated list
                if "," in exclude_tags:
                    tags_array = [tag.strip() for tag in exclude_tags.split(",") if tag.strip()]
                else:
                    tags_array = [exclude_tags.strip()]
            elif isinstance(exclude_tags, list):
                tags_array = exclude_tags
            
            if tags_array:
                # Use the documented API parameter name
                scrape_options["excludeTags"] = tags_array
        
        # Handle numeric parameters
        # wait_for → waitFor (in scrapeOptions)
        wait_for = data.get("wait_for")
        if wait_for is not None:
            try:
                scrape_options["waitFor"] = int(wait_for)
            except (ValueError, TypeError):
                print(f"Invalid value for wait_for: {wait_for}")
        
        # timeout → timeout (in scrapeOptions)
        timeout = data.get("timeout")
        if timeout is not None:
            try:
                scrape_options["timeout"] = int(timeout)
            except (ValueError, TypeError):
                print(f"Invalid value for timeout: {timeout}")
        
        # Add scrapeOptions to the payload if we have any
        if scrape_options:
            payload["scrapeOptions"] = scrape_options
        
        print(f"Final Firecrawl crawler payload: {json.dumps(payload, indent=2)}")
        
        # Call Firecrawl API
        firecrawl_url = f"{FIRECRAWL_BASE_URL}/crawl"
        print(f"Calling API: {firecrawl_url}")
        print(f"With headers: {headers}")
        response = requests.post(firecrawl_url, headers=headers, json=payload)
        
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
        
        # Raise an exception if the response status is not successful
        response.raise_for_status()
        output = response.json()
        
        # Add execution metadata
        execution_time = time.time() - start_time
        
        # Format response
        result = {
            "crawl_results": output,
            "crawl_info": {
                "start_url": url,
                "pages_crawled": len(output) if isinstance(output, list) else 0,
                "crawler_parameters": payload,
                "execution_time_seconds": round(execution_time, 2)
            }
        }
        
        print(f"Returning success response with {len(output) if isinstance(output, list) else 0} pages crawled")
        return Response(
            data=result,
            metadata={"source": "Firecrawl API", "operation": "crawl"}
        )
        
    except Exception as e:
        print(f"Error in crawler endpoint: {str(e)}")
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