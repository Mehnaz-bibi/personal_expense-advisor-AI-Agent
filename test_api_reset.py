"""
Test the reset API endpoint directly.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
import time

def test_reset_api():
    """Test the reset API endpoint."""
    print("Testing Reset API Endpoint")
    print("=" * 60)

    # First, add some test expenses
    print("\n1. Adding test expenses...")
    try:
        from tools import add_expense
        add_expense(500, "food", "Test expense 1")
        add_expense(300, "transport", "Test expense 2")
        add_expense(1000, "shopping", "Test expense 3")
        print("✓ Added 3 test expenses")
    except Exception as e:
        print(f"✗ Failed to add test expenses: {e}")

    # Wait for server
    print("\n2. Waiting for server...")
    time.sleep(3)

    # Test the reset endpoint
    print("\n3. Testing reset endpoint...")
    try:
        response = requests.post("http://localhost:8000/api/reset-memory", timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")

        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print("✓ Reset API working!")
                return True
            else:
                print(f"✗ API returned error: {data.get('error')}")
                return False
        else:
            print(f"✗ Unexpected status code: {response.status_code}")
            return False

    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to server. Is it running?")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Make sure the server is running with: python app.py")
    print()
    success = test_reset_api()
    sys.exit(0 if success else 1)
