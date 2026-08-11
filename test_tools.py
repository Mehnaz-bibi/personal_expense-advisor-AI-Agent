"""
Test script for database and tools functionality.
Run this to verify that Phase 1 and Phase 2 are working correctly.
"""

import os
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from database import get_database
from tools import (
    add_expense,
    get_expenses,
    get_expenses_today,
    get_expenses_this_month,
    calculate_total,
    check_budget,
    analyze_spending_patterns,
    get_spending_suggestions
)


def test_database():
    """Test database connection and basic operations."""
    print("Testing Database...")
    print("-" * 50)

    try:
        # Test database connection
        db = get_database()
        print("[PASS] Database connection successful")

        # Test adding expense
        expense_id = db.add_expense(1200, "groceries", "Monthly groceries", "2026-08-10")
        print(f"[PASS] Added expense with ID: {expense_id}")

        # Test retrieving expenses
        expenses = db.get_expenses()
        print(f"[PASS] Retrieved {len(expenses)} expenses")

        # Test filtering by date
        today_expenses = db.get_expenses_today()
        print(f"[PASS] Retrieved {len(today_expenses)} expenses for today")

        print("Database tests passed!\n")
        return True

    except Exception as e:
        print(f"[FAIL] Database test failed: {e}\n")
        return False


def test_add_expense():
    """Test add_expense tool."""
    print("Testing add_expense tool...")
    print("-" * 50)

    try:
        # Test valid expense
        result = add_expense(500, "food", "Lunch", "2026-08-11")
        if result["success"]:
            print(f"[PASS] Added expense: {result['message']}")
        else:
            print(f"[FAIL] Failed to add expense: {result['error']}")
            return False

        # Test invalid amount
        result = add_expense(-100, "food")
        if not result["success"]:
            print("[PASS] Correctly rejected negative amount")
        else:
            print("[FAIL] Should have rejected negative amount")
            return False

        # Test invalid category
        result = add_expense(100, "invalid_category")
        if not result["success"]:
            print("[PASS] Correctly rejected invalid category")
        else:
            print("[FAIL] Should have rejected invalid category")
            return False

        print("add_expense tests passed!\n")
        return True

    except Exception as e:
        print(f"[FAIL] add_expense test failed: {e}\n")
        return False


def test_get_expenses():
    """Test get_expenses tool."""
    print("Testing get_expenses tool...")
    print("-" * 50)

    try:
        # Test get all expenses
        result = get_expenses()
        if result["success"]:
            print(f"[PASS] Retrieved {result['count']} expenses")
        else:
            print(f"[FAIL] Failed to get expenses: {result['error']}")
            return False

        # Test get today's expenses
        result = get_expenses_today()
        if result["success"]:
            print(f"[PASS] Retrieved {result['count']} expenses for today")
        else:
            print(f"[FAIL] Failed to get today's expenses: {result['error']}")
            return False

        # Test get this month's expenses
        result = get_expenses_this_month()
        if result["success"]:
            print(f"[PASS] Retrieved {result['count']} expenses for this month")
        else:
            print(f"[FAIL] Failed to get this month's expenses: {result['error']}")
            return False

        print("get_expenses tests passed!\n")
        return True

    except Exception as e:
        print(f"[FAIL] get_expenses test failed: {e}\n")
        return False


def test_calculate_total():
    """Test calculate_total tool."""
    print("Testing calculate_total tool...")
    print("-" * 50)

    try:
        # Test with expenses
        test_expenses = [
            {"amount": 100, "category": "food"},
            {"amount": 200, "category": "transport"},
            {"amount": 150, "category": "shopping"}
        ]
        result = calculate_total(test_expenses)
        if result["success"]:
            print(f"[PASS] Calculated total: Rs. {result['total']}")
            print(f"[PASS] Category breakdown: {result['category_breakdown']}")
        else:
            print(f"[FAIL] Failed to calculate total: {result['error']}")
            return False

        # Test with empty list
        result = calculate_total([])
        if result["success"] and result["total"] == 0:
            print("[PASS] Correctly handled empty expense list")
        else:
            print("[FAIL] Failed to handle empty expense list")
            return False

        print("calculate_total tests passed!\n")
        return True

    except Exception as e:
        print(f"[FAIL] calculate_total test failed: {e}\n")
        return False


