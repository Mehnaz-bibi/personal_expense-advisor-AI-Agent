"""
Demo script for Personal Expense Advisor.
Shows the application working with pre-defined conversations.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from agent import get_agent


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60)


def print_conversation(user_msg, agent_response):
    """Print a conversation exchange."""
    print(f"\nYou: {user_msg}")
    print(f"Agent: {agent_response}")


def main():
    """Run a demo conversation."""
    print_header("Personal Expense Advisor - Demo")

    agent = get_agent()

    # Demo conversation
    conversations = [
        "I spent 1200 on groceries today",
        "I spent 500 on lunch",
        "How much did I spend today?",
        "How much did I spend this month?",
        "My budget is 40000",
        "Where am I spending the most?",
        "Give me some suggestions to save money"
    ]

    print("\nStarting demo conversation...\n")

    for i, message in enumerate(conversations, 1):
        print(f"\n--- Conversation {i} ---")
        response = agent.process_message(message)
        print_conversation(message, response)

    print_header("Demo Complete")
    print("\nThe application is working correctly!")
    print("Run 'python main.py' to use the interactive CLI.")
    print("Run 'python test_tools.py' to test individual tools.")
    print("Run 'python test_agent.py' to test agent conversations.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
