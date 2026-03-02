"""
MCP client for Artificial Intelligence Chat.

Handles MCP session creation, tool loading, tool execution, and component loading
with detailed logging.
"""

import json
import time
import asyncio
import threading
import httpx
from typing import Dict, List, Optional, Tuple, Any
from flask import has_request_context

# MCP Python SDK imports - required
try:
    from mcp import ClientSession
    from mcp.client.sse import sse_client
    MCP_SDK_AVAILABLE = True
except ImportError as e:
    MCP_SDK_AVAILABLE = False
    raise ImportError(
        "MCP Python SDK is required. Install with:\n"
        "pip install git+https://github.com/modelcontextprotocol/python-sdk.git\n"
        f"Original error: {e}"
    )

# Try to import langchain-mcp-adapters for tool binding
try:
    from langchain_mcp_adapters.tools import load_mcp_tools
    MCP_ADAPTERS_AVAILABLE = True
except ImportError as e:
    MCP_ADAPTERS_AVAILABLE = False
    # Only print warning once - check if it's a missing package vs missing submodule
    import_error_msg = str(e)
    if "No module named 'langchain_mcp_adapters'" in import_error_msg:
        print("[WARNING] langchain-mcp-adapters package not found. Install with: pip install langchain-mcp-adapters")
    elif "cannot import name 'load_mcp_tools'" in import_error_msg or "No module named 'langchain_mcp_adapters.tools'" in import_error_msg:
        print(f"[WARNING] langchain-mcp-adapters installed but tools submodule missing. Error: {import_error_msg}")
        print("[WARNING] Try: pip install --upgrade langchain-mcp-adapters")
    else:
        print(f"[WARNING] langchain-mcp-adapters import failed: {import_error_msg}")
        print("[WARNING] Try: pip install --upgrade langchain-mcp-adapters")

from auth_manager import get_auth_token, refresh_auth_token_sync, TokenExpiredError

# Configuration - will be set by main app
PROFINITY_MCP_URL = None
PROFINITY_BASE_URL = None

# Persistent event loop for async operations (runs in background thread)
_async_loop = None
_async_thread = None
_loop_lock = threading.Lock()


def initialize_mcp_config(mcp_url: str, base_url: str):
    """
    Initialize MCP configuration.
    Called by main app during startup.
    
    Args:
        mcp_url: MCP server URL (SSE endpoint)
        base_url: Profinity base URL
    """
    global PROFINITY_MCP_URL, PROFINITY_BASE_URL
    PROFINITY_MCP_URL = mcp_url
    PROFINITY_BASE_URL = base_url


def get_or_create_event_loop() -> asyncio.AbstractEventLoop:
    """
    Get or create the persistent event loop for async operations.
    The loop runs in a background thread to avoid blocking the main thread.
    
    Returns:
        Event loop instance
    """
    global _async_loop, _async_thread, _loop_lock
    
    with _loop_lock:
        if _async_loop is not None and not _async_loop.is_closed():
            return _async_loop
        
        # Create new event loop in a background thread
        loop_ref = {'loop': None}
        loop_ready = threading.Event()
        
        def run_event_loop():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop_ref['loop'] = loop
            loop_ready.set()
            loop.run_forever()
        
        _async_thread = threading.Thread(target=run_event_loop, daemon=True)
        _async_thread.start()
        
        # Wait for the loop to be created
        if not loop_ready.wait(timeout=2.0):
            raise RuntimeError("Failed to create event loop: timeout")
        
        _async_loop = loop_ref['loop']
        
        # Verify loop is running
        if _async_loop is None or _async_loop.is_closed():
            raise RuntimeError("Failed to create event loop: invalid state")
    
    return _async_loop


def run_async_in_loop(coro):
    """
    Run an async coroutine in the persistent event loop from a sync context.
    This is thread-safe and much faster than creating new event loops.
    
    Args:
        coro: Async coroutine to run
    
    Returns:
        Result of the coroutine, or error dict if operation fails
    """
    loop = get_or_create_event_loop()
    future = asyncio.run_coroutine_threadsafe(coro, loop)
    try:
        return future.result(timeout=60)  # 60 second timeout
    except asyncio.TimeoutError:
        future.cancel()
        return {"error": "Operation timed out after 60 seconds"}
    except Exception as e:
        return {"error": f"Error running async operation: {str(e)}"}


