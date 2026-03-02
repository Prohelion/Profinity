#!/usr/bin/env python3
"""
Artificial Intelligence Chat — web UI for Ollama with Profinity MCP

This web UI provides a simple interface to interact with Profinity data through
Ollama AI models using MCP (Model Context Protocol) tools.

Rewritten with modular structure for maintainability.
"""
import warnings

# Suppress Pydantic V1 deprecation warning for Python 3.14+
warnings.filterwarnings(
    "ignore",
    message=".*Core Pydantic V1 functionality isn't compatible with Python 3.14.*",
    category=UserWarning
)

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
import json
import os
import subprocess
import sys
import time
import argparse
import uuid
import markdown

# Import modules
from auth_manager import (
    initialize_auth_config, get_auth_token, login as auth_login,
    logout as auth_logout, get_auth_status, TokenExpiredError
)
from conversation_manager import (
    get_conversation_history, add_to_history, clear_history, clear_all_histories
)
from mcp_client import (
    initialize_mcp_config, call_mcp_tool, list_mcp_tools,
    load_components, shutdown_event_loop, get_or_create_event_loop
)
from model_manager import (
    initialize_model_config, get_model, check_needs_mcp,
    update_keywords_from_components, clear_model_cache, get_tool_registry
)

# MCP Python SDK check
try:
    from mcp.client.sse import sse_client
    MCP_SDK_AVAILABLE = True
except ImportError as e:
    MCP_SDK_AVAILABLE = False
    raise ImportError(
        "MCP Python SDK is required. Install with:\n"
        "pip install git+https://github.com/modelcontextprotocol/python-sdk.git\n"
        f"Original error: {e}"
    )

# Flask app setup
app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = os.getenv('FLASK_SECRET_KEY', os.urandom(24).hex())
CORS(app, supports_credentials=True)

# Parse command line arguments
parser = argparse.ArgumentParser(description='Artificial Intelligence Chat', add_help=False)
parser.add_argument('--token', type=str, help='Profinity service account token (optional)')
args, _ = parser.parse_known_args()

# Load configuration
PROFINITY_TOKEN_CMD = args.token if args.token else None
PROFINITY_TOKEN_ENV = os.getenv("PROFINITY_TOKEN", "YOUR_SERVICE_ACCOUNT_TOKEN_HERE")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:14b")
PROFINITY_MCP_URL = os.getenv("PROFINITY_MCP_URL", "http://localhost:18080/sse")

# Extract base URL from MCP URL
PROFINITY_BASE_URL = PROFINITY_MCP_URL.rsplit('/sse', 1)[0] if '/sse' in PROFINITY_MCP_URL else PROFINITY_MCP_URL.rsplit('/', 1)[0]
PROFINITY_API_BASE = f"{PROFINITY_BASE_URL}/api/v2"
PROFINITY_AUTH_URL = f"{PROFINITY_API_BASE}/Users/Authenticate"
PROFINITY_REFRESH_URL = f"{PROFINITY_API_BASE}/Users/Refresh"

USING_CMD_TOKEN = PROFINITY_TOKEN_CMD is not None

# Initialize module configurations
initialize_auth_config(
    base_url=PROFINITY_BASE_URL,
    api_base=PROFINITY_API_BASE,
    auth_url=PROFINITY_AUTH_URL,
    refresh_url=PROFINITY_REFRESH_URL,
    token_cmd=PROFINITY_TOKEN_CMD,
    token_env=PROFINITY_TOKEN_ENV,
    using_cmd_token=USING_CMD_TOKEN
)
initialize_mcp_config(mcp_url=PROFINITY_MCP_URL, base_url=PROFINITY_BASE_URL)
initialize_model_config(default_model=OLLAMA_MODEL)


