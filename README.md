# MCP Server Web Tools

This is a python bundle to use with the mcp python container:
https://github.com/ground-creative/mcp-container-python

## Installation

1. Follow instructions to install the MCP Python container from here:
   https://github.com/ground-creative/mcp-container-python

2. Clone the repository in folder mcp_server

```
cd mcp_servers
rm -rf tools
git clone https://github.com/ground-creative/mcp-web-tool-python.git tools
```

3. Create file /configlibs.json in root folder if it does not exist already, and add required dependencies:

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

5. Run the server

```
# Run via fastapi wrapper
python3 run.py -s fastapi

# Run the mcp server directly
python3 run.py -s fastmcp
```
