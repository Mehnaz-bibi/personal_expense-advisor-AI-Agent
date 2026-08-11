"""
Database initialization script.
Creates the expenses table and initializes the database.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from database import get_database

def initialize_database():
    """Initialize the database with the expenses table."""
    print("Initializing database...")
    print("-" * 50)

    try:
        # Get database instance (this will create the table if it doesn't exist)
        db = get_database()
        print("✓ Database connection successful")

        # Add a test expense to verify the table works
        test_expense_id = db.add_expense(
            amount=100,
            category="food",
            description="Database initialization test",
            date="2026-08-11"
        )
        print(f"✓ Test expense added with ID: {test_expense_id}")

        # Verify the expense was added
        expenses = db.get_expenses()
        print(f"✓ Retrieved {len(expenses)} expenses from database")

        # Clean up the test expense
        db.delete_expense(test_expense_id)
        print("✓ Test expense cleaned up")

        print("-" * 50)
        print("Database initialization complete!")
        print("The expenses table is now ready to use.")

        return True

    except Exception as e:
        print(f"✗ Database initialization failed: {e}")
        return False

if __name__ == "__main__":
    success = initialize_database()
    sys.exit(0 if success else 1)