def test_check_budget():
    """Test check_budget tool."""
    print("Testing check_budget tool...")
    print("-" * 50)

    try:
        # Test with a budget
        result = check_budget(40000)
        if result["success"]:
            print(f"[PASS] Budget check: {result['message']}")
            print(f"[PASS] Status: {result['status']}")
            print(f"[PASS] Percentage used: {result['percentage_used']}%")
        else:
            print(f"[FAIL] Failed to check budget: {result['error']}")
            return False

        # Test with invalid budget
        result = check_budget(-100)
        if not result["success"]:
            print("[PASS] Correctly rejected negative budget")
        else:
            print("[FAIL] Should have rejected negative budget")
            return False

        print("check_budget tests passed!\n")
        return True

    except Exception as e:
        print(f"[FAIL] check_budget test failed: {e}\n")
        return False


def test_analyze_spending():
    """Test analyze_spending_patterns tool."""
    print("Testing analyze_spending_patterns tool...")
    print("-" * 50)

    try:
        result = analyze_spending_patterns()
        if result["success"]:
            print(f"[PASS] This month total: Rs. {result['this_month_total']}")
            print(f"[PASS] Count: {result['this_month_count']} expenses")
            if result['highest_category']['name']:
                print(f"[PASS] Highest category: {result['highest_category']['name']} "
                      f"(Rs. {result['highest_category']['amount']})")
            print(f"[PASS] Average daily spending: Rs. {result['average_daily_spending']}")
        else:
            print(f"[FAIL] Failed to analyze spending: {result['error']}")
            return False

        print("analyze_spending_patterns tests passed!\n")
        return True

    except Exception as e:
        print(f"[FAIL] analyze_spending_patterns test failed: {e}\n")
        return False


def test_spending_suggestions():
    """Test get_spending_suggestions tool."""
    print("Testing get_spending_suggestions tool...")
    print("-" * 50)

    try:
        result = get_spending_suggestions(budget_limit=40000)
        if result["success"]:
            print(f"[PASS] Generated {len(result['suggestions'])} suggestions:")
            for i, suggestion in enumerate(result['suggestions'], 1):
                print(f"  {i}. {suggestion}")
        else:
            print(f"[FAIL] Failed to generate suggestions: {result['error']}")
            return False

        print("get_spending_suggestions tests passed!\n")
        return True

    except Exception as e:
        print(f"[FAIL] get_spending_suggestions test failed: {e}\n")
        return False


def cleanup_test_data():
    """Clean up test data from database."""
    print("Cleaning up test data...")
    print("-" * 50)

    try:
        db = get_database()
        # Note: In a real application, you might want to be more selective
        # about what to delete. For testing, we'll leave the data.
        print("[PASS] Test data left in database for inspection\n")
        return True

    except Exception as e:
        print(f"[FAIL] Cleanup failed: {e}\n")
        return False


def main():
    """Run all tests."""
    print("=" * 50)
    print("Personal Expense Advisor - Tool Tests")
    print("=" * 50)
    print()

    tests = [
        test_database,
        test_add_expense,
        test_get_expenses,
        test_calculate_total,
        test_check_budget,
        test_analyze_spending,
        test_spending_suggestions,
        cleanup_test_data
    ]

    passed = 0
    failed = 0

    for test in tests:
        if test():
            passed += 1
        else:
            failed += 1

    print("=" * 50)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 50)

    if failed == 0:
        print("[PASS] All tests passed!")
        return 0
    else:
        print("[FAIL] Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
