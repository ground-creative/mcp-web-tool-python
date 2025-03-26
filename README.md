# MCP Server Web Tools

This is a python bundle to use with the mcp python container:
https://github.com/ground-creative/mcp-container-python

## Installation

1. Follow instructions to install the MCP Python container from here:
   https://github.com/ground-creative/mcp-container-python

2. Clone the repository in folder mcp_server

```
cd mcp_server
rm -rf tools
git clone https://github.com/ground-creative/mcp-web-tool-python.git tools
```

3. Create file config/libs.json in root folder if it does not exist already, and add required dependencies:

```
[
  {
    "package": "selenium",
    "version": "4.30.0"
  },
  {
    "package": "typing_extensions",
    "version": "4.12.2"
  },
  {
    "package": "beautifulsoup4",
    "version": "4.13.3"
  }
]
```

4. Rebuild and run requirements engine

```
python3 utils/application/generate_requirements.py
pip install -r requirements.txt
```

5. Create file middlewares/api/SetGoogleCredentials.py with the following content:

```
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from utils.application.logger import logger
from utils.application.global_state import global_state


class SetGoogleCredentials(BaseHTTPMiddleware):
    def __init__(self, app, *args, **kwargs):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):

        content_type = request.headers.get("content-type", "")

        if content_type == "application/json":
            data = await request.json()
            method = data.get("method", "")
            params = data.get("params", {})

            if (
                method == "tools/call"
                and "name" in params
                and params["name"] == "search_google_tool"
            ):

                google_api_key = request.headers.get("x-google-api-key")

                # Check if API key is present and valid
                if not google_api_key:
                    logger.error("Google API key missing in request headers.")
                    # return JSONResponse(status_code=400, content={"detail": "API key missing."})

                global_state.set("google_api_key", google_api_key, True)

                google_cse_id = request.headers.get("x-google-csi-id")

                # Check if API key is present and valid
                if not google_api_key:
                    logger.error("Google CSI ID missing in request headers.")
                    # return JSONResponse(status_code=400, content={"detail": "API key missing."})

                global_state.set("google_cse_id", google_cse_id, True)

        # Proceed with the request
        response = await call_next(request)
        return response

```

6. crete file config/middlewares.py if it does not exist and add the middleware:

```
{
    "api": [
        {
            "middleware": "middlewares.api.SetGoogleCredentials",
            "priority": 1
        }
    ]
}
```

7. Run the server

```
# Run via fastapi wrapper
python3 run.py -s fastapi

# Run the mcp server directly
python3 run.py -s fastmcp
```
