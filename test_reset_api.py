"""
Test script for reset memory API endpoint.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
import time

def test_reset_memory_api():
    """Test the reset memory API endpoint."""
    print("Testing Reset Memory API Endpoint")
    print("=" * 60)

    # Wait for server to be ready
    print("Waiting for server...")
    time.sleep(2)

    try:
        # Try the reset memory endpoint
        response = requests.post("http://localhost:8000/api/reset-memory", timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")

        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print("✓ Reset memory API working!")
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
        return False

if __name__ == "__main__":
    print("Make sure the server is running with: python app.py")
    print()
    success = test_reset_memory_api()
    sys.exit(0 if success else 1)
