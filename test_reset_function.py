"""
Test script for reset_everything function.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from tools import reset_everything

def test_reset_function():
    """Test the reset_everything function directly."""
    print("Testing reset_everything function")
    print("=" * 60)

    try:
        result = reset_everything()
        print(f"Success: {result['success']}")
        print(f"Message: {result['message']}")

        if result.get("error"):
            print(f"Error: {result['error']}")

        return result["success"]
    except Exception as e:
        print(f"Exception: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_reset_function()
    sys.exit(0 if success else 1)
