"""
Conversation history management for Artificial Intelligence Chat.

Manages per-session conversation histories with message trimming
to prevent context window overflow.
"""

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from typing import List, Dict, Optional
import uuid

# Store conversation history per session (using session ID as key)
# Format: {session_id: [HumanMessage, AIMessage, ...]}
_conversation_histories: Dict[str, List] = {}


def get_conversation_history(session_id: str, max_messages: int = 20) -> List:
    """
    Get conversation history for a session.
    Maintains last max_messages (default 20) to prevent context window overflow.
    Returns list of LangChain message objects (HumanMessage, AIMessage, etc.).
    
    Args:
        session_id: Unique session identifier
        max_messages: Maximum number of messages to keep (default 20)
    
    Returns:
        List of LangChain message objects
    """
    global _conversation_histories
    
    if session_id not in _conversation_histories:
        _conversation_histories[session_id] = []
        print(f"[MEMORY] Created new conversation history for session: {session_id}")
    
    # Return last max_messages to prevent context overflow
    history = _conversation_histories[session_id]
    if len(history) > max_messages:
        # Keep the most recent messages (remove oldest)
        history = history[-max_messages:]
        _conversation_histories[session_id] = history
        print(f"[MEMORY] Trimmed conversation history to last {max_messages} messages")
    
    return history


def add_to_history(session_id: str, message) -> None:
    """
    Add a message to the conversation history for a session.
    
    Args:
        session_id: Unique session identifier
        message: LangChain message object (HumanMessage, AIMessage, etc.)
    """
    global _conversation_histories
    
    if session_id not in _conversation_histories:
        _conversation_histories[session_id] = []
    
    _conversation_histories[session_id].append(message)


def clear_history(session_id: str) -> None:
    """
    Clear conversation history for a specific session.
    
    Args:
        session_id: Unique session identifier
    """
    global _conversation_histories
    
    if session_id in _conversation_histories:
        _conversation_histories[session_id] = []
        print(f"[MEMORY] Cleared conversation history for session: {session_id}")
    else:
        print(f"[MEMORY] No conversation history found for session: {session_id}")


def clear_all_histories() -> None:
    """
    Clear all conversation histories.
    Called on login to prevent mixing conversations from different users/sessions.
    """
    global _conversation_histories
    
    count = len(_conversation_histories)
    _conversation_histories.clear()
    print(f"[MEMORY] Cleared all conversation histories ({count} sessions)")


def get_history_count(session_id: str) -> int:
    """
    Get the number of messages in the conversation history for a session.
    
    Args:
        session_id: Unique session identifier
    
    Returns:
        Number of messages in history
    """
    global _conversation_histories
    
    if session_id not in _conversation_histories:
        return 0
    
    return len(_conversation_histories[session_id])
