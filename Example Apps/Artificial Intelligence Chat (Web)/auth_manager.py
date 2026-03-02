"""
Authentication management for Artificial Intelligence Chat.

Handles token management, refresh, validation, and login/logout operations.
"""

import os
import httpx
from flask import session, has_request_context
from typing import Optional

# Try to import httpx
try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False
    print("[WARNING] httpx not available. Install with: pip install httpx")


class TokenExpiredError(Exception):
    """Exception raised when token refresh fails due to expiration"""
    pass


# Configuration - will be set by main app
PROFINITY_BASE_URL = None
PROFINITY_API_BASE = None
PROFINITY_AUTH_URL = None
PROFINITY_REFRESH_URL = None
PROFINITY_TOKEN_CMD = None
PROFINITY_TOKEN_ENV = None
USING_CMD_TOKEN = False


def initialize_auth_config(
    base_url: str,
    api_base: str,
    auth_url: str,
    refresh_url: str,
    token_cmd: Optional[str],
    token_env: Optional[str],
    using_cmd_token: bool
):
    """
    Initialize authentication configuration.
    Called by main app during startup.
    
    Args:
        base_url: Profinity base URL
        api_base: Profinity API base URL
        auth_url: Authentication endpoint URL
        refresh_url: Token refresh endpoint URL
        token_cmd: Command line token (if provided)
        token_env: Environment variable token (if provided)
        using_cmd_token: Whether command line token is being used
    """
    global PROFINITY_BASE_URL, PROFINITY_API_BASE, PROFINITY_AUTH_URL, PROFINITY_REFRESH_URL
    global PROFINITY_TOKEN_CMD, PROFINITY_TOKEN_ENV, USING_CMD_TOKEN
    
    PROFINITY_BASE_URL = base_url
    PROFINITY_API_BASE = api_base
    PROFINITY_AUTH_URL = auth_url
    PROFINITY_REFRESH_URL = refresh_url
    PROFINITY_TOKEN_CMD = token_cmd
    PROFINITY_TOKEN_ENV = token_env
    USING_CMD_TOKEN = using_cmd_token


def get_auth_token() -> Optional[str]:
    """
    Get the authentication token for the current session.
    Priority: session token (from login) > command line token > environment token
    
    Can be called outside of request context (e.g., during startup) - in that case,
    only uses command line or environment token.
    
    Returns:
        Authentication token, or None if not available
    """
    # Check session first (user logged in via form) - only if in request context
    has_context = has_request_context()
    if has_context:
        try:
            if 'auth_token' in session:
                token = session.get('auth_token')
                if token:
                    print(f"[AUTH] Token found in Flask session")
                    return token
                else:
                    print(f"[AUTH] Session has 'auth_token' key but value is None/empty")
            else:
                print(f"[AUTH] No 'auth_token' in Flask session")
        except RuntimeError as e:
            # Outside request context - fall through to command line/env token
            print(f"[AUTH] RuntimeError accessing session: {e}")
        except Exception as e:
            print(f"[AUTH] Error accessing session: {e}")
    else:
        print(f"[AUTH] No Flask request context available (outside request)")
    
    # Fall back to command line or environment token
    token = PROFINITY_TOKEN_CMD if PROFINITY_TOKEN_CMD else PROFINITY_TOKEN_ENV
    if token and token != "YOUR_SERVICE_ACCOUNT_TOKEN_HERE":
        print(f"[AUTH] Using token from {'command line' if PROFINITY_TOKEN_CMD else 'environment variable'}")
        return token
    
    print(f"[AUTH] No token available from any source")
    return None


