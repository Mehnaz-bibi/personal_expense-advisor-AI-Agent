"""
FastAPI application for Personal Expense Advisor Web UI.
Serves the web interface and API endpoints.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from agent import get_agent
from tools import (
    get_expenses_today,
    get_expenses_this_month,
    check_budget,
    analyze_spending_patterns
)
from pydantic import BaseModel
from typing import Optional

# Create FastAPI app
app = FastAPI(
    title="Personal Expense Advisor",
    description="AI-powered expense tracking and analysis",
    version="1.0.0"
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize agent
agent = get_agent()


class ExpenseRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str


class BudgetRequest(BaseModel):
    """Request model for budget check."""
    budget_limit: float


# API Endpoints
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the main interface."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/chat")
async def chat(request: ExpenseRequest):
    """Process user message and return agent response."""
    try:
        response = agent.process_message(request.message)
        return {"success": True, "response": response}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/api/expenses/today")
async def get_today_expenses():
    """Get today's expenses."""
    try:
        result = get_expenses_today()
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/api/expenses/month")
async def get_month_expenses():
    """Get this month's expenses."""
    try:
        result = get_expenses_this_month()
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.post("/api/budget")
async def check_budget_endpoint(request: BudgetRequest):
    """Check budget status."""
    try:
        result = check_budget(request.budget_limit)
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/api/analysis")
async def get_analysis():
    """Get spending analysis."""
    try:
        result = analyze_spending_patterns()
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Personal Expense Advisor"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