def shutdown_event_loop():
    """Shutdown the persistent event loop cleanly"""
    global _async_loop, _async_thread, _loop_lock
    
    with _loop_lock:
        if _async_loop is not None:
            try:
                if not _async_loop.is_closed():
                    # Schedule shutdown
                    _async_loop.call_soon_threadsafe(_async_loop.stop)
            except Exception as e:
                print(f"[MCP] Error stopping event loop: {e}")
            
            if _async_thread is not None:
                _async_thread.join(timeout=5)
            
            if _async_loop is not None:
                try:
                    if not _async_loop.is_closed():
                        _async_loop.close()
                except Exception as e:
                    print(f"[MCP] Error closing event loop: {e}")
            
            _async_loop = None
            _async_thread = None


async def create_mcp_session() -> Tuple[ClientSession, Any]:
    """
    Create a new MCP client session for a single operation.
    This is simpler and more reliable than maintaining a persistent session.
    
    Since MCP calls are fast (< 1 second), creating a new session per call
    avoids thread-safety issues and timeout problems with persistent connections.
    
    Returns:
        (session, session_context) tuple - both must be cleaned up after use
    
    Raises:
        ValueError: If no token is available
        TokenExpiredError: If token refresh fails with 401
        ConnectionError: If connection to MCP server fails
    """
    # Get token (from session, command line, or env)
    token = get_auth_token()
    
    if not token:
        raise ValueError(
            "No authentication token available. Please log in using the login form or provide a token via command line or environment variable."
        )
    
    # Refresh token if using session token (not command line token)
    if has_request_context():
        try:
            from flask import session as flask_session
            if 'auth_token' in flask_session:
                try:
                    token = refresh_auth_token_sync(token)
                except TokenExpiredError:
                    # Token expired - re-raise so caller can handle it
                    raise
                except Exception as e:
                    print(f"[AUTH] Token refresh failed (non-fatal): {e}")
                    # If refresh fails for other reasons (network error, etc.), try using the old token anyway
        except RuntimeError:
            # Outside request context - skip token refresh
            pass
    
    # Clean token (remove any whitespace/newlines)
    clean_token = token.strip()
    if not clean_token:
        raise ValueError("Token is empty after stripping whitespace.")
    
    # Connection timeout
    connection_timeout = 10.0  # 10 seconds is plenty for establishing connection
    
    # Log token info (without exposing the actual token)
    token_preview = f"{clean_token[:10]}...{clean_token[-10:]}" if len(clean_token) > 20 else "***"
    print(f"[MCP] Connecting to {PROFINITY_MCP_URL} with token: {token_preview} (length: {len(clean_token)})")
    
    # Log the SSE connection request details
    print(f"[MCP SSE CONNECTION] ========== SSE CONNECTION REQUEST ==========")
    print(f"[MCP SSE CONNECTION] URL: {PROFINITY_MCP_URL}")
    print(f"[MCP SSE CONNECTION] Headers: Authorization: Bearer {token_preview}")
    print(f"[MCP SSE CONNECTION] Timeout: {connection_timeout}s")
    print(f"[MCP SSE CONNECTION] ===========================================")
    
    # sse_client is an async context manager that yields (read_stream, write_stream)
    try:
        session_context = sse_client(
            url=PROFINITY_MCP_URL,
            headers={
                "Authorization": f"Bearer {clean_token}"
            },
            timeout=connection_timeout
        )
        
        # Enter the context manager to get (read_stream, write_stream) tuple
        print(f"[MCP SSE CONNECTION] Entering SSE context manager...")
        streams = await session_context.__aenter__()
        read_stream, write_stream = streams
        print(f"[MCP SSE CONNECTION] SSE streams obtained")
    except (httpx.ConnectError, httpx.ConnectTimeout) as e:
        raise ConnectionError(
            f"Unable to connect to Profinity server at {PROFINITY_MCP_URL}. "
            f"Please ensure Profinity is running and the MCP server is enabled (EnableMcpServer: true)."
        ) from e
    except httpx.RequestError as e:
        raise ConnectionError(
            f"Network error connecting to Profinity: {str(e)}. "
            f"Please check your network connection and ensure Profinity is accessible."
        ) from e
    
    # Create a ClientSession from the streams
    print(f"[MCP SSE CONNECTION] Creating ClientSession from streams...")
    mcp_session = ClientSession(read_stream, write_stream)
    print(f"[MCP SSE CONNECTION] ClientSession created")
    
    # Initialize the session (this performs the MCP handshake)
    print(f"[MCP SSE CONNECTION] Initializing MCP session (handshake)...")
    await mcp_session.__aenter__()
    print(f"[MCP SSE CONNECTION] MCP session initialized successfully")
    
    return mcp_session, session_context


