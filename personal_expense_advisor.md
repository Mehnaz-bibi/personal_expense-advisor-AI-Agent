# Personal Expense Advisor Agent

## 1. Project Overview

**Personal Expense Advisor** is a simple single-agent AI application that helps users record, analyze, and understand their personal expenses.

The main purpose of this project is to learn how an **AI Agent** works in a practical scenario using:

- LLM
- Tool / Function Calling
- Agent decision-making
- SQLite database
- Basic financial analysis
- Personalized recommendations

The agent does not only answer questions. It decides when it needs to use a tool, executes that tool through the application, receives the result, and then generates a useful response.

---

## 2. Main Goal

Build a single AI agent that can:

1. Understand natural-language expense input.
2. Add expenses to a database.
3. Retrieve previous expenses.
4. Calculate totals and percentages.
5. Categorize spending.
6. Check spending against a budget.
7. Analyze spending patterns.
8. Provide personalized budgeting suggestions.

---

## 3. Example Interaction

### Adding an Expense

**User:**

> I spent 1200 on groceries today.

**Agent:**

1. Understands the amount and category.
2. Decides that an expense needs to be stored.
3. Calls the `add_expense` tool.
4. The application stores the record in SQLite.
5. Agent confirms the action.

**Response:**

> Rs. 1,200 grocery expense has been recorded.

---

### Asking for Spending Analysis

**User:**

> How much did I spend this month?

**Agent workflow:**

```text
User Question
      ↓
LLM Agent
      ↓
Needs expense history
      ↓
get_expenses()
      ↓
Calculate total
      ↓
Analyze result
      ↓
Final Answer
```

---

### Asking for Budget Advice

**User:**

> My monthly budget is Rs. 40,000. Am I spending too much?

The agent can:

```text
Get expenses
      ↓
Calculate total
      ↓
Compare with budget
      ↓
Find highest categories
      ↓
Generate recommendation
```

---

# 4. System Architecture

```text
                         USER
                           |
                           v
                    +--------------+
                    |   AI AGENT   |
                    |     LLM      |
                    +------+-------+
                           |
             +-------------+-------------+
             |             |             |
             v             v             v
       Expense Tool   Calculator Tool  Budget Tool
             |             |             |
             +-------------+-------------+
                           |
                           v
                     SQLite Database
                           |
                           v
                    Tool Results
                           |
                           v
                    AI Agent / LLM
                           |
                           v
                    Final Response
```

---

# 5. Agent Workflow

```text
User Input
    |
    v
LLM Agent
    |
    v
Understand User Intent
    |
    v
Does the task require a tool?
    |
    +---- No ----> Generate Answer
    |
    +---- Yes
             |
             v
       Select Appropriate Tool
             |
             v
        Execute Tool
             |
             v
        Get Tool Result
             |
             v
        Send Result to LLM
             |
             v
        Generate Response
```

---

# 6. Core Tools

## 6.1 Add Expense Tool

Stores a new expense.

### Input

```text
amount
category
description
date
```

### Example

```python
add_expense(
    amount=1200,
    category="groceries",
    description="Monthly groceries"
)
```

---

## 6.2 Get Expenses Tool

Retrieves expenses from SQLite.

Possible filters:

- Today
- This week
- This month
- Specific category
- Custom date range

Example:

```python
get_expenses(
    start_date="2026-08-01",
    end_date="2026-08-31"
)
```

---

## 6.3 Calculator Tool

Used for calculations such as:

- Total spending
- Category percentages
- Remaining budget
- Average daily spending

Example:

```python
calculate_total([1200, 800, 2500])
```

---

## 6.4 Budget Tool

Compares current spending against the user's budget.

Example:

```text
Monthly Budget: Rs. 40,000
Current Spending: Rs. 32,000
Remaining: Rs. 8,000
```

The agent can then explain the result in natural language.

---

# 7. Database Design

SQLite can be used because the project is small and does not require a complex database server.

## Expenses Table