# Routes
@app.route('/')
def index():
    """Serve the main web UI"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return render_template('index.html')


@app.route('/api/clear-history', methods=['POST'])
def clear_history_endpoint():
    """Clear conversation history for current session"""
    if 'session_id' in session:
        session_id = session['session_id']
        clear_history(session_id)
    return jsonify({'success': True, 'message': 'Conversation history cleared'})


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Authenticate user with username and password"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400
        
        # Authenticate
        result = auth_login(username, password)
        
        if not result.get('success'):
            return jsonify({'error': result.get('error', 'Authentication failed')}), 401
        
        # Login flow: authenticate → load components → update keywords → clear conversations → clear model cache
        print("[AUTH] Login successful - executing login flow...")
        
        # 1. Load components
        print("[AUTH] Step 1: Loading components...")
        components = load_components()
        
        # 2. Update keywords with component names
        print("[AUTH] Step 2: Updating keywords with component names...")
        update_keywords_from_components(components)
        
        # 3. Clear all conversation histories
        print("[AUTH] Step 3: Clearing all conversation histories...")
        clear_all_histories()
        
        # 4. Clear model cache
        print("[AUTH] Step 4: Clearing model cache...")
        clear_model_cache()
        
        print("[AUTH] Login flow completed successfully")
        
        return jsonify({
            'success': True,
            'message': 'Authentication successful',
            'username': result.get('username')
        })
    except Exception as e:
        import traceback
        return jsonify({
            'error': f'Login error: {str(e)}',
            'traceback': traceback.format_exc() if app.debug else None
        }), 500


@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """Log out the current user (clear session token)"""
    # Clear model cache on logout
    clear_model_cache()
    
    result = auth_logout()
    return jsonify(result)


@app.route('/api/auth/status', methods=['GET'])
def auth_status():
    """Get authentication status"""
    return jsonify(get_auth_status())


@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages and process with Ollama + MCP tools"""
    request_start_time = time.time()
    print(f"[TIMING] Request START: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(request_start_time))}")
    
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        query = data.get('message', '')
        model_name = data.get('model', OLLAMA_MODEL)
        clear_history_flag = data.get('clear_history', False)
        
        if not query:
            return jsonify({'error': 'Message is required'}), 400
        
        # Get or create session ID
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())
        session_id = session['session_id']
        
        # Get conversation history
        conversation_history = get_conversation_history(session_id)
        
        # Clear history if requested
        if clear_history_flag:
            clear_history(session_id)
            conversation_history = []
        
        # Check if query needs MCP tools
        needs_mcp, matched_keywords = check_needs_mcp(query)
        
        print(f"[CHAT] Query: {query}")
        print(f"[CHAT] Needs MCP: {needs_mcp}, Matched keywords: {matched_keywords}")
        
        # Get the model (bind tools if needed)
        try:
            llm = get_model(model_name, bind_tools=needs_mcp)
            tool_registry = get_tool_registry()
        except Exception as e:
            import traceback
            print(f"[ERROR] Failed to initialize Ollama model: {e}")
            print(f"[ERROR] Traceback: {traceback.format_exc()}")
            return jsonify({'error': f'Failed to initialize Ollama model: {str(e)}'}), 500
        
        # Build system message if MCP query
        if needs_mcp:
            # Get component list for context
            components_context = ""
            mcp_context_start = time.time()
            try:
                print(f"[TIMING] Fetching component list for context...")
                components_result = call_mcp_tool("get_all_components", {})
                mcp_context_duration = time.time() - mcp_context_start
                print(f"[TIMING] Component list fetch completed in {mcp_context_duration:.3f}s")
                
                if "error" not in components_result:
                    if isinstance(components_result, list):
                        components_context = f"Available components: {', '.join(components_result)}"
                    elif isinstance(components_result, dict) and "content" in components_result:
                        content = components_result.get("content", [])
                        if isinstance(content, list) and len(content) > 0:
                            components = []
                            for item in content:
                                if isinstance(item, str):
                                    try:
                                        parsed = json.loads(item)
                                        if isinstance(parsed, list):
                                            components.extend(parsed)
                                    except:
                                        if item.strip():
                                            components.append(item.strip())
                                elif isinstance(item, list):
                                    components.extend(item)
                            if components:
                                components_context = f"Available components: {', '.join(components)}"
            except Exception as e:
                components_context = f"Could not retrieve component list: {str(e)}"
            
            system_message_content = f"""You are an AI assistant helping users query Profinity data.

Profinity Data Model:
Profinity organizes data in a hierarchical structure:
- Component: A device or system (e.g., "Prohelion 12v", "Prohelion BMU", "Prohelion WaveSculptor 22 - Left")
  - Message: A CAN bus message containing multiple signals (e.g., "Voltages", "Temperatures")
    - Signal: A specific data point within a message (e.g., "Cell 1 mV", "Cell Temp")

Component Name Matching:
The backend MCP tools support fuzzy matching for component, message, and signal names. You can use partial or shortened names directly.

{components_context}

CRITICAL: YOU MUST ACTUALLY CALL TOOLS - DO NOT DESCRIBE WHAT YOU WOULD DO

Your Capabilities:
- You have access to MCP tools that can query the Profinity system
- **YOU MUST ACTUALLY CALL THESE TOOLS** - do not describe what you would do, actually execute the tool calls
- When the user asks for data, you MUST call the appropriate tool immediately

Available MCP Tools:
1. get_all_components: Returns a list of component names
2. get_all_metadata: Returns full metadata (units, ranges, data types, etc.)
3. get_component_data: Returns current signal values for a component
4. get_all_components_data: Returns current signal values for all components
5. get_signal_value: Returns current or historical time-series data for a specific signal

Available Search Tools:
1. prohelion_docs_search: Search the Prohelion documentation site
2. web_search: Search the general web for current information

Instructions:
- **DO NOT DESCRIBE TOOL CALLS - ACTUALLY EXECUTE THEM**
- When the user asks a question, immediately call the appropriate tool
- For Profinity data queries: **CALL** the MCP tools immediately
- For Prohelion questions: **CALL** prohelion_docs_search
- For general questions: **CALL** web_search
- Remember the filter hierarchy: Component → Message → Signal
- You can use fuzzy/partial names - the backend will resolve them automatically
- **NEVER say "I'll use tool X" or "Here's what I would do" - just call the tool directly**

Answer the user's question accurately and honestly. **ACTUALLY CALL** the tools for queries. Do not describe what you would do - execute the tool calls immediately.
"""
        else:
            system_message_content = """You are a helpful AI assistant.

CRITICAL ACCURACY REQUIREMENTS:
- NEVER make up information, data, or facts. All statements must be backed by actual data or verified sources.
- If you don't know something or cannot find the information, it is PERFECTLY ACCEPTABLE to say "I don't know" or "I couldn't find that information."
- The user values accuracy over completeness - they prefer honest "I don't know" responses over potentially incorrect information.
"""
        
        # Build messages list
        messages = []
        
        # Add system message
        if needs_mcp:
            messages.append(SystemMessage(content=system_message_content))
        
        # Add conversation history
        messages.extend(conversation_history)
        
        # Add current user message
        user_message = HumanMessage(content=query)
        messages.append(user_message)
        
        # Get response from Ollama
        ollama_start = time.time()
        print(f"[TIMING] Ollama processing START (with {len(conversation_history)} previous messages)")
        
        try:
            print(f"[OLLAMA] Invoking model...")
            response = llm.invoke(messages)
            print(f"[OLLAMA] Invoke completed successfully")
            
            # Handle tool calls if the model requested them
            tool_calls_made = []
            if hasattr(response, 'tool_calls') and response.tool_calls:
                print(f"[TOOLS] ✓ Model requested {len(response.tool_calls)} tool calls - executing them now")
                for tool_call in response.tool_calls:
                    # Handle both dict and object formats for tool_call
                    if isinstance(tool_call, dict):
                        tool_name = tool_call.get('name', '') or tool_call.get('function', {}).get('name', '')
                        tool_args = tool_call.get('args', {}) or tool_call.get('function', {}).get('arguments', {})
                        tool_call_id = tool_call.get('id', '')
                    else:
                        # ToolCall object from LangChain
                        tool_name = getattr(tool_call, 'name', '') or getattr(tool_call, 'function', {}).get('name', '') if hasattr(tool_call, 'function') else ''
                        tool_args = getattr(tool_call, 'args', {}) or (getattr(tool_call, 'function', {}).get('arguments', {}) if hasattr(tool_call, 'function') else {})
                        tool_call_id = getattr(tool_call, 'id', '')
                    
                    # Parse tool_args if it's a string
                    if isinstance(tool_args, str):
                        try:
                            tool_args = json.loads(tool_args)
                        except:
                            tool_args = {}
                    
                    print(f"[TOOLS] Tool call structure: {type(tool_call)}")
                    print(f"[TOOLS] Executing tool: {tool_name} with args: {tool_args}, id: {tool_call_id}")
                    
                    # Check if this is a LangChain tool or MCP tool
                    tool_obj = tool_registry.get(tool_name)
                    if tool_obj is not None:
                        # LangChain tool (search tools)
                        print(f"[TOOLS] Executing LangChain tool: {tool_name}")
                        try:
                            tool_result = tool_obj.invoke(tool_args)
                            if isinstance(tool_result, str):
                                tool_result = {"result": tool_result}
                            else:
                                tool_result = {"result": str(tool_result)}
                        except Exception as e:
                            print(f"[TOOLS] Error executing LangChain tool {tool_name}: {e}")
                            import traceback
                            traceback.print_exc()
                            tool_result = {"error": f"Error executing {tool_name}: {str(e)}"}
                    elif tool_name in tool_registry:
                        # MCP tool
                        print(f"[TOOLS] Executing MCP tool: {tool_name}")
                        tool_result = call_mcp_tool(tool_name, tool_args)
                    else:
                        # Unknown tool - try MCP
                        print(f"[TOOLS] Unknown tool {tool_name}, trying MCP...")
                        try:
                            tool_result = call_mcp_tool(tool_name, tool_args)
                        except Exception as e:
                            print(f"[TOOLS] Tool {tool_name} not found")
                            tool_result = {"error": f"Unknown tool: {tool_name}"}
                    
                    # Create ToolMessage with the result
                    if isinstance(tool_result, str):
                        tool_message_content = tool_result
                    else:
                        tool_message_content = json.dumps(tool_result, default=str)
                    
                    tool_message = ToolMessage(
                        content=tool_message_content,
                        tool_call_id=tool_call_id
                    )
                    print(f"[TOOLS] Created ToolMessage with content length: {len(tool_message_content)}, tool_call_id: {tool_call_id}")
                    messages.append(tool_message)
                    tool_calls_made.append(tool_name)
                
                # Get final response after ALL tool calls are executed
                # Add a follow-up message to prompt the model to respond based on tool results
                print(f"[OLLAMA] Invoking model again after {len(tool_calls_made)} tool call(s)...")
                print(f"[OLLAMA] Message history has {len(messages)} messages (including tool results)")
                print(f"[OLLAMA] Last few messages:")
                for i, msg in enumerate(messages[-3:], start=len(messages)-2):
                    msg_type = type(msg).__name__
                    content_preview = str(msg.content)[:100] if hasattr(msg, 'content') and msg.content else "No content"
                    print(f"[OLLAMA]   Message {i}: {msg_type} - {content_preview}...")
                
                response = llm.invoke(messages)
                print(f"[OLLAMA] Second invoke completed successfully")
                print(f"[OLLAMA] Response type: {type(response)}")
                if hasattr(response, 'content'):
                    print(f"[OLLAMA] Response content type: {type(response.content)}, length: {len(str(response.content)) if response.content else 0}")
                if hasattr(response, 'tool_calls') and response.tool_calls:
                    print(f"[WARNING] Model is requesting {len(response.tool_calls)} more tool calls after first round!")
                    print(f"[WARNING] This might indicate the model needs more information or there's a configuration issue")
            
            # Extract response text
            response_text = None
            if hasattr(response, 'content') and response.content:
                response_text = str(response.content)
            elif hasattr(response, 'text'):
                response_text = str(response.text)
            else:
                response_text = str(response)
            
            # Check if response is empty or only whitespace
            if not response_text or not response_text.strip():
                print(f"[WARNING] Empty response from Ollama!")
                print(f"[WARNING] Response object: {response}")
                print(f"[WARNING] Response has tool_calls: {hasattr(response, 'tool_calls') and bool(response.tool_calls)}")
                if hasattr(response, 'tool_calls') and response.tool_calls:
                    print(f"[WARNING] Model returned {len(response.tool_calls)} tool calls instead of text response")
                    print(f"[WARNING] Tool calls: {response.tool_calls}")
                    # Try to extract any content that might be there
                    if hasattr(response, 'content') and response.content:
                        print(f"[WARNING] Response.content exists but is empty/whitespace: {repr(response.content)}")
                response_text = "I apologize, but I didn't receive a valid response. Please try asking your question again."
            
            ollama_duration = time.time() - ollama_start
            print(f"[TIMING] Ollama processing END - Duration: {ollama_duration:.3f}s (tools called: {tool_calls_made})")
            
            # Save conversation to history
            add_to_history(session_id, user_message)
            add_to_history(session_id, AIMessage(content=response_text))
            
            # Convert markdown to HTML
            markdown_start = time.time()
            try:
                html_content = markdown.markdown(
                    response_text,
                    extensions=['extra', 'codehilite', 'nl2br']
                )
            except Exception:
                html_content = markdown.markdown(
                    response_text,
                    extensions=['extra', 'nl2br']
                )
            markdown_duration = time.time() - markdown_start
            print(f"[TIMING] Markdown conversion completed in {markdown_duration:.3f}s")
            
        except Exception as e:
            ollama_duration = time.time() - ollama_start
            print(f"[TIMING] Ollama processing ERROR - Duration: {ollama_duration:.3f}s")
            print(f"[ERROR] Exception type: {type(e).__name__}")
            print(f"[ERROR] Exception message: {str(e)}")
            import traceback
            error_trace = traceback.format_exc()
            print(f"[ERROR] Full traceback:\n{error_trace}")
            return jsonify({'error': f'Failed to get response from Ollama: {str(e)}'}), 500
        
        total_duration = time.time() - request_start_time
        print(f"[TIMING] Request END - Total duration: {total_duration:.3f}s")
        
        # Get updated history count
        updated_history = get_conversation_history(session_id)
        history_count = len(updated_history)
        
        return jsonify({
            'response': html_content,
            'response_text': response_text,
            'used_mcp': needs_mcp,
            'history_length': history_count
        })
    except Exception as e:
        import traceback
        total_duration = time.time() - request_start_time
        print(f"[TIMING] Request ERROR - Duration: {total_duration:.3f}s")
        error_msg = str(e)
        if app.debug:
            error_msg += f"\n{traceback.format_exc()}"
        return jsonify({'error': error_msg}), 500