async def call_mcp_tool_async(tool_name: str, arguments: Dict) -> Dict:
    """
    Call an MCP tool using the MCP Python SDK.
    This is the async version that must be called from async context.
    
    Creates a new session for each call to avoid thread-safety and timeout issues.
    
    Args:
        tool_name: Name of the MCP tool to call
        arguments: Dictionary of tool arguments
    
    Returns:
        Dictionary with tool result or error information
    """
    start_time = time.time()
    
    # Log the request going to MCP
    print(f"[MCP REQUEST] Tool: {tool_name}")
    print(f"[MCP REQUEST] Arguments: {json.dumps(arguments, indent=2)}")
    print(f"[TIMING] MCP call START: {tool_name} with args: {arguments}")
    
    session = None
    session_context = None
    
    try:
        # Create a new session for this call (this may raise TokenExpiredError or connection errors)
        try:
            session, session_context = await create_mcp_session()
        except (httpx.ConnectError, httpx.ConnectTimeout) as e:
            # Connection error - can't reach the server
            import traceback
            error_trace = traceback.format_exc()
            total_duration = time.time() - start_time
            print(f"[TIMING] MCP call ERROR: {tool_name} - Duration: {total_duration:.3f}s")
            print(f"[MCP ERROR] Tool: {tool_name}")
            print(f"[MCP ERROR] Connection error: {error_trace}")
            return {
                "error": f"Unable to connect to Profinity server at {PROFINITY_MCP_URL}. Please ensure Profinity is running and the MCP server is enabled.",
                "error_type": "ConnectionError",
                "error_code": "CONNECTION_FAILED",
                "suggestion": f"Check that Profinity is running and accessible at {PROFINITY_BASE_URL}. Verify that EnableMcpServer is set to true in the Profinity configuration.",
                "traceback": error_trace
            }
        except httpx.RequestError as e:
            # General network/request error
            import traceback
            error_trace = traceback.format_exc()
            total_duration = time.time() - start_time
            print(f"[TIMING] MCP call ERROR: {tool_name} - Duration: {total_duration:.3f}s")
            print(f"[MCP ERROR] Tool: {tool_name}")
            print(f"[MCP ERROR] Request error: {error_trace}")
            return {
                "error": f"Network error: {str(e)}. Please check your network connection and ensure Profinity is accessible.",
                "error_type": "NetworkError",
                "error_code": "NETWORK_ERROR",
                "suggestion": f"Verify that Profinity is running and accessible at {PROFINITY_BASE_URL}.",
                "traceback": error_trace
            }
        except TokenExpiredError:
            # Token expired - return error that frontend can handle
            total_duration = time.time() - start_time
            print(f"[TIMING] MCP call ERROR: {tool_name} - Duration: {total_duration:.3f}s")
            print(f"[MCP ERROR] Tool: {tool_name}")
            print(f"[MCP ERROR] Token expired")
            return {
                "error": "Authentication token has expired. Please log in again.",
                "error_type": "TokenExpiredError",
                "error_code": 401
            }
        except ValueError as e:
            # Invalid token or other validation error
            total_duration = time.time() - start_time
            print(f"[TIMING] MCP call ERROR: {tool_name} - Duration: {total_duration:.3f}s")
            print(f"[MCP ERROR] Tool: {tool_name}")
            print(f"[MCP ERROR] Validation error: {str(e)}")
            return {
                "error": str(e),
                "error_type": "ValueError",
                "error_code": "VALIDATION_ERROR"
            }
        
        # Log the raw request payload
        raw_request_payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
        print(f"[MCP SSE REQUEST] Raw request payload:")
        print(f"[MCP SSE REQUEST] {json.dumps(raw_request_payload, indent=2)}")
        print(f"[MCP SSE REQUEST] URL: {PROFINITY_MCP_URL}")
        print(f"[MCP SSE REQUEST] Tool: {tool_name}")
        print(f"[MCP SSE REQUEST] Arguments: {json.dumps(arguments, indent=2)}")
        print(f"[MCP SSE REQUEST] Calling tool via MCP SDK...")
        
        # Call the tool using MCP SDK with a per-call timeout
        call_start = time.time()
        
        async def make_call():
            if hasattr(session, 'call_tool'):
                result = await session.call_tool(tool_name, arguments)
                print(f"[MCP SSE REQUEST] Used session.call_tool() method")
                return result
            elif hasattr(session, 'callTool'):
                result = await session.callTool(tool_name, arguments)
                print(f"[MCP SSE REQUEST] Used session.callTool() method")
                return result
            elif hasattr(session, 'call'):
                result = await session.call("tools/call", {"name": tool_name, "arguments": arguments})
                print(f"[MCP SSE REQUEST] Used session.call() method")
                return result
            else:
                # Try to find the right method
                available_methods = [m for m in dir(session) if 'tool' in m.lower() and not m.startswith('_')]
                raise Exception(
                    f"Could not find tool calling method on session. "
                    f"Available methods with 'tool': {available_methods}. "
                    f"Session type: {type(session)}"
                )
        
        result = await asyncio.wait_for(make_call(), timeout=10.0)
        call_duration = time.time() - call_start
        print(f"[TIMING] MCP tool call completed in {call_duration:.3f}s")
        
        # Log detailed response information
        print(f"[MCP SSE RESPONSE] ========== RAW SSE RESPONSE ==========")
        print(f"[MCP SSE RESPONSE] Raw result type: {type(result)}")
        print(f"[MCP SSE RESPONSE] Raw result class: {result.__class__.__name__}")
        print(f"[MCP SSE RESPONSE] Raw result module: {result.__class__.__module__}")
        
        # Extract result from MCP SDK response
        # MCP SDK returns CallToolResult which contains content array with TextContent/ImageContent objects
        if hasattr(result, 'content'):
            # result.content is a list of content items (TextContent, ImageContent, etc.)
            content_items = result.content
            extracted_content = []
            
            for item in content_items:
                if hasattr(item, 'text'):
                    # TextContent object
                    extracted_content.append(item.text)
                elif hasattr(item, 'type') and item.type == 'text':
                    # Dictionary-like object with type and text
                    if hasattr(item, 'text'):
                        extracted_content.append(item.text)
                    elif isinstance(item, dict):
                        extracted_content.append(item.get('text', ''))
                elif isinstance(item, str):
                    # Direct string
                    extracted_content.append(item)
                elif isinstance(item, dict):
                    # Dictionary - try to extract text
                    extracted_content.append(item.get('text', json.dumps(item)))
            
            # Join all content items
            if extracted_content:
                result_text = "\n".join(extracted_content)
                # Try to parse as JSON if it looks like JSON
                try:
                    parsed = json.loads(result_text)
                    print(f"[MCP RESPONSE] Final parsed result: {json.dumps(parsed, indent=2)}")
                    return parsed
                except (json.JSONDecodeError, ValueError):
                    # Not JSON, return as string
                    print(f"[MCP RESPONSE] Final parsed result (string): {result_text[:200]}...")
                    return {"content": result_text}
            else:
                print(f"[MCP RESPONSE] No content extracted from response")
                return {"content": ""}
        else:
            # No content attribute - try to convert to dict or string
            try:
                if hasattr(result, '__dict__'):
                    result_dict = result.__dict__
                    print(f"[MCP RESPONSE] Final parsed result (from __dict__): {json.dumps(result_dict, indent=2, default=str)}")
                    return result_dict
                else:
                    result_str = str(result)
                    print(f"[MCP RESPONSE] Final parsed result (string): {result_str[:200]}...")
                    return {"content": result_str}
            except Exception as e:
                print(f"[MCP RESPONSE] Error extracting result: {e}")
                return {"content": str(result)}
        
    except asyncio.TimeoutError:
        total_duration = time.time() - start_time
        print(f"[TIMING] MCP call TIMEOUT: {tool_name} - Duration: {total_duration:.3f}s")
        return {
            "error": f"Tool call timed out after 10 seconds",
            "error_type": "TimeoutError",
            "error_code": "TIMEOUT"
        }
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        total_duration = time.time() - start_time
        print(f"[TIMING] MCP call ERROR: {tool_name} - Duration: {total_duration:.3f}s")
        print(f"[MCP ERROR] Tool: {tool_name}")
        print(f"[MCP ERROR] Exception: {error_trace}")
        return {
            "error": f"Error calling tool: {str(e)}",
            "error_type": type(e).__name__,
            "traceback": error_trace
        }
    finally:
        # Always clean up the session after use
        if session is not None:
            try:
                await session.__aexit__(None, None, None)
            except Exception as e:
                print(f"[MCP] Error closing session: {e}")
        if session_context is not None:
            try:
                await session_context.__aexit__(None, None, None)
            except Exception as e:
                print(f"[MCP] Error closing session context: {e}")
        
        total_duration = time.time() - start_time
        print(f"[TIMING] MCP call END: {tool_name} - Duration: {total_duration:.3f}s")


