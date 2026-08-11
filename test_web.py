"""
Test script for web API endpoints.
Tests the FastAPI application and API functionality.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
import time
import socket

def find_available_port(start_port=8000, max_attempts=10):
    """Find an available port starting from start_port."""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            continue
    return 8000  # Default fallback

BASE_URL = f"http://localhost:{find_available_port()}"


def test_health():
    """Test health endpoint."""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_chat():
    """Test chat endpoint."""
    print("\nTesting chat endpoint...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/chat",
            json={"message": "I spent 500 on lunch"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_today_expenses():
    """Test today's expenses endpoint."""
    print("\nTesting today's expenses endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/expenses/today")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_month_expenses():
    """Test month's expenses endpoint."""
    print("\nTesting month's expenses endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/expenses/month")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_analysis():
    """Test analysis endpoint."""
    print("\nTesting analysis endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/analysis")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Web API Tests")
    print("=" * 60)
    print("Make sure the server is running with: python app.py")
    print()

    # Try to find which port the server is using
    port = find_available_port()
    print(f"Trying to connect to port {port}...")

    # Try common ports if the default is not available
    for test_port in [8000, 8001, 8002, 8080, 3000]:
        try:
            test_url = f"http://localhost:{test_port}"
            response = requests.get(f"{test_url}/health", timeout=2)
            if response.status_code == 200:
                global BASE_URL
                BASE_URL = test_url
                print(f"Found server running on port {test_port}")
                break
        except:
            continue
    else:
        print("Could not find running server. Please start it with: python app.py")
        return 1

    print(f"Testing endpoints at: {BASE_URL}")
    print()

    # Wait a moment for server to be ready
    print("Waiting for server to be ready...")
    time.sleep(1)

    tests = [
        test_health,
        test_chat,
        test_today_expenses,
        test_month_expenses,
        test_analysis
    ]

    results = []
    for test in tests:
        result = test()
        results.append(result)
        print()

    print("=" * 60)
    print(f"Test Results: {sum(results)}/{len(results)} passed")
    print("=" * 60)

    if all(results):
        print("All tests passed!")
        return 0
    else:
        print("Some tests failed")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nTests interrupted")
        sys.exit(1)
