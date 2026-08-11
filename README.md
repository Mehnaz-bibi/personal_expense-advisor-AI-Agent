# Personal Expense Advisor Agent

A single AI agent that helps users record, analyze, and understand their personal expenses using natural language. Built with Python, SQLite, and intelligent tool calling.

## 🎯 Features

- **Natural Language Input**: Add expenses using everyday language (e.g., "I spent 500 on lunch")
- **Automatic Categorization**: Expenses are automatically categorized into relevant groups
- **Spending Analysis**: Get insights into your spending patterns and trends
- **Budget Tracking**: Check your spending against budget limits
- **Personalized Suggestions**: Receive tailored advice based on your spending habits
- **Database Storage**: All expenses are stored in a local SQLite database
- **CLI Interface**: Simple command-line interface for easy interaction

## 📋 Requirements

- Python 3.7 or higher
- SQLite (included with Python)
- python-dotenv

## 🚀 Installation

1. **Clone or download the project**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   Edit the `.env` file to set your preferences:
   ```env
   LLM_PROVIDER=ollama
   OLLAMA_MODEL=qwen2.5:7b
   DATABASE_PATH=data/expenses.db
   ```

## 📁 Project Structure

```
personal-expense-advisor/
├── main.py              # CLI application entry point
├── app.py               # FastAPI web application
├── agent.py             # Agent logic and tool calling
├── tools.py             # Tool functions (add_expense, get_expenses, etc.)
├── database.py          # SQLite database operations
├── prompts.py           # System prompts and agent instructions
├── requirements.txt     # Python dependencies
├── .env                 # Environment configuration
├── demo.py              # Demo script
├── test_tools.py        # Tool testing script
├── test_agent.py        # Agent testing script
├── test_web.py          # Web API testing script
├── README.md            # This file
├── static/              # Static files for web UI
│   ├── css/
│   │   └── style.css    # Styling
│   └── js/
│       └── app.js       # Frontend JavaScript
├── templates/           # HTML templates
│   └── index.html       # Main web interface
└── data/
    └── expenses.db      # SQLite database (created automatically)
```

## 🎮 Usage

### Option 1: Web UI (Recommended)

**First time setup:**
```bash
python init_db.py
```

**Run the web interface:**
```bash
python app.py
```

The application will automatically find an available port and display the URL.
Then open your browser to the displayed URL (usually `http://localhost:8000` or `http://localhost:8001`)

**Web UI Features:**
- Beautiful chat interface with AI agent
- Real-time dashboard with spending statistics
- Quick action buttons for common tasks
- Responsive design for mobile and desktop
- Auto-refreshing dashboard

### Option 2: CLI Application

Run the CLI application for terminal use:
```bash
python main.py
```

**Note**: The CLI requires interactive terminal input.

### Option 3: Quick Demo

Run the demo to see sample conversations:
```bash
python demo.py
```

### Example Conversations

**Adding an Expense**
```
You: I spent 1200 on groceries today
Agent: Rs. 1,200.00 groceries expense has been recorded.
```

**Checking Spending**
```
You: How much did I spend this month?
Agent: You've spent Rs. 2,550.00 this month across 3 expense(s).
```

**Budget Check**
```
You: My budget is 40000
Agent: You are within budget. Rs. 37,450.00 remaining (6.4% used).
```

**Spending Analysis**
```
You: Where am I spending the most?
Agent: Here's your spending analysis for this month:

Total spending: Rs. 2,550.00
Number of expenses: 3
Average daily spending: Rs. 231.82

Highest spending category: groceries (Rs. 1,200.00, 47.1% of total)
```

**Getting Suggestions**
```
You: Give me some suggestions
Agent: Here are some suggestions based on your spending:

1. Your spending on groceries is 47.1% of your total. Consider setting a specific budget for this category.
2. Based on your average daily spending of Rs. 231.82, you're projected to spend Rs. 6,954.60 this month.
3. You have very few recorded expenses this month. Make sure to track all your spending.
```