def call_mcp_tool(tool_name: str, arguments: Dict) -> Dict:
    """
    Synchronous wrapper for calling MCP tools.
    Uses the persistent event loop for better performance.
    
    Args:
        tool_name: Name of the MCP tool to call
        arguments: Dictionary of tool arguments
    
    Returns:
        Dictionary with tool result or error information
    """
    return run_async_in_loop(call_mcp_tool_async(tool_name, arguments))


async def list_mcp_tools_async() -> List:
    """
    List available MCP tools using the SDK.
    
    Returns:
        List of available MCP tools
    """
    session = None
    session_context = None
    try:
        session, session_context = await create_mcp_session()
        
        # Try different method names
        if hasattr(session, 'list_tools'):
            tools = await session.list_tools()
        elif hasattr(session, 'listTools'):
            tools = await session.listTools()
        elif hasattr(session, 'list'):
            tools = await session.list("tools")
        else:
            tools = []
        
        return tools
    except Exception as e:
        print(f"[MCP] Error listing tools: {e}")
        return []
    finally:
        # Clean up session
        if session is not None:
            try:
                await session.__aexit__(None, None, None)
            except:
                pass
        if session_context is not None:
            try:
                await session_context.__aexit__(None, None, None)
            except:
                pass


def list_mcp_tools() -> List:
    """
    Synchronous wrapper for listing MCP tools.
    
    Returns:
        List of available MCP tools
    """
    result = run_async_in_loop(list_mcp_tools_async())
    if isinstance(result, dict) and "error" in result:
        return []
    return result if isinstance(result, list) else []


