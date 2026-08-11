"""
FastAPI application for Personal Expense Advisor Web UI.
Serves the web interface and API endpoints.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
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

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize agent
agent = get_agent()

# Initialize database on startup
try:
    from database import get_database
    db = get_database()
    print("Database initialized successfully")
except Exception as e:
    print(f"Warning: Database initialization failed: {e}")


class ExpenseRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str


class BudgetRequest(BaseModel):
    """Request model for budget check."""
    budget_limit: float


# API Endpoints
@app.get("/", response_class=HTMLResponse)
async def home():
    """Render the main interface."""
    try:
        with open("templates/index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
            # Replace the static file paths to work with the mounted static files
            return html_content
    except FileNotFoundError:
        return """
        <h1>Template not found</h1>
        <p>Please ensure templates/index.html exists in the project directory.</p>
        """


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
    import webbrowser
    import threading
    import time

    def open_browser(port):
        """Open browser after a short delay."""
        time.sleep(3)  # Wait for server to start
        url = f"http://127.0.0.1:{port}"
        print(f"✓ Opening browser at {url}")
        try:
            webbrowser.open(url)
        except Exception as e:
            print(f"Could not open browser automatically: {e}")
            print(f"Please manually open: {url}")

    # Try port 8000 first, then 8001, 8002, etc.
    for port in [8000, 8001, 8002, 8003, 8080, 3000]:
        try:
            print("=" * 60)
            print("Personal Expense Advisor - Web Server")
            print("=" * 60)
            print(f"✓ Starting server on port {port}...")
            print(f"✓ Server will be available at: http://127.0.0.1:{port}")
            print(f"✓ Opening browser automatically...")
            print("=" * 60)

            # Open browser in a separate thread
            browser_thread = threading.Thread(target=open_browser, args=(port,))
            browser_thread.daemon = True
            browser_thread.start()

            # Start the server
            uvicorn.run(app, host="127.0.0.1", port=port)
            break
        except OSError as e:
            if "address already in use" in str(e) or "only one usage" in str(e):
                print(f"✗ Port {port} is already in use, trying next port...")
                continue
            else:
                print(f"✗ Error starting server: {e}")
                break
