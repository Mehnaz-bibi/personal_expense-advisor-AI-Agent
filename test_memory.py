"""
Test script for memory functionality.
Tests the memory manager and memory-based features.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from memory import get_memory_manager, MemoryManager

def test_memory_manager():
    """Test memory manager functionality."""
    print("=" * 60)
    print("Memory Manager Tests")
    print("=" * 60)

    # Create fresh memory manager with unique file
    import time
    unique_id = str(int(time.time()))
    memory = MemoryManager(f"data/test_memory_{unique_id}.json")

    print("\n[PASS] Memory manager created")

    # Test preferences
    memory.set_preference("default_budget", 40000)
    budget = memory.get_preference("default_budget")
    assert budget == 40000, f"Expected 40000, got {budget}"
    print("[PASS] Set and get preference: default_budget")

    # Test category memory
    memory.remember_category("food")
    memory.remember_category("food")
    memory.remember_category("transport")

    common = memory.get_common_categories()
    assert common["food"] == 2, f"Expected food count 2, got {common['food']}"
    assert common["transport"] == 1, f"Expected transport count 1, got {common['transport']}"
    print("[PASS] Remember categories")

    # Test amount memory
    memory.remember_amount(500)
    memory.remember_amount(300)
    memory.remember_amount(1500)

    recent = memory.get_recent_amounts()
    assert len(recent) == 3, f"Expected 3 amounts, got {len(recent)}"
    assert recent == [500, 300, 1500], f"Expected [500, 300, 1500], got {recent}"
    print("[PASS] Remember amounts")

    # Test conversation history
    memory.add_conversation("I spent 500 on lunch", "Expense recorded successfully")
    memory.add_conversation("How much did I spend?", "You spent Rs. 500 today")

    history = memory.get_conversation_history(limit=2)
    assert len(history) == 2, f"Expected 2 conversations, got {len(history)}"
    print("[PASS] Add and get conversation history")

    # Test spending patterns
    patterns = memory.get_spending_patterns()
    assert patterns["most_common_category"] == "food", f"Expected 'food', got {patterns['most_common_category']}"
    assert abs(patterns["average_amount"] - 766.67) < 0.01, f"Expected ~766.67, got {patterns['average_amount']}"
    print("[PASS] Get spending patterns")

    # Test user profile
    memory.set_user_profile(name="John", location="New York")
    profile = memory.get_user_profile()
    assert profile["name"] == "John", f"Expected 'John', got {profile['name']}"
    assert profile["location"] == "New York", f"Expected 'New York', got {profile['location']}"
    print("[PASS] Set and get user profile")

    # Test clear history
    memory.clear_history()
    history = memory.get_conversation_history()
    assert len(history) == 0, f"Expected 0 conversations after clear, got {len(history)}"
    print("[PASS] Clear conversation history")

    # Clean up
    import os
    if os.path.exists(f"data/test_memory_{unique_id}.json"):
        os.remove(f"data/test_memory_{unique_id}.json")
    print("[PASS] Cleaned up test memory file")

    print("\n" + "=" * 60)
    print("All memory tests passed!")
    print("=" * 60)

    return True

def test_memory_integration():
    """Test memory integration with tools."""
    print("\n" + "=" * 60)
    print("Memory Integration Tests")
    print("=" * 60)

    from tools import set_user_budget, get_user_budget, get_conversation_summary, clear_memory

    # Test set user budget
    result = set_user_budget(50000)
    assert result["success"], f"Failed to set budget: {result.get('error')}"
    print("[PASS] Set user budget")

    # Test get user budget
    result = get_user_budget()
    assert result["success"], f"Failed to get budget: {result.get('error')}"
    assert result["budget"] == 50000, f"Expected 50000, got {result['budget']}"
    print("[PASS] Get user budget")

    # Test conversation summary
    result = get_conversation_summary()
    assert result["success"], f"Failed to get conversation summary: {result.get('error')}"
    print("[PASS] Get conversation summary")

    # Test clear memory
    result = clear_memory()
    assert result["success"], f"Failed to clear memory: {result.get('error')}"
    print("[PASS] Clear memory")

    print("\n" + "=" * 60)
    print("All memory integration tests passed!")
    print("=" * 60)

    return True

def main():
    """Run all memory tests."""
    try:
        test_memory_manager()
        test_memory_integration()
        return 0
    except Exception as e:
        print(f"\n[FAIL] Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