async def load_mcp_tools_from_session():
    """
    Load MCP tools and convert them to LangChain tools.
    
    Returns:
        List of LangChain tool objects
    """
    if not MCP_ADAPTERS_AVAILABLE:
        return []
    
    session = None
    session_context = None
    try:
        session, session_context = await create_mcp_session()
        
        # First, list available tools to see what's available
        print(f"[TOOLS] Listing available MCP tools from server...")
        try:
            if hasattr(session, 'list_tools'):
                available_tools_list = await session.list_tools()
            elif hasattr(session, 'listTools'):
                available_tools_list = await session.listTools()
            elif hasattr(session, 'list'):
                available_tools_list = await session.list("tools")
            else:
                available_tools_list = []
            
            if available_tools_list:
                print(f"[TOOLS] ========== MCP SERVER TOOLS DISCOVERY ==========")
                print(f"[TOOLS] Server reports {len(available_tools_list)} available MCP tools:")
                print(f"[TOOLS]")
                for i, tool in enumerate(available_tools_list):
                    tool_name = tool.name if hasattr(tool, 'name') else str(tool)
                    tool_desc = tool.description if hasattr(tool, 'description') else 'No description'
                    
                    # Try to get input schema if available
                    input_schema = None
                    if hasattr(tool, 'inputSchema'):
                        input_schema = tool.inputSchema
                    elif hasattr(tool, 'input_schema'):
                        input_schema = tool.input_schema
                    
                    print(f"[TOOLS] Tool {i+1}: {tool_name}")
                    print(f"[TOOLS]   Description: {tool_desc}")
                    if input_schema:
                        if isinstance(input_schema, dict):
                            properties = input_schema.get('properties', {})
                            if properties:
                                print(f"[TOOLS]   Parameters:")
                                for param_name, param_info in properties.items():
                                    param_type = param_info.get('type', 'unknown')
                                    param_desc = param_info.get('description', 'No description')
                                    print(f"[TOOLS]     - {param_name} ({param_type}): {param_desc[:60]}...")
                        else:
                            print(f"[TOOLS]   Input schema: {input_schema}")
                    print(f"[TOOLS]")
                print(f"[TOOLS] ===============================================")
            else:
                print(f"[TOOLS] ⚠ WARNING: Server returned empty tools list")
                print(f"[TOOLS] This may indicate an authentication or connection issue.")
        except Exception as e:
            print(f"[TOOLS] Could not list tools from server: {e}")
        
        # Now load tools for LangChain
        tools = await load_mcp_tools(session)
        print(f"[TOOLS] Loaded {len(tools)} MCP tools for LangChain")
        if tools:
            print(f"[TOOLS] LangChain-converted tool names:")
            for i, tool in enumerate(tools):
                tool_name = tool.name if hasattr(tool, 'name') else str(tool)
                tool_desc = tool.description if hasattr(tool, 'description') else 'No description'
                print(f"[TOOLS]   {i+1}. {tool_name}")
                print(f"[TOOLS]      Description: {tool_desc[:100]}...")
        else:
            print(f"[TOOLS] ⚠ WARNING: No tools were converted for LangChain")
            print(f"[TOOLS] This may indicate an issue with langchain-mcp-adapters")
        
        print(f"[TOOLS] ========== MCP TOOLS LOADING COMPLETE ==========")
        return tools
    except Exception as e:
        print(f"[TOOLS] Error loading MCP tools: {e}")
        import traceback
        traceback.print_exc()
        return []
    finally:
        # Clean up session
        if session is not None:
            try:
                await session.__aexit__(None, None, None)
            except:
                pass
        if session_context is not None:
            try:
                await session_context.__aexit__(None, None, None)
            except:
                pass


