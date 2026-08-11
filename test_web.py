"""
Test script for web API endpoints.
Tests the FastAPI application and API functionality.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
import time

BASE_URL = "http://localhost:8000"


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
    print(f"Testing endpoints at: {BASE_URL}")
    print("Make sure the server is running with: python app.py")
    print()

    # Wait a moment for server to be ready
    print("Waiting for server to be ready...")
    time.sleep(2)

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