```sql
CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    date TEXT NOT NULL
);
```

## Example Data

| id | amount | category | description | date |
|---:|---:|---|---|---|
| 1 | 1200 | groceries | Monthly groceries | 2026-08-10 |
| 2 | 700 | transport | Uber | 2026-08-10 |
| 3 | 2500 | shopping | Clothes | 2026-08-09 |

---

# 8. Expense Categories

Initial categories can be:

- Food
- Groceries
- Transport
- Shopping
- Bills
- Entertainment
- Health
- Education
- Other

The LLM can also classify a natural-language expense into one of these categories.

Example:

> "I spent 850 on pizza."

Agent classification:

```text
Category = Food
Amount = 850
```

---

# 9. Example Agent Decisions

### Case 1

**User:**

> I spent 500 on lunch.

Agent decision:

```text
Intent: Add expense
Tool: add_expense
```

---

### Case 2

**User:**

> What did I spend on food this month?

Agent decision:

```text
Intent: Retrieve expenses
Tool: get_expenses
Filter: food + current month
```

---

### Case 3

**User:**

> What percentage of my spending went to shopping?

Agent decision:

```text
Intent: Analysis
Tools:
1. get_expenses
2. calculator
```

---

### Case 4

**User:**

> I have a Rs. 40,000 budget. How much can I still spend?

Agent decision:

```text
Intent: Budget check
Tools:
1. get_expenses
2. budget/calculator
```

---

# 10. Agent vs Normal Chatbot

A normal chatbot might only respond:

```text
User
  ↓
LLM
  ↓
Answer
```

This project uses:

```text
User
  ↓
LLM Agent
  ↓
Decision
  ↓
Tool
  ↓
Database / Calculation
  ↓
Tool Result
  ↓
LLM
  ↓
Final Answer
```

The important difference is that the agent can **take actions and use external capabilities**.

---

# 11. ReAct / Agent Loop

The project can conceptually follow a ReAct-style loop:

```text
Reason
  ↓
Choose Action
  ↓
Execute Tool
  ↓
Observe Result
  ↓
Reason Again
  ↓
Final Answer
```

The application should not expose private chain-of-thought. Instead, the implementation can log safe high-level events such as:

```text
Selected tool: get_expenses
Tool completed successfully
Retrieved 12 expense records
```

---

# 12. Suggested Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| LLM | Ollama/Qwen or an API-based LLM |
| Agent Logic | Python + tool/function calling |
| Database | SQLite |
| API | FastAPI (optional) |
| Frontend | HTML/CSS/JavaScript (optional) |
| Environment | Python virtual environment |
| Version Control | Git/GitHub |

For the first version, a **terminal/CLI application** is recommended. A web UI can be added after the agent works correctly.

---

# 13. Project Structure

```text
personal-expense-advisor/
│
├── main.py
├── agent.py
├── tools.py
├── database.py
├── prompts.py
├── requirements.txt
├── .env
├── README.md
│
└── data/
    └── expenses.db
```

## File Responsibilities

### `main.py`

Application entry point.

Responsibilities:

- Start the application
- Receive user input
- Send input to the agent
- Display the response

### `agent.py`

Contains the main agent logic.

Responsibilities:

- Configure the LLM
- Register tools
- Handle tool calls
- Return final responses

### `tools.py`

Contains functions available to the agent.

Example:

```python
add_expense()
get_expenses()
calculate_total()
check_budget()
```

### `database.py`

Handles SQLite operations.

Responsibilities:

- Create database
- Create tables
- Insert expenses
- Retrieve expenses
- Update/delete records if required

### `prompts.py`

Contains the system prompt and agent instructions.

Example instructions:

```text
You are a personal expense advisor.

Use tools when the user asks about stored expenses,
calculations, budgets, or expense records.

Never invent expense data.
Use database results for financial summaries.
```

---

# 14. Development Phases

## Phase 1 — Database

Build:

- SQLite connection
- Expenses table
- Add expense
- Get expenses

Goal:

