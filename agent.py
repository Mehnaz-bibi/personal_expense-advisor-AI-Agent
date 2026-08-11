"""
Agent module for Personal Expense Advisor.
Handles LLM integration and tool calling logic.
"""

import os
import json
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
from prompts import get_system_prompt, get_intent_prompt, get_tool_result_prompt
from tools import TOOLS_METADATA, VALID_CATEGORIES
from memory import get_memory_manager

# Load environment variables
load_dotenv()


class ExpenseAgent:
    """Main AI agent for expense tracking and advice."""

    def __init__(self):
        """Initialize the agent with LLM configuration."""
        self.llm_provider = os.getenv("LLM_PROVIDER", "ollama")
        self.model = self._get_model_config()
        self.tools = TOOLS_METADATA
        self.tool_functions = self._get_tool_functions()
        self.llm_client = self._initialize_llm_client()
        self.memory = get_memory_manager()

    def _get_model_config(self) -> str:
        """Get the model configuration based on provider."""
        if self.llm_provider == "ollama":
            return os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
        elif self.llm_provider == "openai":
            return os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        elif self.llm_provider == "anthropic":
            return os.getenv("ANTHROPIC_MODEL", "claude-3-haiku-20240307")
        elif self.llm_provider == "gemini":
            return os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        else:
            return "qwen2.5:7b"  # Default

    def _initialize_llm_client(self):
        """Initialize the LLM client based on provider."""
        if self.llm_provider == "gemini":
            try:
                import google.generativeai as genai
                api_key = os.getenv("GEMINI_API_KEY")
                if not api_key or api_key == "your_gemini_api_key_here":
                    print("Warning: GEMINI_API_KEY not set. Using rule-based mode.")
                    return None
                genai.configure(api_key=api_key)
                return genai.GenerativeModel(self.model)
            except ImportError:
                print("Warning: google-generativeai not installed. Run: pip install google-generativeai")
                return None
            except Exception as e:
                print(f"Warning: Failed to initialize Gemini: {e}")
                return None
        return None

    def _get_tool_functions(self) -> Dict[str, callable]:
        """Map tool names to their actual functions."""
        from tools import (
            add_expense,
            get_expenses,
            get_expenses_today,
            get_expenses_this_month,
            calculate_total,
            check_budget,
            analyze_spending_patterns,
            get_spending_suggestions,
            set_user_budget,
            get_user_budget,
            get_conversation_summary,
            clear_memory,
            reset_everything
        )

        return {
            "add_expense": add_expense,
            "get_expenses": get_expenses,
            "get_expenses_today": get_expenses_today,
            "get_expenses_this_month": get_expenses_this_month,
            "calculate_total": calculate_total,
            "check_budget": check_budget,
            "analyze_spending_patterns": analyze_spending_patterns,
            "get_spending_suggestions": get_spending_suggestions,
            "set_user_budget": set_user_budget,
            "get_user_budget": get_user_budget,
            "get_conversation_summary": get_conversation_summary,
            "clear_memory": clear_memory,
            "reset_everything": reset_everything
        }

    def process_message(self, user_message: str) -> str:
        """
        Process a user message and generate a response.

        Args:
            user_message: The user's input message

        Returns:
            The agent's response
        """
        # Try to use LLM if available
        if self.llm_client:
            try:
                response = self._llm_response(user_message)
            except Exception as e:
                print(f"LLM error: {e}, falling back to rule-based")
                response = self._rule_based_response(user_message)
        else:
            response = self._rule_based_response(user_message)

        # Store conversation in memory
        self.memory.add_conversation(user_message, response)

        return response

    def _llm_response(self, user_message: str) -> str:
        """
        Generate a response using the LLM (Gemini).

        Args:
            user_message: The user's input message

        Returns:
            The agent's response
        """
        if not self.llm_client:
            return self._rule_based_response(user_message)

        try:
            system_prompt = get_system_prompt()
            full_prompt = f"{system_prompt}\n\nUser: {user_message}\n\nAgent:"

            response = self.llm_client.generate_content(full_prompt)
            return response.text.strip()
        except Exception as e:
            print(f"LLM generation error: {e}")
            return self._rule_based_response(user_message)

    def _rule_based_response(self, user_message: str) -> str:
        """
        Generate a response using rule-based logic.
        This is a temporary implementation until LLM integration is complete.

        Args:
            user_message: The user's input message

        Returns:
            The agent's response
        """
        message_lower = user_message.lower()

        # Check if user is adding an expense
        if self._is_adding_expense(message_lower):
            return self._handle_add_expense(user_message)

        # Check if user is asking about spending
        elif self._is_asking_spending(message_lower):
            return self._handle_spending_query(message_lower)

        # Check if user is asking about budget
        elif self._is_asking_budget(message_lower):
            return self._handle_budget_query(message_lower)

        # Check if user is setting budget
        elif self._is_setting_budget(message_lower):
            return self._handle_set_budget(user_message)

        # Check if user is asking for analysis
        elif self._is_asking_analysis(message_lower):
            return self._handle_analysis_query(user_message)

        # Check if user is asking for suggestions
        elif self._is_asking_suggestions(message_lower):
            return self._handle_suggestions_query(message_lower)

        # Check if user wants to clear memory
        elif self._is_clearing_memory(message_lower):
            return self._handle_clear_memory()

        # Default response
        else:
            return self._default_response(user_message)

    def _is_adding_expense(self, message: str) -> bool:
        """Check if the user is trying to add an expense."""
        expense_keywords = ["spent", "spent on", "paid", "cost", "expense", "bought"]
        return any(keyword in message for keyword in expense_keywords)

    def _is_asking_spending(self, message: str) -> bool:
        """Check if the user is asking about spending."""
        spending_keywords = ["how much", "spend", "spent", "total", "expenses", "show me"]
        return any(keyword in message for keyword in spending_keywords)

    def _is_asking_budget(self, message: str) -> bool:
        """Check if the user is asking about budget."""
        budget_keywords = ["budget", "limit", "can i afford", "am i spending too much"]
        return any(keyword in message for keyword in budget_keywords)

    def _is_asking_analysis(self, message: str) -> bool:
        """Check if the user is asking for analysis."""
        analysis_keywords = ["analyze", "pattern", "trend", "breakdown", "where", "highest", "most"]
        return any(keyword in message for keyword in analysis_keywords)

    def _is_asking_suggestions(self, message: str) -> bool:
        """Check if the user is asking for suggestions."""
        suggestion_keywords = ["suggest", "advice", "recommend", "save money", "tip"]
        return any(keyword in message for keyword in suggestion_keywords)

    def _is_setting_budget(self, message: str) -> bool:
        """Check if the user is setting a budget."""
        budget_keywords = ["set my budget", "set budget", "my budget is", "default budget"]
        return any(keyword in message for keyword in budget_keywords)

    def _is_clearing_memory(self, message: str) -> bool:
        """Check if the user wants to clear memory."""
        clear_keywords = ["clear memory", "clear history", "forget everything", "reset memory"]
        return any(keyword in message for keyword in clear_keywords)

    def _handle_add_expense(self, message: str) -> str:
        """Handle adding an expense from natural language."""
        # Simple pattern matching for demo purposes
        # In a real implementation, this would use the LLM for extraction

        # Try to extract amount
        amount = self._extract_amount(message)
        if amount is None:
            return "I couldn't find the amount in your message. Please specify how much you spent."

        # Try to extract category
        category = self._extract_category(message)
        if category is None:
            category = "other"  # Default

        # Use the rest as description
        description = message

        # Remember the category and amount in memory
        self.memory.remember_category(category)
        self.memory.remember_amount(amount)

        # Call the add_expense tool
        result = self.tool_functions["add_expense"](
            amount=amount,
            category=category,
            description=description
        )

        if result["success"]:
            return result["message"]
        else:
            return f"Error: {result['error']}"

    def _handle_spending_query(self, message: str) -> str:
        """Handle queries about spending."""
        message_lower = message.lower()

        # Check for time-based queries
        if "today" in message_lower:
            result = self.tool_functions["get_expenses_today"]()
            if result["success"]:
                if result["count"] == 0:
                    return "You haven't recorded any expenses today."
                return f"You've spent Rs. {result['total']:,.2f} today across {result['count']} expense(s)."
            else:
                return f"Error: {result['error']}"

        elif "this month" in message_lower or "month" in message_lower:
            result = self.tool_functions["get_expenses_this_month"]()
            if result["success"]:
                if result["count"] == 0:
                    return "You haven't recorded any expenses this month."
                return f"You've spent Rs. {result['total']:,.2f} this month across {result['count']} expense(s)."
            else:
                return f"Error: {result['error']}"

        else:
            # Get all expenses
            result = self.tool_functions["get_expenses"]()
            if result["success"]:
                if result["count"] == 0:
                    return "You haven't recorded any expenses yet."
                return f"You've spent Rs. {result['total']:,.2f} in total across {result['count']} expense(s)."
            else:
                return f"Error: {result['error']}"

    def _handle_budget_query(self, message: str) -> str:
        """Handle budget-related queries."""
        # Try to extract budget amount
        budget = self._extract_amount(message)
        if budget is None:
            return "Please specify your budget amount. For example: 'My budget is 40000'"

        result = self.tool_functions["check_budget"](budget)
        if result["success"]:
            return result["message"]
        else:
            return f"Error: {result['error']}"

    def _handle_analysis_query(self, message: str) -> str:
        """Handle analysis queries."""
        result = self.tool_functions["analyze_spending_patterns"]()
        if result["success"]:
            if result["this_month_count"] == 0:
                return "You don't have enough expense data for analysis yet. Start by adding some expenses!"

            response = f"Here's your spending analysis for this month:\n\n"
            response += f"Total spending: Rs. {result['this_month_total']:,.2f}\n"
            response += f"Number of expenses: {result['this_month_count']}\n"
            response += f"Average daily spending: Rs. {result['average_daily_spending']:,.2f}\n\n"

            if result["highest_category"]["name"]:
                highest = result["highest_category"]
                response += f"Highest spending category: {highest['name']} "
                response += f"(Rs. {highest['amount']:,.2f}, {highest['percentage']:.1f}% of total)\n"

            return response
        else:
            return f"Error: {result['error']}"

    def _handle_suggestions_query(self, message: str) -> str:
        """Handle suggestion queries."""
        # Try to extract budget if mentioned
        budget = self._extract_amount(message)

        result = self.tool_functions["get_spending_suggestions"](budget)
        if result["success"]:
            if not result["suggestions"]:
                return "I don't have enough data to provide suggestions yet. Keep tracking your expenses!"

            response = "Here are some suggestions based on your spending:\n\n"
            for i, suggestion in enumerate(result["suggestions"], 1):
                response += f"{i}. {suggestion}\n"
            return response
        else:
            return f"Error: {result['error']}"

    def _handle_set_budget(self, user_message: str) -> str:
        """Handle setting a default budget."""
        amount = self._extract_amount(user_message)
        if amount is None:
            return "Please specify the budget amount. For example: 'Set my budget to 40000'"

        result = self.tool_functions["set_user_budget"](amount)
        if result["success"]:
            return result["message"]
        else:
            return f"Error: {result['error']}"

    def _handle_clear_memory(self) -> str:
        """Handle clearing memory."""
        result = self.tool_functions["reset_everything"]()
        if result["success"]:
            return result["message"]
        else:
            return f"Error: {result['error']}"

    def _default_response(self, user_message: str) -> str:
        """Handle general messages."""
        # Check if user wants to know their current budget
        if "my budget" in user_message.lower() and "what" in user_message.lower():
            result = self.tool_functions["get_user_budget"]()
            if result["success"]:
                return result["message"]

        return """I'm your Personal Expense Advisor. I can help you:

• Add expenses (e.g., "I spent 500 on lunch")
• Check your spending (e.g., "How much did I spend this month?")
• Budget tracking (e.g., "My budget is 40000")
• Set default budget (e.g., "Set my budget to 40000")
• Analyze patterns (e.g., "Where am I spending the most?")
• Get suggestions (e.g., "Give me some money-saving tips")
• Reset everything (e.g., "Clear my conversation history and all expenses")

What would you like to do?"""

    def _extract_amount(self, message: str) -> Optional[float]:
        """Extract amount from a message."""
        import re
        # Look for numbers in the message
        numbers = re.findall(r'\d+\.?\d*', message)
        if numbers:
            try:
                return float(numbers[0])
            except ValueError:
                pass
        return None

    def _extract_category(self, message: str) -> Optional[str]:
        """Extract category from a message."""
        message_lower = message.lower()

        # Check for category keywords
        category_keywords = {
            "food": ["food", "lunch", "dinner", "breakfast", "snack", "restaurant", "meal"],
            "groceries": ["grocer", "supermarket", "vegetable", "fruit", "food items"],
            "transport": ["transport", "uber", "taxi", "bus", "petrol", "gas", "fuel", "travel"],
            "shopping": ["shop", "clothes", "shoes", "electronics", "buy"],
            "bills": ["bill", "electricity", "water", "internet", "phone", "rent"],
            "entertainment": ["movie", "game", "concert", "entertainment", "fun"],
            "health": ["health", "doctor", "medicine", "pharmacy", "hospital"],
            "education": ["education", "book", "course", "tuition", "class"],
            "other": []
        }

        for category, keywords in category_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                return category

        return "other"  # Default


# Singleton instance
_agent_instance: Optional[ExpenseAgent] = None


def get_agent() -> ExpenseAgent:
    """Get or create the agent singleton instance."""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = ExpenseAgent()
    return _agent_instance
