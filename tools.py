"""
Tools module for Personal Expense Advisor.
Contains functions that the AI agent can call to perform actions.
"""

from typing import List, Dict, Optional
from datetime import datetime
from database import get_database
from memory import get_memory_manager


# Valid expense categories
VALID_CATEGORIES = [
    "food",
    "groceries",
    "transport",
    "shopping",
    "bills",
    "entertainment",
    "health",
    "education",
    "other"
]


def add_expense(
    amount: float,
    category: str,
    description: Optional[str] = None,
    date: Optional[str] = None
) -> Dict:
    """
    Add a new expense to the database.

    Args:
        amount: Expense amount (positive number)
        category: Expense category (food, groceries, transport, shopping, bills, entertainment, health, education, other)
        description: Optional description of the expense
        date: Date in YYYY-MM-DD format (defaults to today)

    Returns:
        Dictionary with success status and expense details
    """
    try:
        # Validate amount
        if amount <= 0:
            return {
                "success": False,
                "error": "Amount must be positive"
            }

        # Normalize category
        category = category.lower().strip()
        if category not in VALID_CATEGORIES:
            return {
                "success": False,
                "error": f"Invalid category. Valid categories: {', '.join(VALID_CATEGORIES)}"
            }

        # Validate date format if provided
        if date:
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                return {
                    "success": False,
                    "error": "Invalid date format. Use YYYY-MM-DD"
                }

        # Add to database
        db = get_database()
        expense_id = db.add_expense(amount, category, description, date)

        return {
            "success": True,
            "expense_id": expense_id,
            "amount": amount,
            "category": category,
            "description": description,
            "date": date or datetime.now().strftime("%Y-%m-%d"),
            "message": f"Rs. {amount:,.2f} {category} expense has been recorded."
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to add expense: {str(e)}"
        }


def get_expenses(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    category: Optional[str] = None
) -> Dict:
    """
    Retrieve expenses from the database with optional filters.

    Args:
        start_date: Start date in YYYY-MM-DD format (inclusive)
        end_date: End date in YYYY-MM-DD format (inclusive)
        category: Filter by category

    Returns:
        Dictionary with success status and list of expenses
    """
    try:
        db = get_database()
        expenses = db.get_expenses(start_date, end_date, category)

        return {
            "success": True,
            "count": len(expenses),
            "expenses": expenses,
            "total": sum(exp["amount"] for exp in expenses)
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to retrieve expenses: {str(e)}"
        }


def get_expenses_today() -> Dict:
    """
    Get all expenses for today.

    Returns:
        Dictionary with success status and today's expenses
    """
    try:
        db = get_database()
        expenses = db.get_expenses_today()

        return {
            "success": True,
            "count": len(expenses),
            "expenses": expenses,
            "total": sum(exp["amount"] for exp in expenses),
            "date": datetime.now().strftime("%Y-%m-%d")
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to retrieve today's expenses: {str(e)}"
        }


def get_expenses_this_month() -> Dict:
    """
    Get all expenses for the current month.

    Returns:
        Dictionary with success status and this month's expenses
    """
    try:
        db = get_database()
        expenses = db.get_expenses_this_month()

        return {
            "success": True,
            "count": len(expenses),
            "expenses": expenses,
            "total": sum(exp["amount"] for exp in expenses),
            "month": datetime.now().strftime("%Y-%m")
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to retrieve this month's expenses: {str(e)}"
        }


def calculate_total(expenses: List[Dict]) -> Dict:
    """
    Calculate the total amount from a list of expenses.

    Args:
        expenses: List of expense dictionaries

    Returns:
        Dictionary with total amount and breakdown
    """
    try:
        if not expenses:
            return {
                "success": True,
                "total": 0.0,
                "count": 0,
                "message": "No expenses to calculate"
            }

        total = sum(exp["amount"] for exp in expenses)
        count = len(expenses)

        # Calculate category breakdown
        category_totals = {}
        for exp in expenses:
            category = exp["category"]
            category_totals[category] = category_totals.get(category, 0) + exp["amount"]

        return {
            "success": True,
            "total": total,
            "count": count,
            "category_breakdown": category_totals,
            "average": total / count if count > 0 else 0
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to calculate total: {str(e)}"
        }


def calculate_category_percentage(category: str, total_spending: float) -> Dict:
    """
    Calculate what percentage of total spending went to a specific category.

    Args:
        category: Category name
        total_spending: Total spending amount

    Returns:
        Dictionary with percentage calculation
    """
    try:
        if total_spending <= 0:
            return {
                "success": False,
                "error": "Total spending must be positive"
            }

        db = get_database()
        category_spending = db.get_total_spending(category=category)
        percentage = (category_spending / total_spending) * 100

        return {
            "success": True,
            "category": category,
            "category_spending": category_spending,
            "total_spending": total_spending,
            "percentage": round(percentage, 2)
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to calculate percentage: {str(e)}"
        }