```text
Python → SQLite → Store/Retrieve Expenses
```

---

## Phase 2 — Basic Tools

Create:

```text
add_expense()
get_expenses()
calculate_total()
check_budget()
```

Test every tool independently before connecting them to the LLM.

---

## Phase 3 — LLM Integration

Connect the LLM.

Basic flow:

```text
User Input
   ↓
LLM
   ↓
Response
```

At this stage, the LLM can understand natural language but cannot yet perform actions.

---

## Phase 4 — Tool Calling

Register the tools with the LLM.

Flow:

```text
User
 ↓
LLM
 ↓
Tool Call
 ↓
Python Function
 ↓
Tool Result
 ↓
LLM
 ↓
Response
```

This is the point where the application starts behaving like an AI agent.

---

## Phase 5 — Agent Intelligence

Add:

- Intent understanding
- Automatic category detection
- Budget comparison
- Spending analysis
- Multiple tool calls
- Natural-language responses

---

## Phase 6 — Optional UI

After the CLI version works, add a simple web interface.

Possible UI:

```text
+--------------------------------------+
|       Personal Expense Advisor       |
+--------------------------------------+
|                                      |
|  "I spent 1200 on groceries today"   |
|                                      |
|              [ Send ]                |
|                                      |
+--------------------------------------+
| Monthly Spending                     |
| Rs. 32,500                           |
|                                      |
| Food       Rs. 10,000                |
| Shopping   Rs. 12,000                |
| Transport  Rs.  5,500                |
| Bills      Rs.  5,000                |
+--------------------------------------+
```

---

# 15. Future Features

Once the basic agent is complete, optional improvements include:

### Spending Alerts

```text
You have used 85% of your monthly budget.
```

### Monthly Reports

```text
August Spending Summary

Total: Rs. 35,400

Highest Category:
Shopping — Rs. 12,500
```

### Savings Suggestions

```text
Your shopping expenses increased by 25%
compared with last month.
```

### Recurring Expenses

Detect:

- Rent
- Internet
- Subscriptions
- Utility bills

### Expense Trends

Compare:

```text
This month vs last month
```

### Natural Language Queries

Support questions such as:

```text
"How much did I spend last week?"

"Where am I spending the most?"

"Show my food expenses."

"Can I afford to spend Rs. 5,000 today?"

"Which category increased the most?"
```

---

# 16. Important Scope Limitation

This project is a **personal budgeting assistant**, not a professional financial advisor.

The agent should:

- Work with the user's stored expense data.
- Clearly distinguish calculations from recommendations.
- Avoid making claims about investments, loans, or regulated financial products.
- Never invent missing financial data.

---

# 17. Learning Outcomes

By completing this project, you will understand:

- What an AI agent is
- LLM integration
- Prompt engineering
- Tool calling
- Function calling
- Agent loops
- ReAct concepts
- SQLite
- Database CRUD operations
- Natural-language intent handling
- Basic data analysis
- Building an AI-powered application

---

# 18. Final Project Flow

```text
                    USER
                      |
                      v
                Natural Language
                      |
                      v
               +-------------+
               | AI AGENT    |
               |    LLM      |
               +------+------+
                      |
              Tool Selection
                      |
        +-------------+-------------+
        |             |             |
        v             v             v
  Add Expense   Get Expenses   Calculator
        |             |             |
        +-------------+-------------+
                      |
                      v
                SQLite Database
                      |
                      v
                  Tool Result
                      |
                      v
                     LLM
                      |
                      v
              Personalized Advice
                      |
                      v
                 FINAL RESPONSE
```

# 19. MVP Definition

The **minimum viable version** should contain only:

1. Add expense through natural language.
2. Store expense in SQLite.
3. Retrieve expenses.
4. Calculate total spending.
5. Check a monthly budget.
6. Use LLM tool/function calling.
7. Generate a natural-language response.

Do **not** start with charts, authentication, complex dashboards, multi-agent systems, or RAG. Add those only after the single-agent workflow is working correctly.

