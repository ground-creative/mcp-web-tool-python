from utils.application.logger import logger
import requests
from utils.application.global_state import global_state
from pydantic import Field
from typing import Annotated, Dict

SERVICE_URL = "https://www.googleapis.com/customsearch/v1"


# X-GOOGLE-API-KEY and X-GOOGLE-CSE-ID need to be sent with headers
def search_google_tool(
    query: Annotated[
        str,
        Field(
            description="Required, the search query. Convert the query into a concise 3-4 word Google search term. Ex: 'Hotels in New York'"
        ),
    ],
    num: Annotated[
        int,
        Field(
            default=10,
            description="Required, number of results to fetch (max 10 per request). Default is 10. If more results are required, perform multiple searches incrementing the `start` parameter by 10 for each.",
        ),
    ] = 10,
    start: Annotated[
        int,
        Field(
            default=1,
            description="Required, the starting index for retrieving results, typically increments by 10.",
        ),
    ] = 1,
    filter: Annotated[
        str,
        Field(
            default=None,
            description="Optional, a site filter, e.g., 'example.com'. Use to restrict results to a specific site.",
        ),
    ] = None,
) -> Dict:
    """
    Use this tool to search on Google using Custom Search API and returns status code and either search results or error string.
    The `num` parameter cannot be more then 10. If more results are required, perform multiple searches incrementing the `start` value by 10 for each

    Request Body Parameters:
    - query (str): Required, this is the search query. Convert the query into a concise 3-4 word Google search term. Ex: "Hotels in New York"
    - num (int): Required, number of results to fetch (max 10 per request).
    - start (int): Required, the starting index for retrieving results, typically increments by 10.
    - filter (str): Optional, site filter (e.g., "example.com").

    Example Request Payload:
    {
        "query": "Hotels in New York"
        "depth": 10,   # get 10 results
        "start": 1     # Get results from first page
    }

    Example Request Payload From Second Page:
    {
        "query": "Hotels in Singapore",
        "depth": 10,                # get 10 results
        "start": 11                 # get results of second page
    }

    Example Response (200 OK):
    {
        "data": {
            "page_title": "Example Title",
            "content_chunks": ["chunk1", "chunk2"],
            "total_chars": 1024
        }
    }
    """
    params = {
        "q": query,
        "key": global_state.get("google_api_key"),
        "cx": global_state.get("google_cse_id"),
        "num": num,
        "start": start,
    }

    logger.info(
        f"Starting google search with query `{query} ` num `{num} start {start}`"
    )

    try:
        response = requests.get(SERVICE_URL, params=params)

        # If the request is successful (status code 200)
        if response.status_code == 200:
            results = response.json()

            if "items" in results:
                search_results = [
                    {
                        "title": item["title"],
                        "link": item["link"],
                        "snippet": item["snippet"],
                    }
                    for item in results["items"]
                ]

                # Apply site filter if provided
                if filter:
                    search_results = [
                        result for result in search_results if filter in result["link"]
                    ]

                return response.status_code, search_results

            # If no items are found, return an empty list
            return response.status_code, []

        # If the request fails, return the error string with the status code
        return response.status_code, f"Search request failed: {response.text}"

    except requests.exceptions.RequestException as e:
        # Handle any request exceptions
        return 500, f"Search request failed: {str(e)}"
