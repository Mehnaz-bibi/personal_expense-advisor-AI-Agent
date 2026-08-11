/**
 * Personal Expense Advisor - Frontend JavaScript
 * Handles chat interface, API communication, and dashboard updates
 */

class ExpenseAdvisor {
    constructor() {
        this.chatMessages = document.getElementById('chatMessages');
        this.userInput = document.getElementById('userInput');
        this.sendBtn = document.getElementById('sendBtn');

        this.setupEventListeners();
        this.loadDashboard();
    }

    setupEventListeners() {
        // Send button click
        this.sendBtn.addEventListener('click', () => this.sendMessage());

        // Enter key to send
        this.userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });

        // Auto-refresh dashboard every 30 seconds
        setInterval(() => this.loadDashboard(), 30000);
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
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message })
            });

            const data = await response.json();

            // Remove loading indicator
            this.removeLoadingIndicator();

            if (data.success) {
                // Add agent response
                this.addMessage(data.response, 'agent');

                // Update dashboard after a short delay
                setTimeout(() => this.loadDashboard(), 500);
            } else {
                this.addMessage(`Error: ${data.error}`, 'agent');
            }
        } catch (error) {
            this.removeLoadingIndicator();
            this.addMessage('Sorry, something went wrong. Please try again.', 'agent');
            console.error('Error:', error);
        }
    }

    addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;

        // Handle multi-line text
        const formattedText = text
            .replace(/\n/g, '<br>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>');

        messageDiv.innerHTML = `<p>${formattedText}</p>`;
        this.chatMessages.appendChild(messageDiv);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    addLoadingIndicator() {
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'message agent loading';
        loadingDiv.id = 'loadingIndicator';
        loadingDiv.innerHTML = '<p class="loading-dots">Thinking</p>';
        this.chatMessages.appendChild(loadingDiv);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    removeLoadingIndicator() {
        const loading = document.getElementById('loadingIndicator');
        if (loading) loading.remove();
    }

    async loadDashboard() {
        try {
            // Fetch today's expenses
            const todayResponse = await fetch('/api/expenses/today');
            const todayData = await todayResponse.json();

            if (todayData.success) {
                document.getElementById('todayTotal').textContent =
                    `Rs. ${todayData.data.total.toLocaleString()}`;
                document.getElementById('todayCount').textContent =
                    `${todayData.data.count} expenses`;
            }

            // Fetch month's expenses
            const monthResponse = await fetch('/api/expenses/month');
            const monthData = await monthResponse.json();

            if (monthData.success) {
                document.getElementById('monthlyTotal').textContent =
                    `Rs. ${monthData.data.total.toLocaleString()}`;
                document.getElementById('monthlyCount').textContent =
                    `${monthData.data.count} expenses`;
            }

            // Budget status will be updated when user sets budget
            // For now, show a default message
            document.getElementById('budgetStatus').textContent = 'Set Budget';
            document.getElementById('budgetPercentage').textContent = 'Check your spending';

        } catch (error) {
            console.error('Error loading dashboard:', error);
        }
    }

    async checkBudget(budgetLimit) {
        try {
            const response = await fetch('/api/budget', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ budget_limit: budgetLimit })
            });

            const data = await response.json();

            if (data.success) {
                const budgetData = data.data;
                document.getElementById('budgetStatus').textContent = budgetData.status;
                document.getElementById('budgetPercentage').textContent =
                    `${budgetData.percentage_used.toFixed(1)}% used`;

                // Add budget info to chat
                this.addMessage(
                    `Budget Check: ${budgetData.message}`,
                    'agent'
                );
            }
        } catch (error) {
            console.error('Error checking budget:', error);
        }
    }
}

// Quick action function
function quickAction(message) {
    const advisor = window.expenseAdvisor;
    if (advisor) {
        advisor.userInput.value = message;
        advisor.sendMessage();
    }
}

// Initialize the app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.expenseAdvisor = new ExpenseAdvisor();
    console.log('Personal Expense Advisor initialized');
});

// Handle page visibility changes to refresh dashboard
document.addEventListener('visibilitychange', () => {
    if (!document.hidden && window.expenseAdvisor) {
        window.expenseAdvisor.loadDashboard();
    }
});
