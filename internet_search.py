import json
from fastmcp import FastMCP
from duckduckgo_search import DDGS

# Initialize the FastMCP server
mcp = FastMCP("WebSearch")

@mcp.tool()
def search_internet(query: str, max_results: int = 5) -> str:
    """
    Search the internet using DuckDuckGo to get up-to-date information.
    
    Args:
        query: The search terms or question to look up.
        max_results: Maximum number of search snippets to return (default 5).
    """
    try:
        # Instantiate DDGS normally
        ddgs = DDGS()
        
        # Call text() and use list slicing to limit the results
        results = list(ddgs.text(query))[:max_results]
            
        if not results:
            return f"No results found for query: '{query}'"
            
        # Format the output clearly for the LLM
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
        return f"An error occurred while executing the search: {str(e)}"

if __name__ == "__main__":
    # FastMCP handles transport internally when run is called
    mcp.run(transport="http", host="0.0.0.0", port=8000)
