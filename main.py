import traceback
from fastmcp import FastMCP
from duckduckgo_search import DDGS

# Initialize FastMCP with a clean name
mcp = FastMCP("WebSearch")

@mcp.tool()
def search_internet(query: str, max_results: int = 5) -> str:
    """Search the internet using DuckDuckGo to get up-to-date information."""
    try:
        # DDGS works best when initialized inside the tool call loop
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
            
        if not results:
            return f"No results found for query: '{query}'"
            
        formatted_results = []
        for i, res in enumerate(results, 1):
            formatted_results.append(
                f"[{i}] {res.get('title')}\n"
                f"URL: {res.get('href')}\n"
                f"Snippet: {res.get('body')}\n"
                f"{'-'*40}"
            )
        return "\n\n".join(formatted_results)
        
    except Exception as e:
        print("=== SERVER ERROR EXCEPTION ===")
        traceback.print_exc()
        return f"An error occurred while executing the search: {str(e)}"

if __name__ == "__main__":
    # Use 'http' transport, binding to all interfaces, with an explicit path mapping
    mcp.run(transport="http", host="0.0.0.0", port=8000, path="/mcp")
