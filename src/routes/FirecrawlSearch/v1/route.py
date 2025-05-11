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
    Web Search functionality using Firecrawl API:
    - Search the web with customizable parameters
    - Get search results with full content
    - Filter by language, country, and time
    """
    print("======== Firecrawl Search endpoint called ========")
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
        # Get query (required)
        query = data.get("query")
        print(f"Search query: {query}")
        
        if not query:
            print("Query is missing")
            return Response(
                data={"error": "Search query is required"},
                status_code=400
            )

        # Print full data for debugging
        print(f"Full form data: {json.dumps(data, indent=2)}")
        
        # Build API payload
        payload = {
            "query": query
        }
        
        # Result limit
        limit = data.get("limit")
        if limit is not None:
            try:
                limit = int(limit)
                payload["limit"] = limit
            except (ValueError, TypeError):
                print(f"Invalid value for limit: {limit}, using default")
        
        # Language
        lang = data.get("lang")
        if lang and lang.strip():
            payload["lang"] = lang.strip()
        
        # Country
        country = data.get("country")
        if country and country.strip():
            payload["country"] = country.strip()
        
        # Time-based search
        tbs = data.get("tbs")
        if tbs and tbs.strip():
            payload["tbs"] = tbs.strip()
        
        # Scrape options - get full content if requested
        scrape_results = data.get("scrape_results")
        if scrape_results:
            payload["scrapeOptions"] = {
                "formats": ["markdown", "links"]
            }
        
        print(f"Final Firecrawl search payload: {json.dumps(payload, indent=2)}")
        
        # Call Firecrawl API search endpoint
        firecrawl_url = f"{FIRECRAWL_BASE_URL}/search"
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
        
        # Get the number of results
        results_count = len(output.get("data", [])) if isinstance(output.get("data"), list) else 0
        
        # Format response
        result = {
            "search_results": output.get("data", []),
            "search_info": {
                "query": query,
                "results_count": results_count,
                "parameters": payload,
                "execution_time_seconds": round(execution_time, 2)
            }
        }
        
        print(f"Returning success response with {results_count} search results")
        return Response(
            data=result,
            metadata={"source": "Firecrawl API", "operation": "search"}
        )
        
    except Exception as e:
        print(f"Error in search endpoint: {str(e)}")
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