"""
Main entry point for Personal Expense Advisor CLI application.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from agent import get_agent


def print_welcome():
    """Print welcome message."""
    print("=" * 60)
    print("Personal Expense Advisor - AI Agent")
    print("=" * 60)
    print("Track, analyze, and understand your personal expenses")
    print("Type 'exit' or 'quit' to exit")
    print("=" * 60)
    print()


def print_help():
    """Print help information."""
    print("\nAvailable commands:")
    print("  Add expenses: 'I spent 500 on lunch'")
    print("  Check spending: 'How much did I spend this month?'")
    print("  Budget check: 'My budget is 40000'")
    print("  Analysis: 'Where am I spending the most?'")
    print("  Suggestions: 'Give me some money-saving tips'")
    print("  Help: 'help' or '?'")
    print("  Exit: 'exit' or 'quit'")
    print()


def main():
    """Main application loop."""
    print_welcome()
    print_help()

    agent = get_agent()

    print("Note: This is an interactive application. Press Ctrl+C to exit.")
    print()

    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()

            # Check for exit commands
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("\nThank you for using Personal Expense Advisor. Goodbye!")
                break

            # Check for help command
            if user_input.lower() in ['help', '?', 'h']:
                print_help()
                continue

            # Skip empty input
            if not user_input:
                continue

            # Process the message
            print("Agent: ", end="", flush=True)
            response = agent.process_message(user_input)
            print(response)
            print()

        except KeyboardInterrupt:
            print("\n\nInterrupted by user. Goodbye!")
            break
        except EOFError:
            print("\n\nEnd of input detected. This application requires interactive terminal input.")
            print("For a demo, run: python demo.py")
            print("For testing, run: python test_agent.py")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again.")


if __name__ == "__main__":
    main()
