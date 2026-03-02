"""
Model management for Artificial Intelligence Chat.

Handles Ollama model initialization, caching, tool binding, and keyword management.
"""

from langchain_ollama import ChatOllama
from langchain_core.tools import StructuredTool
from typing import List, Optional, Dict
import os

# Try to import langchain-mcp-adapters for tool binding
# Note: Import check and warning is handled in mcp_client.py to avoid duplicate messages
try:
    from langchain_mcp_adapters.tools import load_mcp_tools
    MCP_ADAPTERS_AVAILABLE = True
except ImportError:
    MCP_ADAPTERS_AVAILABLE = False
    # Warning message is printed in mcp_client.py to avoid duplicates

from mcp_client import run_async_in_loop, load_mcp_tools_from_session
from search_tools import create_search_tools
from auth_manager import get_auth_token

# Configuration - will be set by main app
OLLAMA_MODEL = None

# Model cache - maps cache_key -> ChatOllama instance
model_cache: Dict[str, ChatOllama] = {}
current_model_name: Optional[str] = None

# Tool registry - maps tool name -> tool object (for LangChain tools) or None (for MCP tools)
tool_registry: Dict[str, Optional[StructuredTool]] = {}

# Component names for keyword matching (updated when components are loaded)
component_names: List[str] = []

# Base keywords for Profinity queries
BASE_KEYWORDS = [
    'profinity', 'prohelion', 'component', 'signal', 'message', 'dbc',
    'battery', 'voltage', 'temperature', 'profile'
]


def initialize_model_config(default_model: str):
    """
    Initialize model configuration.
    Called by main app during startup.
    
    Args:
        default_model: Default Ollama model name
    """
    global OLLAMA_MODEL
    OLLAMA_MODEL = default_model


def update_keywords_from_components(components: List[str]) -> None:
    """
    Update component names list for keyword matching.
    Called after components are loaded during login.
    
    Args:
        components: List of component name strings
    """
    global component_names
    component_names = components
    print(f"[KEYWORDS] Updated keywords with {len(components)} component names")


def get_profinity_keywords() -> List[str]:
    """
    Get current Profinity keywords (base keywords + component names).
    
    Returns:
        List of keyword strings (all lowercase)
    """
    # Start with base keywords
    keywords = BASE_KEYWORDS.copy()
    
    # Add component names (convert to lowercase for matching)
    keywords.extend([name.lower() for name in component_names])
    
    # Add tokenized component names for better matching
    # (e.g., "WaveSculptor Left" from "Prohelion WaveSculptor 22 - Left")
    for name in component_names:
        # Split on common separators and add individual tokens
        tokens = name.lower().replace('-', ' ').replace('_', ' ').split()
        keywords.extend(tokens)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_keywords = []
    for kw in keywords:
        if kw not in seen:
            seen.add(kw)
            unique_keywords.append(kw)
    
    return unique_keywords


def check_needs_mcp(query: str) -> tuple[bool, List[str]]:
    """
    Check if query needs MCP tools based on keyword matching.
    
    Args:
        query: User query string
    
    Returns:
        Tuple of (needs_mcp: bool, matched_keywords: List[str])
    """
    profinity_keywords = get_profinity_keywords()
    query_lower = query.lower()
    matched_keywords = [kw for kw in profinity_keywords if kw in query_lower]
    needs_mcp = len(matched_keywords) > 0
    
    print(f"[KEYWORDS] Query: {query}")
    print(f"[KEYWORDS] Component names loaded: {len(component_names)} - {component_names[:5] if component_names else []}...")
    print(f"[KEYWORDS] Total profinity keywords: {len(profinity_keywords)}")
    print(f"[KEYWORDS] Matched keywords: {matched_keywords}")
    print(f"[KEYWORDS] Needs MCP: {needs_mcp}")
    
    return needs_mcp, matched_keywords


def clear_model_cache() -> None:
    """
    Clear the model cache.
    Called on login/logout to ensure models are reloaded with correct authentication.
    """
    global model_cache, tool_registry, current_model_name
    
    count = len(model_cache)
    model_cache.clear()
    tool_registry = {}
    current_model_name = None
    print(f"[MODEL] Cleared model cache ({count} models)")