---

## Portfolio Description

> **Personal Expense Advisor Agent** — Built a single AI agent that uses LLM-based tool calling to record and retrieve personal expenses, perform spending calculations, compare expenses against budgets, and provide personalized budgeting insights using Python and SQLite.

---

# Phase 6 — Optional UI (Complete Implementation Guide)

## 6.1 UI Technology Stack

**Recommended Stack:**
- **Backend:** FastAPI (Python)
- **Frontend:** HTML/CSS/JavaScript (Vanilla or React)
- **Database:** SQLite (same as CLI)
- **API Communication:** REST endpoints
- **Styling:** CSS Framework (Bootstrap or Tailwind)

## 6.2 Project Structure with UI

```text
personal-expense-advisor/
├── main.py              # CLI entry point
├── agent.py             # Agent logic
├── tools.py             # Tool functions
├── database.py          # SQLite operations
├── prompts.py           # System prompts
├── app.py               # FastAPI application
├── requirements.txt     # Dependencies
├── .env                 # Environment variables
├── README.md            # Documentation
├── static/              # Static files
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│   └── images/
├── templates/           # HTML templates
│   ├── index.html
│   ├── dashboard.html
│   └── history.html
└── data/
    └── expenses.db      # SQLite database
```

## 6.3 FastAPI Application Structure

```python
# app.py
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from agent import get_agent
from pydantic import BaseModel

app = FastAPI(title="Personal Expense Advisor")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

agent = get_agent()

class ExpenseRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def chat(request: ExpenseRequest):
    """Process user message and return agent response."""
    try:
        response = agent.process_message(request.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def home(request):
    """Render the main interface."""
    return templates.TemplateResponse("index.html", {"request": request})
```

## 6.4 Frontend Implementation

**HTML Structure (index.html):**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Personal Expense Advisor</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>💰 Personal Expense Advisor</h1>
            <p>Track, analyze, and understand your expenses</p>
        </header>

        <main>
            <div class="chat-section">
                <div class="chat-messages" id="chatMessages">
                    <div class="message agent">
                        <p>Hello! I'm your Personal Expense Advisor. Tell me about your expenses or ask for spending analysis.</p>
                    </div>
                </div>

                <div class="input-section">
                    <input
                        type="text"
                        id="userInput"
                        placeholder="e.g., 'I spent 500 on lunch today'"
                        autocomplete="off"
                    >
                    <button id="sendBtn">Send</button>
                </div>
            </div>

            <div class="dashboard-section">
                <div class="stat-card">
                    <h3>This Month</h3>
                    <p class="stat-value" id="monthlyTotal">Rs. 0</p>
                </div>
                <div class="stat-card">
                    <h3>Today</h3>
                    <p class="stat-value" id="todayTotal">Rs. 0</p>
                </div>
                <div class="stat-card">
                    <h3>Budget Status</h3>
                    <p class="stat-value" id="budgetStatus">Healthy</p>
                </div>
            </div>
        </main>
    </div>

    <script src="/static/js/app.js"></script>
</body>
</html>
```

**JavaScript Logic (app.js):**

```javascript
class ExpenseAdvisor {
    constructor() {
        this.chatMessages = document.getElementById('chatMessages');
        this.userInput = document.getElementById('userInput');
        this.sendBtn = document.getElementById('sendBtn');

        this.setupEventListeners();
        this.loadDashboard();
    }