def check_budget(budget_limit: float) -> Dict:
    """
    Check current spending against a budget limit.

    Args:
        budget_limit: Monthly budget limit

    Returns:
        Dictionary with budget status and recommendations
    """
    try:
        if budget_limit <= 0:
            return {
                "success": False,
                "error": "Budget limit must be positive"
            }

        db = get_database()
        current_spending = db.get_total_spending_this_month()
        remaining = budget_limit - current_spending
        percentage_used = (current_spending / budget_limit) * 100

        # Determine status
        if percentage_used >= 100:
            status = "exceeded"
            message = f"You have exceeded your budget by Rs. {abs(remaining):,.2f}"
        elif percentage_used >= 90:
            status = "warning"
            message = f"You have used {percentage_used:.1f}% of your budget. Only Rs. {remaining:,.2f} remaining."
        elif percentage_used >= 70:
            status = "caution"
            message = f"You have used {percentage_used:.1f}% of your budget. Rs. {remaining:,.2f} remaining."
        else:
            status = "healthy"
            message = f"You are within budget. Rs. {remaining:,.2f} remaining ({percentage_used:.1f}% used)."

        # Get category breakdown
        category_breakdown = db.get_category_breakdown()

        return {
            "success": True,
            "budget_limit": budget_limit,
            "current_spending": current_spending,
            "remaining": remaining,
            "percentage_used": round(percentage_used, 2),
            "status": status,
            "message": message,
            "category_breakdown": category_breakdown
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to check budget: {str(e)}"
        }


def analyze_spending_patterns() -> Dict:
    """
    Analyze spending patterns from historical data.

    Returns:
        Dictionary with spending analysis and insights
    """
    try:
        db = get_database()

        # Get this month's expenses
        this_month_expenses = db.get_expenses_this_month()
        this_month_total = sum(exp["amount"] for exp in this_month_expenses)

        # Get category breakdown
        category_breakdown = db.get_category_breakdown()

        # Find highest spending category
        if category_breakdown:
            highest_category = max(category_breakdown.items(), key=lambda x: x[1])
        else:
            highest_category = (None, 0)

        # Calculate average daily spending this month
        now = datetime.now()
        days_in_month = now.day
        avg_daily = this_month_total / days_in_month if days_in_month > 0 else 0

        return {
            "success": True,
            "this_month_total": this_month_total,
            "this_month_count": len(this_month_expenses),
            "category_breakdown": category_breakdown,
            "highest_category": {
                "name": highest_category[0],
                "amount": highest_category[1],
                "percentage": (highest_category[1] / this_month_total * 100) if this_month_total > 0 else 0
            },
            "average_daily_spending": round(avg_daily, 2),
            "days_so_far": days_in_month
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to analyze spending patterns: {str(e)}"
        }


def get_spending_suggestions(budget_limit: Optional[float] = None) -> Dict:
    """
    Generate personalized spending suggestions based on current data.

    Args:
        budget_limit: Optional budget limit for context

    Returns:
        Dictionary with suggestions and recommendations
    """
    try:
        analysis = analyze_spending_patterns()
        if not analysis["success"]:
            return analysis

        suggestions = []
        memory = get_memory_manager()

        # Suggestion based on highest category
        if analysis["highest_category"]["name"]:
            highest_cat = analysis["highest_category"]
            if highest_cat["percentage"] > 30:
                suggestions.append(
                    f"Your spending on {highest_cat['name']} is {highest_cat['percentage']:.1f}% of your total. "
                    f"Consider setting a specific budget for this category."
                )

        # Suggestion based on daily average
        if analysis["average_daily_spending"] > 0:
            projected_monthly = analysis["average_daily_spending"] * 30
            suggestions.append(
                f"Based on your average daily spending of Rs. {analysis['average_daily_spending']:.2f}, "
                f"you're projected to spend Rs. {projected_monthly:,.2f} this month."
            )

        # Memory-based suggestions
        patterns = memory.get_spending_patterns()
        if patterns["most_common_category"]:
            suggestions.append(
                f"I notice you frequently spend on {patterns['most_common_category']}. "
                f"This is your most common expense category."
            )

        if patterns["average_amount"] > 0:
            suggestions.append(
                f"Your average expense amount is Rs. {patterns['average_amount']:.2f}. "
                f"Try to keep individual expenses below Rs. {patterns['average_amount'] * 1.5:.2f} when possible."
            )

        # Budget-specific suggestions
        if budget_limit:
            budget_check = check_budget(budget_limit)
            if budget_check["success"]:
                if budget_check["status"] == "warning":
                    suggestions.append(
                        "You're approaching your budget limit. Review your discretionary spending."
                    )
                elif budget_check["status"] == "exceeded":
                    suggestions.append(
                        "You've exceeded your budget. Identify non-essential expenses to reduce."
                    )

        # General suggestions
        if analysis["this_month_count"] < 5:
            suggestions.append(
                "You have very few recorded expenses this month. Make sure to track all your spending."
            )

        return {
            "success": True,
            "suggestions": suggestions,
            "analysis": analysis,
            "memory_patterns": patterns
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to generate suggestions: {str(e)}"
        }