def extract_component_names(components_result: Dict) -> List[str]:
    """
    Extract component names from MCP tool response.
    Handles various response formats from the MCP SDK.
    
    Args:
        components_result: Result from get_all_components MCP tool call
    
    Returns:
        List of component name strings
    """
    components = []
    
    if isinstance(components_result, list):
        # Direct list of component names
        components = components_result
    elif isinstance(components_result, dict):
        if "content" in components_result:
            # Handle MCP SDK response format with content array
            content = components_result.get("content", [])
            if isinstance(content, list) and len(content) > 0:
                for item in content:
                    if isinstance(item, str):
                        try:
                            parsed = json.loads(item)
                            if isinstance(parsed, list):
                                components.extend(parsed)
                        except (json.JSONDecodeError, ValueError):
                            # If it's not JSON, treat as a single component name
                            if item.strip():
                                components.append(item.strip())
                    elif isinstance(item, list):
                        components.extend(item)
                    elif isinstance(item, dict):
                        # If it's a dict, try to extract text or value
                        if "text" in item:
                            try:
                                parsed = json.loads(item["text"])
                                if isinstance(parsed, list):
                                    components.extend(parsed)
                            except (json.JSONDecodeError, ValueError):
                                pass
        elif "text" in components_result:
            # Single text field containing JSON
            try:
                parsed = json.loads(components_result["text"])
                if isinstance(parsed, list):
                    components = parsed
            except (json.JSONDecodeError, ValueError):
                pass
    elif isinstance(components_result, str):
        # String response, try to parse as JSON
        try:
            parsed = json.loads(components_result)
            if isinstance(parsed, list):
                components = parsed
        except (json.JSONDecodeError, ValueError):
            pass
    
    # Filter out empty strings and ensure all are strings
    return [str(c).strip() for c in components if c and str(c).strip()]


def load_components() -> List[str]:
    """
    Load all component names from Profinity.
    This populates the component names list for keyword matching.
    Only loads if a valid token is available.
    
    Returns:
        List of component name strings
    """
    # Check if we have a valid token before attempting to load
    token = get_auth_token()
    if not token:
        print("[COMPONENTS] Skipping component load - no valid token available")
        return []
    
    try:
        load_start = time.time()
        print(f"[TIMING] Component load START")
        print("Loading component names from Profinity...")
        components_result = call_mcp_tool("get_all_components", {})
        load_duration = time.time() - load_start
        
        if "error" not in components_result:
            component_names = extract_component_names(components_result)
            if component_names:
                print(f"Loaded {len(component_names)} components: {', '.join(component_names)}")
            else:
                print("Warning: No components found in response")
                component_names = []
            
            print(f"[TIMING] Component load END - Duration: {load_duration:.3f}s")
            return component_names
        else:
            error_msg = components_result.get("error", "Unknown error")
            print(f"Warning: Could not load components: {error_msg}")
            print(f"[TIMING] Component load ERROR - Duration: {load_duration:.3f}s")
            return []
    except Exception as e:
        load_duration = time.time() - load_start if 'load_start' in locals() else 0
        print(f"[TIMING] Component load ERROR - Duration: {load_duration:.3f}s")
        print(f"Warning: Error loading components: {e}")
        return []
