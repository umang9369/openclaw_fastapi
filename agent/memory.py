"""
agent/memory.py — Conversation memory for the agent.
Stores full message history per session. Designed to be upgradeable 
to vector-based or persistent memory later.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime


class ConversationMemory:
    """In-memory conversation history for a single session."""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.messages: List[Dict[str, Any]] = []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def add(self, role: str, content: str) -> None:
        """Add a message to the history."""
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
        })
        self.updated_at = datetime.now()

    def add_raw(self, message: Dict[str, Any]) -> None:
        """Add a raw message dictionary (e.g., from OpenAI tool calls)."""
        self.messages.append(message)
        self.updated_at = datetime.now()

    def get_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get conversation history, optionally limited to last N messages."""
        if limit is None:
            return self.messages
        return self.messages[-limit:]

    def get_summary(self) -> str:
        """Generate a simple text summary of the conversation."""
        if not self.messages:
            return "No conversation history."

        user_messages = [m["content"] for m in self.messages if m["role"] == "user"]
        if not user_messages:
            return "No user messages."

        last_message = user_messages[-1]
        return f"Last user message: {last_message[:100]}..."

    def clear(self) -> None:
        """Clear conversation history."""
        self.messages = []
        self.updated_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert memory to dictionary for serialization."""
        return {
            "session_id": self.session_id,
            "message_count": len(self.messages),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "messages": self.messages,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConversationMemory":
        """Create memory from dictionary."""
        memory = cls(data["session_id"])
        memory.messages = data.get("messages", [])
        memory.created_at = datetime.fromisoformat(data["created_at"])
        memory.updated_at = datetime.fromisoformat(data["updated_at"])
        return memory


class MemoryManager:
    """Manages multiple conversation memories."""

    def __init__(self):
        self.sessions: Dict[str, ConversationMemory] = {}

    def get_memory(self, session_id: str) -> ConversationMemory:
        """Get or create memory for a session."""
        if session_id not in self.sessions:
            self.sessions[session_id] = ConversationMemory(session_id)
        return self.sessions[session_id]

    def list_sessions(self) -> List[str]:
        """List all active sessions."""
        return list(self.sessions.keys())

    def delete_session(self, session_id: str) -> bool:
        """Delete a session."""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False

    def get_summary(self, session_id: str) -> str:
        """Get summary for a session."""
        memory = self.get_memory(session_id)
        return memory.get_summary()

    def clear_session(self, session_id: str) -> bool:
        """Clear a specific session."""
        if session_id in self.sessions:
            self.sessions[session_id].clear()
            return True
        return False

    def clear_all(self) -> None:
        """Clear all sessions."""
        self.sessions = {}


memory_manager = MemoryManager()