## 🏷️ Expense Categories

The agent automatically categorizes expenses into these categories:

- **Food** - Restaurant meals, lunch, dinner, snacks
- **Groceries** - Supermarket, vegetables, fruits
- **Transport** - Uber, taxi, bus, petrol, travel
- **Shopping** - Clothes, shoes, electronics
- **Bills** - Electricity, water, internet, phone, rent
- **Entertainment** - Movies, games, concerts
- **Health** - Doctor, medicine, pharmacy
- **Education** - Books, courses, tuition
- **Other** - Anything else

## 🧪 Testing

### Test Web API
```bash
# Start the server first
python app.py

# In another terminal, test the API
python test_web.py
```

### Run Demo
```bash
python demo.py
```
This shows a complete working conversation with all features.

### Test Individual Tools
```bash
python test_tools.py
```
This will test all database operations and tool functions.

### Test Agent Conversations
```bash
python test_agent.py
```
This will run sample conversations through the agent.

## 🔧 Available Commands

In the CLI, you can use:

- **Add expenses**: "I spent 500 on lunch"
- **Check spending**: "How much did I spend this month?"
- **Budget check**: "My budget is 40000"
- **Analysis**: "Where am I spending the most?"
- **Suggestions**: "Give me some money-saving tips"
- **Help**: Type "help" or "?"
- **Exit**: Type "exit" or "quit"

## 🛠️ How It Works

The agent follows a ReAct-style loop:

1. **User Input** → Receives natural language message
2. **Intent Understanding** → Analyzes what the user wants to do
3. **Tool Selection** → Chooses the appropriate tool(s)
4. **Tool Execution** → Calls the tool function
5. **Result Processing** → Analyzes the tool result
6. **Response Generation** → Creates a natural language response

### Available Tools

- `add_expense()` - Store new expenses
- `get_expenses()` - Retrieve expenses with filters
- `get_expenses_today()` - Get today's expenses
- `get_expenses_this_month()` - Get this month's expenses
- `calculate_total()` - Calculate totals from expense lists
- `check_budget()` - Compare spending against budget
- `analyze_spending_patterns()` - Analyze spending trends
- `get_spending_suggestions()` - Generate personalized advice

## 🔮 Future Enhancements

Potential improvements for future versions:

- **Web Interface**: Add a simple web UI
- **Spending Alerts**: Notify when approaching budget limits
- **Monthly Reports**: Generate detailed monthly summaries
- **Recurring Expenses**: Track regular payments
- **Expense Trends**: Compare month-over-month spending
- **Advanced Natural Language**: Better intent understanding with LLM integration
- **Data Export**: Export data to CSV or other formats
- **Multiple Budgets**: Support for different budget categories

## 📝 Development Phases

The project was developed in phases:

1. **Phase 1**: Database setup and basic operations
2. **Phase 2**: Core tool implementation
3. **Phase 3**: LLM integration foundation
4. **Phase 4**: Agent logic and tool calling
5. **Phase 5**: Intelligence and natural language processing
6. **Phase 6**: CLI application and testing

## 🎓 Learning Outcomes

This project demonstrates:
- AI agent architecture
- Tool/function calling patterns
- SQLite database integration
- Natural language processing basics
- ReAct-style agent loops
- CLI application development
- Expense tracking algorithms

## ⚠️ Important Notes

- This is a **personal budgeting assistant**, not a professional financial advisor
- The agent works with your stored expense data only
- Always backup your `expenses.db` file regularly
- The current implementation uses rule-based pattern matching (can be enhanced with LLM integration)

## 🤝 Contributing

This is a learning project. Feel free to:
- Report issues
- Suggest improvements
- Add new features
- Improve documentation

## 📄 License

This project is for educational purposes.

## 🙏 Acknowledgments

Built as a learning project to understand AI agent development, tool calling, and practical implementation of LLM-powered applications.

---

**Status**: ✅ MVP Complete - All core features implemented and tested
