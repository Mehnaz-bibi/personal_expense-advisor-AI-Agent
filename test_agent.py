"""
Test script for the agent functionality.
Tests the end-to-end workflow with sample conversations.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from agent import get_agent


def test_conversation():
    """Test a conversation with the agent."""
    print("=" * 60)
    print("Testing Agent Conversations")
    print("=" * 60)
    print()

    agent = get_agent()

    test_messages = [
        "I spent 850 on pizza today",
        "How much did I spend today?",
        "My budget is 40000",
        "Where am I spending the most?",
        "Give me some suggestions"
    ]

    for i, message in enumerate(test_messages, 1):
        print(f"Test {i}: {message}")
        print("-" * 40)
        response = agent.process_message(message)
        print(f"Response: {response}")
        print()


def main():
    """Run the test."""
    try:
        test_conversation()
        print("=" * 60)
        print("[PASS] Agent conversation tests completed")
        print("=" * 60)
        return 0
    except Exception as e:
        print(f"[FAIL] Error during testing: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