    setupEventListeners() {
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        this.userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });
    }

    async sendMessage() {
        const message = this.userInput.value.trim();
        if (!message) return;

        // Add user message to chat
        this.addMessage(message, 'user');
        this.userInput.value = '';

        // Show loading indicator
        this.addLoadingIndicator();

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });

            const data = await response.json();

            // Remove loading indicator
            this.removeLoadingIndicator();

            // Add agent response
            this.addMessage(data.response, 'agent');

            // Update dashboard
            this.loadDashboard();
        } catch (error) {
            this.removeLoadingIndicator();
            this.addMessage('Sorry, something went wrong. Please try again.', 'agent');
        }
    }

    addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        messageDiv.innerHTML = `<p>${text}</p>`;
        this.chatMessages.appendChild(messageDiv);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    addLoadingIndicator() {
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'message agent loading';
        loadingDiv.id = 'loadingIndicator';
        loadingDiv.innerHTML = '<p>Thinking...</p>';
        this.chatMessages.appendChild(loadingDiv);
    }

    removeLoadingIndicator() {
        const loading = document.getElementById('loadingIndicator');
        if (loading) loading.remove();
    }

    async loadDashboard() {
        // Fetch dashboard data and update UI
        // This would call additional API endpoints
    }
}

// Initialize the app
document.addEventListener('DOMContentLoaded', () => {
    new ExpenseAdvisor();
});
```

**CSS Styling (style.css):**

```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    padding: 20px;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    background: white;
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    overflow: hidden;
}

header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 30px;
    text-align: center;
}

header h1 {
    font-size: 2.5em;
    margin-bottom: 10px;
}

.chat-section {
    padding: 30px;
    border-bottom: 1px solid #eee;
}

.chat-messages {
    height: 400px;
    overflow-y: auto;
    margin-bottom: 20px;
    padding: 15px;
    background: #f8f9fa;
    border-radius: 10px;
}

.message {
    margin-bottom: 15px;
    padding: 12px 18px;
    border-radius: 10px;
    max-width: 80%;
}

.message.user {
    background: #667eea;
    color: white;
    margin-left: auto;
}

.message.agent {
    background: #e9ecef;
    color: #333;
}

.message.loading {
    opacity: 0.7;
}

.input-section {
    display: flex;
    gap: 10px;
}

.input-section input {
    flex: 1;
    padding: 15px;
    border: 2px solid #ddd;
    border-radius: 8px;
    font-size: 16px;
}

.input-section button {
    padding: 15px 30px;
    background: #667eea;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 16px;
    transition: background 0.3s;
}

.input-section button:hover {
    background: #5568d3;
}

.dashboard-section {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    padding: 30px;
}

.stat-card {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
    padding: 25px;
    border-radius: 12px;
    text-align: center;
}

