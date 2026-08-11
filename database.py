"""
Database module for Personal Expense Advisor.
Handles SQLite database operations for expense tracking.
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional


class ExpenseDatabase:
    """Manages SQLite database operations for expenses."""

    def __init__(self, db_path: str = "data/expenses.db"):
        """
        Initialize database connection.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._ensure_db_exists()
        self._create_tables()

    def _ensure_db_exists(self):
        """Ensure the database directory and file exist."""
        # Create directory if it doesn't exist
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)

    def _get_connection(self) -> sqlite3.Connection:
        """Get a database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn

    def _create_tables(self):
        """Create the expenses table if it doesn't exist."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                date TEXT NOT NULL
            )
        """)

        conn.commit()
        conn.close()

    def add_expense(
        self,
        amount: float,
        category: str,
        description: Optional[str] = None,
        date: Optional[str] = None
    ) -> int:
        """
        Add a new expense to the database.

        Args:
            amount: Expense amount
            category: Expense category
            description: Optional description
            date: Date in YYYY-MM-DD format (defaults to today)

        Returns:
            ID of the inserted expense
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO expenses (amount, category, description, date)
            VALUES (?, ?, ?, ?)
            """,
            (amount, category, description, date)
        )

        expense_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return expense_id

    def get_expenses(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        category: Optional[str] = None
    ) -> List[Dict]:
        """
        Retrieve expenses from the database with optional filters.

        Args:
            start_date: Start date in YYYY-MM-DD format (inclusive)
            end_date: End date in YYYY-MM-DD format (inclusive)
            category: Filter by category

        Returns:
            List of expense dictionaries
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM expenses WHERE 1=1"
        params = []

        if start_date:
            query += " AND date >= ?"
            params.append(start_date)

        if end_date:
            query += " AND date <= ?"
            params.append(end_date)

        if category:
            query += " AND category = ?"
            params.append(category)

        query += " ORDER BY date DESC, id DESC"

        cursor.execute(query, params)
        rows = cursor.fetchall()

        expenses = []
        for row in rows:
            expenses.append({
                "id": row["id"],
                "amount": row["amount"],
                "category": row["category"],
                "description": row["description"],
                "date": row["date"]
            })

        conn.close()
        return expenses

    def get_expenses_by_date_range(
        self,
        start_date: str,
        end_date: str
    ) -> List[Dict]:
        """
        Get expenses for a specific date range.

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format

        Returns:
            List of expense dictionaries
        """
        return self.get_expenses(start_date=start_date, end_date=end_date)

    def get_expenses_by_category(self, category: str) -> List[Dict]:
        """
        Get all expenses for a specific category.

        Args:
            category: Category name

        Returns:
            List of expense dictionaries
        """
        return self.get_expenses(category=category)

    def get_expenses_today(self) -> List[Dict]:
        """
        Get all expenses for today.

        Returns:
            List of expense dictionaries
        """
        today = datetime.now().strftime("%Y-%m-%d")
        return self.get_expenses(start_date=today, end_date=today)

    def get_expenses_this_month(self) -> List[Dict]:
        """
        Get all expenses for the current month.

        Returns:
            List of expense dictionaries
        """
        now = datetime.now()
        start_date = now.strftime("%Y-%m-01")
        end_date = now.strftime("%Y-%m-%d")
        return self.get_expenses(start_date=start_date, end_date=end_date)

    def get_total_spending_this_month(self) -> float:
        """
        Get total spending for the current month.

        Returns:
            Total spending amount
        """
        expenses = self.get_expenses_this_month()
        return sum(expense["amount"] for expense in expenses)

    def get_total_spending(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        category: Optional[str] = None
    ) -> float:
        """
        Calculate total spending for given filters.

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            category: Filter by category

        Returns:
            Total spending amount
        """
        expenses = self.get_expenses(start_date, end_date, category)
        return sum(expense["amount"] for expense in expenses)

    def get_category_breakdown(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, float]:
        """
        Get spending breakdown by category.

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format

        Returns:
            Dictionary mapping categories to total amounts
        """
        expenses = self.get_expenses(start_date, end_date)
        breakdown = {}

        for expense in expenses:
            category = expense["category"]
            amount = expense["amount"]
            breakdown[category] = breakdown.get(category, 0) + amount

        return breakdown

    def delete_expense(self, expense_id: int) -> bool:
        """
        Delete an expense by ID.

        Args:
            expense_id: ID of the expense to delete

        Returns:
            True if deleted, False if not found
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        deleted = cursor.rowcount > 0

        conn.commit()
        conn.close()

        return deleted


# Singleton instance for use throughout the application
_db_instance: Optional[ExpenseDatabase] = None


def get_database(db_path: str = "data/expenses.db") -> ExpenseDatabase:
    """
    Get or create the database singleton instance.

    Args:
        db_path: Path to SQLite database file

    Returns:
        ExpenseDatabase instance
    """
    global _db_instance
    if _db_instance is None:
        _db_instance = ExpenseDatabase(db_path)
    return _db_instance