@app.route('/api/models', methods=['GET'])
def get_models():
    """Return available Ollama models"""
    try:
        result = subprocess.run(
            ['ollama', 'list'],
            capture_output=True,
            text=True,
            timeout=5
        )
        models = []
        for line in result.stdout.split('\n')[1:]:  # Skip header
            if line.strip():
                parts = line.split()
                if parts:
                    model_name = parts[0]
                    models.append({'name': model_name})
        return jsonify({'models': models})
    except Exception as e:
        # Return default model if ollama command fails
        return jsonify({
            'models': [
                {'name': OLLAMA_MODEL}
            ]
        })


@app.route('/api/mcp/tools', methods=['GET'])
def get_mcp_tools():
    """List available MCP tools using MCP SDK"""
    try:
        tools = list_mcp_tools()
        # Convert tools to JSON-serializable format
        tools_list = []
        for tool in tools:
            if hasattr(tool, 'name'):
                tools_list.append({
                    'name': tool.name,
                    'description': getattr(tool, 'description', ''),
                    'inputSchema': getattr(tool, 'inputSchema', {})
                })
        return jsonify({'tools': tools_list})
    except Exception as e:
        import traceback
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc() if app.debug else None,
            'tools': []
        }), 500


@app.route('/api/mcp/status', methods=['GET'])
def get_mcp_status():
    """Get MCP connection status and diagnostics"""
    status = {
        'sdk_available': MCP_SDK_AVAILABLE,
        'url': PROFINITY_MCP_URL,
        'token_configured': get_auth_token() is not None,
    }
    
    # Try to test connection
    try:
        tools = list_mcp_tools()
        status['connection_test'] = 'success'
        status['tools_count'] = len(tools)
    except Exception as e:
        status['connection_test'] = 'failed'
        status['connection_error'] = str(e)
        import traceback
        if app.debug:
            status['connection_traceback'] = traceback.format_exc()
    
    return jsonify(status)