.stat-card:nth-child(2) {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.stat-card:nth-child(3) {
    background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.stat-card h3 {
    font-size: 1.2em;
    margin-bottom: 10px;
    opacity: 0.9;
}

.stat-value {
    font-size: 2em;
    font-weight: bold;
}
```

## 6.5 API Endpoints

**Additional Endpoints for Dashboard:**

```python
@app.get("/api/expenses/today")
async def get_today_expenses():
    """Get today's expenses."""
    from tools import get_expenses_today
    result = get_expenses_today()
    return result

@app.get("/api/expenses/month")
async def get_month_expenses():
    """Get this month's expenses."""
    from tools import get_expenses_this_month
    result = get_expenses_this_month()
    return result

@app.get("/api/budget/{budget_limit}")
async def check_budget_endpoint(budget_limit: float):
    """Check budget status."""
    from tools import check_budget
    result = check_budget(budget_limit)
    return result

@app.get("/api/analysis")
async def get_analysis():
    """Get spending analysis."""
    from tools import analyze_spending_patterns
    result = analyze_spending_patterns()
    return result
```

## 6.6 UI Features

**Chat Interface:**
- Real-time conversation with AI agent
- Message history
- Loading indicators
- Auto-scroll to latest messages
- Enter key to send

**Dashboard Features:**
- Real-time spending statistics
- Category breakdown charts
- Budget progress indicators
- Quick action buttons
- Expense history table

**Responsive Design:**
- Mobile-friendly layout
- Touch-optimized controls
- Adaptive grid layouts
- Optimized loading times

## 6.7 Deployment Options

**Local Development:**
```bash
# Install additional dependencies
pip install fastapi uvicorn jinja2 python-multipart

# Run the application
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

**Production Deployment:**
- **Render:** Easy deployment for Python apps
- **Railway:** Simple hosting with database
- **Heroku:** Established platform (requires paid dynos)
- **Vercel:** Great for frontend + API
- **DigitalOcean:** Full control over hosting

## 6.8 Advanced UI Features (Future Enhancements)

**Data Visualization:**
- Chart.js integration for spending graphs
- Pie charts for category breakdown
- Line charts for spending trends
- Bar charts for monthly comparisons

**User Authentication:**
- User registration/login
- Personal dashboards
- Data isolation between users
- Session management

**Export Features:**
- CSV export for expenses
- PDF report generation
- Email reports
- Data backup/restore

**Mobile App:**
- React Native implementation
- Push notifications for budget alerts
- Offline mode support
- Biometric authentication

## 6.9 Testing the UI

**Manual Testing Checklist:**
- [ ] Chat interface responds correctly
- [ ] Dashboard statistics update in real-time
- [ ] Mobile responsive design works
- [ ] Error handling displays user-friendly messages
- [ ] API endpoints return correct data
- [ ] Loading states display properly
- [ ] Enter key sends messages
- [ ] Long messages handle correctly

**Automated Testing:**
```python
# test_ui.py
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_chat_endpoint():
    response = client.post("/api/chat", json={"message": "I spent 500 on lunch"})
    assert response.status_code == 200
    assert "response" in response.json()

def test_expenses_endpoint():
    response = client.get("/api/expenses/today")
    assert response.status_code == 200
```

## 6.10 UI Mockup

**Complete Interface Layout:**

```text
+---------------------------------------------------------------+
|                    💰 Personal Expense Advisor               |
|                   Track your expenses intelligently            |
+---------------------------------------------------------------+
|                                                               |
|  +---------------------------------------------------------+  |
|  |                  Chat Interface                          |  |
|  |                                                         |  |
|  |  Agent: Hello! How can I help with your expenses?      |  |
|  |                                                         |  |
|  |  You: I spent 1200 on groceries today                   |  |
|  |                                                         |  |
|  |  Agent: Rs. 1,200.00 groceries expense recorded.       |  |
|  |          Your monthly total is now Rs. 15,200.          |  |
|  |                                                         |  |
|  +---------------------------------------------------------+  |
|  | [ I spent 500 on lunch today            ]      [ Send ] |  |
|  +---------------------------------------------------------+  |
|                                                               |
|  +-----------+  +-----------+  +-------------------------+  |
|  |   This    |  |   Today   |  |      Budget Status      |  |
|  |   Month   |  |           |  |                         |  |
|  | Rs.15,200 |  | Rs. 1,200 |  |        Healthy ✅         |  |
|  +-----------+  +-----------+  +-------------------------+  |
|                                                               |
|  +---------------------------------------------------------+  |
|  |                 Spending Breakdown                     |  |
|  |                                                         |  |
|  |  🛒 Groceries    Rs. 7,200  (47%)  ██████████░░░░      |  |
|  |  🍔 Food         Rs. 3,500  (23%)  ██████░░░░░░░░░░      |  |
|  |  🚗 Transport    Rs. 2,800  (18%)  █████░░░░░░░░░░░░     |  |
|  |  🛍️ Shopping     Rs. 1,700  (12%)  ██░░░░░░░░░░░░░░░     |  |
|  +---------------------------------------------------------+  |
|                                                               |
+---------------------------------------------------------------+
```

## 6.11 Phase 6 Completion Criteria

**Minimum Viable UI:**
- [ ] FastAPI backend running
- [ ] Basic chat interface working
- [ ] Real-time agent responses
- [ ] Dashboard with basic statistics
- [ ] Responsive design
- [ ] Error handling
- [ ] Local deployment successful

**Enhanced UI (Optional):**
- [ ] Data visualization charts
- [ ] User authentication
- [ ] Export functionality
- [ ] Mobile app version
- [ ] Production deployment
- [ ] Performance optimization
