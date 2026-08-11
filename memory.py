"""
Memory module for Personal Expense Advisor.
Handles user preferences, context, and conversation history.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class MemoryManager:
    """Manages user memory and preferences."""

    def __init__(self, memory_file: str = "data/memory.json"):
        """
        Initialize memory manager.

        Args:
            memory_file: Path to memory storage file
        """
        self.memory_file = memory_file
        self.memory = self._load_memory()

    def _load_memory(self) -> Dict:
        """Load memory from file."""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return self._get_default_memory()
        return self._get_default_memory()

    def _get_default_memory(self) -> Dict:
        """Get default memory structure."""
        return {
            "user_id": "default",
            "preferences": {
                "default_budget": None,
                "preferred_currency": "Rs.",
                "date_format": "%Y-%m-%d",
                "language": "en"
            },
            "context": {
                "last_category": None,
                "recent_amounts": [],
                "common_categories": {},
                "conversation_count": 0
            },
            "history": [],
            "user_profile": {
                "name": None,
                "location": None,
                "timezone": None
            }
        }

    def _save_memory(self):
        """Save memory to file."""
        try:
            os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.memory, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save memory: {e}")

    def set_preference(self, key: str, value):
        """
        Set a user preference.

        Args:
            key: Preference key
            value: Preference value
        """
        self.memory["preferences"][key] = value
        self._save_memory()

    def get_preference(self, key: str, default=None):
        """
        Get a user preference.

        Args:
            key: Preference key
            default: Default value if not found

        Returns:
            Preference value or default
        """
        return self.memory["preferences"].get(key, default)

    def set_default_budget(self, budget: float):
        """Set the default budget."""
        self.set_preference("default_budget", budget)

    def get_default_budget(self) -> Optional[float]:
        """Get the default budget."""
        return self.get_preference("default_budget")

    def remember_category(self, category: str):
        """Remember a category usage."""
        self.memory["context"]["last_category"] = category
        self.memory["context"]["common_categories"][category] = \
            self.memory["context"]["common_categories"].get(category, 0) + 1
        self._save_memory()

    def remember_amount(self, amount: float):
        """Remember a recent amount."""
        self.memory["context"]["recent_amounts"].append(amount)
        # Keep only last 10 amounts
        if len(self.memory["context"]["recent_amounts"]) > 10:
            self.memory["context"]["recent_amounts"].pop(0)
        self._save_memory()

    def get_recent_amounts(self) -> List[float]:
        """Get recent amounts."""
        return self.memory["context"]["recent_amounts"]

    def get_common_categories(self) -> Dict[str, int]:
        """Get common categories with usage count."""
        return self.memory["context"]["common_categories"]

    def add_conversation(self, user_message: str, agent_response: str):
        """
        Add a conversation to history.

        Args:
            user_message: User's message
            agent_response: Agent's response
        """
        conversation = {
            "timestamp": datetime.now().isoformat(),
            "user": user_message,
            "agent": agent_response
        }
        self.memory["history"].append(conversation)
        self.memory["context"]["conversation_count"] += 1

        # Keep only last 50 conversations
        if len(self.memory["history"]) > 50:
            self.memory["history"].pop(0)

        self._save_memory()

    def get_conversation_history(self, limit: int = 10) -> List[Dict]:
        """
        Get recent conversation history.

        Args:
            limit: Number of recent conversations to return

        Returns:
            List of recent conversations
        """
        return self.memory["history"][-limit:]

    def set_user_profile(self, name: str = None, location: str = None, timezone: str = None):
        """
        Set user profile information.

        Args:
            name: User's name
            location: User's location
            timezone: User's timezone
        """
        if name:
            self.memory["user_profile"]["name"] = name
        if location:
            self.memory["user_profile"]["location"] = location
        if timezone:
            self.memory["user_profile"]["timezone"] = timezone
        self._save_memory()

    def get_user_profile(self) -> Dict:
        """Get user profile information."""
        return self.memory["user_profile"]

    def get_spending_patterns(self) -> Dict:
        """Analyze spending patterns from memory."""
        common_categories = self.get_common_categories()
        recent_amounts = self.get_recent_amounts()

        if recent_amounts:
            avg_amount = sum(recent_amounts) / len(recent_amounts)
            max_amount = max(recent_amounts)
            min_amount = min(recent_amounts)
        else:
            avg_amount = 0
            max_amount = 0
            min_amount = 0

        return {
            "most_common_category": max(common_categories.items(), key=lambda x: x[1])[0] if common_categories else None,
            "average_amount": avg_amount,
            "max_recent_amount": max_amount,
            "min_recent_amount": min_amount,
            "total_conversations": self.memory["context"]["conversation_count"]
        }

    def clear_history(self):
        """Clear conversation history."""
        self.memory["history"] = []
        self.memory["context"]["conversation_count"] = 0
        self._save_memory()

    def reset_memory(self):
        """Reset memory to defaults."""
        self.memory = self._get_default_memory()
        self._save_memory()


# Singleton instance
_memory_instance: Optional[MemoryManager] = None


def get_memory_manager() -> MemoryManager:
    """Get or create the memory manager singleton instance."""
    global _memory_instance
    if _memory_instance is None:
        _memory_instance = MemoryManager()
    return _memory_instance
