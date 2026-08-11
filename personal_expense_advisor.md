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