def get_model(model_name: Optional[str] = None, bind_tools: bool = False) -> ChatOllama:
    """
    Get or initialize the Ollama model.
    If model_name is provided, uses that model. Otherwise uses the default from config.
    Models are cached by name to avoid recreating them unnecessarily.
    
    If bind_tools is True, binds MCP tools to the model for function calling.
    
    Args:
        model_name: Name of the Ollama model (uses default if None)
        bind_tools: Whether to bind tools to the model
    
    Returns:
        ChatOllama model instance
    """
    global model_cache, current_model_name, tool_registry
    
    print(f"[MODEL] get_model() called: model_name={model_name}, bind_tools={bind_tools}")
    
    # Use provided model name, or default from config
    if model_name is None or model_name == "":
        model_name = OLLAMA_MODEL
        print(f"[MODEL] Using default model: {model_name}")
    
    # Create cache key that includes whether tools are bound
    cache_key = f"{model_name}_tools" if bind_tools else model_name
    
    # Log cache state
    print(f"[MODEL] Cache key: '{cache_key}' (bind_tools={bind_tools})")
    print(f"[MODEL] Cache contains keys: {list(model_cache.keys())}")
    
    # If we already have this model cached, return it
    if cache_key in model_cache:
        print(f"[MODEL] ⚠ Using cached model with key '{cache_key}'")
        print(f"[MODEL] ⚠ NOTE: Tools listing messages only appear when creating NEW models, not cached ones")
        if current_model_name != model_name:
            print(f"[MODEL] Switching to cached model: {model_name} (tools: {bind_tools})")
            current_model_name = model_name
        cached_model = model_cache[cache_key]
        # Check if cached model has tools
        if hasattr(cached_model, 'bound_tools') and cached_model.bound_tools:
            print(f"[MODEL] Cached model has {len(cached_model.bound_tools)} tools bound")
            print(f"[MODEL] Cached model tools:")
            for tool in cached_model.bound_tools:
                tool_name = tool.name if hasattr(tool, 'name') else str(tool)
                print(f"[MODEL]   - {tool_name}")
        elif hasattr(cached_model, 'lc_kwargs') and 'tools' in getattr(cached_model, 'lc_kwargs', {}):
            print(f"[MODEL] Cached model has tools in lc_kwargs")
        else:
            print(f"[MODEL] ⚠ Cached model does NOT have tools bound")
        return cached_model
    
    print(f"[MODEL] Creating NEW model (not in cache) - tool listing will appear below")
    
    # Create new model instance
    print(f"[MODEL] ========== CREATING NEW MODEL INSTANCE ==========")
    print(f"[MODEL] Initializing new model: {model_name} (tools: {bind_tools})")
    new_model = ChatOllama(
        model=model_name,
        temperature=0.1,
        timeout=300
    )
    
    # Bind tools if requested
    if bind_tools:
        print(f"[MODEL] bind_tools=True - will load and bind tools now...")
        tool_registry = {}  # Reset tool registry for this model
        all_tools = []
        
        # Load MCP tools
        if MCP_ADAPTERS_AVAILABLE:
            try:
                # Check if we have a token before attempting to load tools
                token = get_auth_token()
                print(f"[MODEL] Token check: {'Available' if token else 'NOT available'}")
                if token:
                    token_preview = f"{token[:10]}...{token[-10:]}" if len(token) > 20 else "***"
                    print(f"[MODEL] Token preview: {token_preview} (length: {len(token)})")
                if not token:
                    print(f"[MODEL] WARNING: No authentication token available - cannot load MCP tools")
                    print(f"[MODEL] Tools will not be available until user logs in")
                    print(f"[MODEL] To use MCP tools, please log in via the login form or set PROFINITY_TOKEN environment variable")
                else:
                    print(f"[MODEL] Token available, loading MCP tools...")
                    mcp_tools = run_async_in_loop(load_mcp_tools_from_session())
                    if mcp_tools:
                        all_tools.extend(mcp_tools)
                        # Register MCP tools (they don't have direct invoke, so mark as None)
                        for tool in mcp_tools:
                            tool_name = tool.name if hasattr(tool, 'name') else str(tool)
                            tool_registry[tool_name] = None  # None means it's an MCP tool
                        print(f"[MODEL] Loaded {len(mcp_tools)} MCP tools")
                    else:
                        print(f"[MODEL] No MCP tools loaded (empty list returned)")
            except Exception as e:
                print(f"[MODEL] Error loading MCP tools: {e}")
                import traceback
                traceback.print_exc()
        
        # Load search tools
        search_tools = create_search_tools()
        if search_tools:
            all_tools.extend(search_tools)
            # Register search tools (they are LangChain tools)
            for tool in search_tools:
                tool_name = tool.name if hasattr(tool, 'name') else str(tool)
                tool_registry[tool_name] = tool
            print(f"[MODEL] Loaded {len(search_tools)} search tools")
        
        # Log tool summary
        if all_tools:
            mcp_tool_names = [t.name if hasattr(t, 'name') else str(t) for t in all_tools if t.name in tool_registry and tool_registry[t.name] is None]
            search_tool_names = [t.name if hasattr(t, 'name') else str(t) for t in all_tools if t.name in tool_registry and tool_registry[t.name] is not None]
            
            print(f"[MODEL] ========== TOOLS BOUND TO MODEL ==========")
            print(f"[MODEL] Tool Summary:")
            print(f"[MODEL]   - MCP Tools: {len(mcp_tool_names)}")
            for name in mcp_tool_names:
                print(f"[MODEL]     • {name}")
            print(f"[MODEL]   - LangChain/Search Tools: {len(search_tool_names)}")
            for name in search_tool_names:
                print(f"[MODEL]     • {name}")
            print(f"[MODEL]   - Total: {len(all_tools)} tools")
            print(f"[MODEL] =================================================")
            
            new_model = new_model.bind_tools(all_tools)
            # Verify tools were bound
            if hasattr(new_model, 'bound_tools'):
                bound_count = len(new_model.bound_tools) if new_model.bound_tools else 0
                print(f"[MODEL] ✓ Tools bound successfully: {bound_count} tools")
                if new_model.bound_tools:
                    print(f"[MODEL] Verified bound tools:")
                    for tool in new_model.bound_tools:
                        tool_name = tool.name if hasattr(tool, 'name') else str(tool)
                        print(f"[MODEL]   ✓ {tool_name}")
            else:
                print(f"[MODEL] ⚠ bind_tools() called but bound_tools attribute not found")
        else:
            print(f"[MODEL] ⚠ WARNING: No tools available to bind!")
            print(f"[MODEL] This means the model will not be able to call any tools.")
    
    # Cache it
    model_cache[cache_key] = new_model
    current_model_name = model_name
    
    return new_model


def get_tool_registry() -> Dict[str, Optional[StructuredTool]]:
    """
    Get the current tool registry.
    
    Returns:
        Dictionary mapping tool names to tool objects (or None for MCP tools)
    """
    return tool_registry.copy()