def set_user_budget(budget: float) -> Dict:
    """
    Set the user's default budget in memory.

    Args:
        budget: Monthly budget amount

    Returns:
        Dictionary with success status
    """
    try:
        memory = get_memory_manager()
        memory.set_default_budget(budget)
        return {
            "success": True,
            "message": f"Default budget set to Rs. {budget:,.2f}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to set budget: {str(e)}"
        }


def get_user_budget() -> Dict:
    """
    Get the user's default budget from memory.

    Returns:
        Dictionary with budget information
    """
    try:
        memory = get_memory_manager()
        budget = memory.get_default_budget()
        if budget:
            return {
                "success": True,
                "budget": budget,
                "message": f"Your default budget is Rs. {budget:,.2f}"
            }
        else:
            return {
                "success": True,
                "budget": None,
                "message": "No default budget set. You can set one with: 'Set my budget to 40000'"
            }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to get budget: {str(e)}"
        }


def get_conversation_summary() -> Dict:
    """
    Get a summary of recent conversations.

    Returns:
        Dictionary with conversation summary
    """
    try:
        memory = get_memory_manager()
        history = memory.get_conversation_history(limit=5)
        patterns = memory.get_spending_patterns()

        return {
            "success": True,
            "recent_conversations": len(history),
            "total_conversations": patterns["total_conversations"],
            "most_common_category": patterns["most_common_category"],
            "average_amount": patterns["average_amount"]
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to get conversation summary: {str(e)}"
        }


def clear_memory() -> Dict:
    """
    Clear conversation history from memory.

    Returns:
        Dictionary with success status
    """
    try:
        memory = get_memory_manager()
        memory.clear_history()
        return {
            "success": True,
            "message": "Conversation history has been cleared."
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to clear memory: {str(e)}"
        }


def reset_everything() -> Dict:
    """
    Reset everything - clear memory and all expenses from database.

    Returns:
        Dictionary with success status
    """
    try:
        # Clear memory
        memory = get_memory_manager()
        memory.clear_history()

        # Clear all expenses from database
        db = get_database()
        all_expenses = db.get_expenses()

        deleted_count = 0
        for expense in all_expenses:
            db.delete_expense(expense["id"])
            deleted_count += 1

        return {
            "success": True,
            "message": f"Reset complete! Cleared {deleted_count} expenses and conversation history."
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to reset everything: {str(e)}"
        }


# Tool metadata for function calling
TOOLS_METADATA = [
    {
        "name": "add_expense",
        "description": "Add a new expense to the database",
        "parameters": {
            "amount": {"type": "float", "description": "Expense amount (positive number)"},
            "category": {"type": "string", "description": f"Expense category: {', '.join(VALID_CATEGORIES)}"},
            "description": {"type": "string", "description": "Optional description of the expense", "required": False},
            "date": {"type": "string", "description": "Date in YYYY-MM-DD format (defaults to today)", "required": False}
        }
    },
    {
        "name": "get_expenses",
        "description": "Retrieve expenses from the database with optional filters",
        "parameters": {
            "start_date": {"type": "string", "description": "Start date in YYYY-MM-DD format (inclusive)", "required": False},
            "end_date": {"type": "string", "description": "End date in YYYY-MM-DD format (inclusive)", "required": False},
            "category": {"type": "string", "description": "Filter by category", "required": False}
        }
    },
    {
        "name": "get_expenses_today",
        "description": "Get all expenses for today",
        "parameters": {}
    },
    {
        "name": "get_expenses_this_month",
        "description": "Get all expenses for the current month",
        "parameters": {}
    },
    {
        "name": "calculate_total",
        "description": "Calculate the total amount from a list of expenses",
        "parameters": {
            "expenses": {"type": "array", "description": "List of expense dictionaries"}
        }
    },
    {
        "name": "check_budget",
        "description": "Check current spending against a budget limit",
        "parameters": {
            "budget_limit": {"type": "float", "description": "Monthly budget limit"}
        }
    },
    {
        "name": "analyze_spending_patterns",
        "description": "Analyze spending patterns from historical data",
        "parameters": {}
    },
    {
        "name": "get_spending_suggestions",
        "description": "Generate personalized spending suggestions based on current data",
        "parameters": {
            "budget_limit": {"type": "float", "description": "Optional budget limit for context", "required": False}
        }
    },
    {
        "name": "set_user_budget",
        "description": "Set the user's default budget in memory",
        "parameters": {
            "budget": {"type": "float", "description": "Monthly budget amount"}
        }
    },
    {
        "name": "get_user_budget",
        "description": "Get the user's default budget from memory",
        "parameters": {}
    },
    {
        "name": "get_conversation_summary",
        "description": "Get a summary of recent conversations",
        "parameters": {}
    },
    {
        "name": "clear_memory",
        "description": "Clear conversation history from memory",
        "parameters": {}
    },
    {
        "name": "reset_everything",
        "description": "Reset everything - clear memory and all expenses from database",
        "parameters": {}
    }
]
