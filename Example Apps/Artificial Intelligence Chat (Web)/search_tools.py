"""
Search tools for Artificial Intelligence Chat.

Provides web search and Prohelion documentation search tools
for LangChain integration.
"""

from langchain_core.tools import StructuredTool
from typing import List
import os

# Try to import langchain-community for DuckDuckGo search
try:
    from langchain_community.tools import DuckDuckGoSearchRun
    LANGCHAIN_DUCKDUCKGO_AVAILABLE = True
except ImportError:
    LANGCHAIN_DUCKDUCKGO_AVAILABLE = False

# Try to import ddgs as fallback
try:
    from ddgs import DDGS
    DDGS_AVAILABLE = True
except ImportError:
    DDGS_AVAILABLE = False


def create_web_search_tool() -> StructuredTool:
    """
    Create a web search tool using DuckDuckGo.
    
    Returns:
        StructuredTool for web search, or None if not available
    """
    # Try LangChain's built-in DuckDuckGo search tool first
    if LANGCHAIN_DUCKDUCKGO_AVAILABLE:
        try:
            web_search_tool = DuckDuckGoSearchRun()
            print(f"[TOOLS] Added web_search tool (LangChain DuckDuckGo)")
            return web_search_tool
        except Exception as e:
            print(f"[TOOLS] Error creating LangChain DuckDuckGo tool: {e}")
    
    # Fallback to custom implementation using ddgs
    if DDGS_AVAILABLE:
        try:
            def web_search(query: str) -> str:
                """Search the web using DuckDuckGo. Use this to find current information, documentation, or general knowledge."""
                try:
                    print(f"[SEARCH] Web search: {query}")
                    with DDGS() as ddgs:
                        results = list(ddgs.text(query, max_results=5))
                        if not results:
                            return f"No results found for: {query}"
                        
                        formatted_results = []
                        for result in results:
                            title = result.get('title', 'No title')
                            body = result.get('body', 'No description')
                            href = result.get('href', '')
                            formatted_results.append(
                                f"Title: {title}\n"
                                f"URL: {href}\n"
                                f"Description: {body}\n"
                            )
                        return "\n".join(formatted_results)
                except Exception as e:
                    return f"Error searching web: {str(e)}"
            
            web_search_tool = StructuredTool.from_function(
                func=web_search,
                name="web_search",
                description="Search the web using DuckDuckGo. Use this to find current information, documentation, or general knowledge."
            )
            print(f"[TOOLS] Added web_search tool (custom ddgs)")
            return web_search_tool
        except Exception as e:
            print(f"[TOOLS] Error creating custom DuckDuckGo tool: {e}")
    
    print(f"[TOOLS] Web search not available. Install with: pip install langchain-community or pip install ddgs")
    return None


def create_docs_search_tool() -> StructuredTool:
    """
    Create a Prohelion documentation search tool.
    
    Returns:
        StructuredTool for docs search, or None if not available
    """
    if not DDGS_AVAILABLE:
        print(f"[TOOLS] DuckDuckGo search not available for docs search. Install with: pip install ddgs")
        return None
    
    try:
        # Get docs URL from environment or use default
        docs_url = os.getenv("PROHELION_DOCS_URL", "https://docs.prohelion.com")
        
        def docs_search(query: str) -> str:
            """Search the Prohelion documentation site. Use this when the user asks about Prohelion features, configuration, setup, or how to use something."""
            try:
                print(f"[SEARCH] Docs search: {query}")
                # Search with site: filter for Prohelion docs
                search_query = f"site:{docs_url} {query}"
                with DDGS() as ddgs:
                    results = list(ddgs.text(search_query, max_results=5))
                    if not results:
                        return f"No results found in Prohelion documentation for: {query}"
                    
                    formatted_results = []
                    for result in results:
                        title = result.get('title', 'No title')
                        body = result.get('body', 'No description')
                        href = result.get('href', '')
                        formatted_results.append(
                            f"Title: {title}\n"
                            f"URL: {href}\n"
                            f"   {body}\n"
                        )
                    return "\n".join(formatted_results)
            except Exception as e:
                return f"Error searching documentation: {str(e)}"
        
        docs_search_tool = StructuredTool.from_function(
            func=docs_search,
            name="prohelion_docs_search",
            description=f"Search the Prohelion documentation site at {docs_url}. Use this when the user asks about Prohelion features, configuration, setup, or how to use something. Always use this tool for Prohelion-related questions."
        )
        print(f"[TOOLS] Added prohelion_docs_search tool for {docs_url}")
        return docs_search_tool
    except Exception as e:
        print(f"[TOOLS] Error creating docs search tool: {e}")
        return None


def create_search_tools() -> List[StructuredTool]:
    """
    Create all available search tools.
    
    Returns:
        List of StructuredTool objects for search functionality
    """
    tools = []
    
    # Add web search tool
    web_tool = create_web_search_tool()
    if web_tool:
        tools.append(web_tool)
    
    # Add docs search tool
    docs_tool = create_docs_search_tool()
    if docs_tool:
        tools.append(docs_tool)
    
    return tools