def refresh_auth_token_sync(token: str) -> str:
    """
    Refresh the authentication token synchronously.
    Returns the new token, or raises an exception if refresh fails.
    
    If token refresh returns 401, clears the session and raises TokenExpiredError.
    
    Args:
        token: Current authentication token
    
    Returns:
        New authentication token
    
    Raises:
        TokenExpiredError: If token is invalid or expired
        ValueError: If refresh fails for other reasons
    """
    if not HTTPX_AVAILABLE:
        raise ValueError("httpx is required for token refresh. Install with: pip install httpx")
    
    try:
        response = httpx.get(
            PROFINITY_REFRESH_URL,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            timeout=10.0
        )
        
        if response.status_code == 401:
            # Token is invalid or expired - clear session if using login token (and in request context)
            if has_request_context():
                try:
                    if 'auth_token' in session:
                        session.pop('auth_token', None)
                        session.pop('username', None)
                        print("[AUTH] Token expired - session cleared")
                except RuntimeError:
                    # Outside request context - can't clear session
                    pass
            # Raise a specific exception type for token expiration
            raise TokenExpiredError("Token refresh failed: token is invalid or expired")
        
        if response.status_code != 200:
            raise ValueError(f"Token refresh failed: HTTP {response.status_code}")
        
        result = response.json()
        new_token = result.get('token')
        if not new_token:
            raise ValueError("Token refresh failed: no token in response")
        
        # Update session if using login token (and in request context)
        if has_request_context():
            try:
                if 'auth_token' in session:
                    session['auth_token'] = new_token
                    print("[AUTH] Token refreshed successfully")
            except RuntimeError:
                # Outside request context - can't update session
                pass
        
        return new_token
    except httpx.RequestError as e:
        # Network error - don't clear session, just raise error
        # The main operation can still try with the old token
        raise ValueError(f"Token refresh failed: {str(e)}")


def validate_auth() -> bool:
    """
    Check if authentication is valid (token is available).
    
    Returns:
        True if authenticated, False otherwise
    """
    token = get_auth_token()
    return token is not None


def login(username: str, password: str) -> dict:
    """
    Authenticate user with username and password.
    
    Args:
        username: Username
        password: Password
    
    Returns:
        Dictionary with 'success' (bool) and either 'token'/'username' on success
        or 'error' on failure
    
    Raises:
        ValueError: If httpx is not available or other validation errors
    """
    if not HTTPX_AVAILABLE:
        raise ValueError("httpx is required for authentication. Install with: pip install httpx")
    
    username = username.strip()
    password = password.strip()
    
    if not username or not password:
        raise ValueError("Username and password are required")
    
    # Call Profinity authentication API
    try:
        response = httpx.post(
            PROFINITY_AUTH_URL,
            json={
                'username': username,
                'password': password
            },
            headers={
                'Content-Type': 'application/json'
            },
            timeout=10.0
        )
        
        if response.status_code == 404:
            return {
                'success': False,
                'error': 'Unable to connect to Profinity server. Please ensure the backend service is running.'
            }
        
        if response.status_code != 200:
            try:
                error_data = response.json()
                error_message = error_data.get('message', 'Failed to authenticate')
            except:
                error_message = f'Authentication failed: HTTP {response.status_code}'
            return {
                'success': False,
                'error': error_message
            }
        
        # Parse response (status_code is 200)
        result = response.json()
        token = result.get('token')
        if not token:
            return {
                'success': False,
                'error': 'No token in authentication response'
            }
        
        # Store in session (if in request context)
        if has_request_context():
            try:
                session['auth_token'] = token
                session['username'] = username
            except RuntimeError:
                # Outside request context - can't store in session
                pass
        
        return {
            'success': True,
            'token': token,
            'username': username
        }
    except httpx.RequestError as e:
        return {
            'success': False,
            'error': f'Network error: {str(e)}. Please ensure Profinity is running and accessible.'
        }


def logout() -> dict:
    """
    Log out the current user (clear session token).
    
    Returns:
        Dictionary with 'success' (bool) and 'message'
    """
    username = session.get('username', 'Unknown') if has_request_context() else 'Unknown'
    
    if has_request_context():
        try:
            session.pop('auth_token', None)
            session.pop('username', None)
        except RuntimeError:
            # Outside request context - can't clear session
            pass
    
    print(f"[AUTH] User {username} logged out")
    return {
        'success': True,
        'message': 'Logged out successfully'
    }


def get_auth_status() -> dict:
    """
    Get authentication status.
    
    Returns:
        Dictionary with authentication status information
    """
    token = get_auth_token()
    is_authenticated = token is not None
    can_logout = False
    username = None
    
    if has_request_context():
        try:
            can_logout = 'auth_token' in session
            username = session.get('username') if can_logout else None
        except RuntimeError:
            # Outside request context
            pass
    
    return {
        'is_authenticated': is_authenticated,
        'can_logout': can_logout,
        'username': username,
        'using_cmd_token': USING_CMD_TOKEN
    }