if __name__ == '__main__':
    if not MCP_SDK_AVAILABLE:
        print("ERROR: MCP Python SDK is required!")
        print("Install with: pip install git+https://github.com/modelcontextprotocol/python-sdk.git")
        exit(1)
    
    # Check if running in virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    if not in_venv:
        print("WARNING: Not running in a virtual environment!")
        print("Packages may not be available. Please:")
        print("  1. Use ./run.sh to run the application (recommended), or")
        print("  2. Activate the virtual environment first: source venv/bin/activate")
        print("")
    
    print(f"Starting Artificial Intelligence Chat...")
    print(f"MCP SDK: Available")
    print(f"Ollama Model: {OLLAMA_MODEL}")
    print(f"Profinity MCP URL: {PROFINITY_MCP_URL}")
    print(f"Token configured: {'Yes' if get_auth_token() else 'No (set PROFINITY_TOKEN env var or use login form)'}")
    
    # Initialize persistent event loop
    try:
        get_or_create_event_loop()
        print("Event loop initialized")
    except Exception as e:
        print(f"Warning: Failed to initialize event loop: {e}")
    
    # Load component names on startup (only if token is available)
    token = get_auth_token()
    if token:
        print("[STARTUP] Token available - loading components...")
        components = load_components()
        update_keywords_from_components(components)
    else:
        print("[STARTUP] No token available - components will be loaded after login")
    
    try:
        print(f"Open http://localhost:8090 in your browser")
        app.run(debug=True, port=8090, host='0.0.0.0')
    finally:
        # Cleanup on shutdown
        print("Shutting down...")
        shutdown_event_loop()
        print("Shutdown complete")
