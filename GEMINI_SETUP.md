# Gemini API Setup Guide

## 🔑 Get Your Free Gemini API Key

### Step 1: Create Google AI Studio Account
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key" button
4. Copy your API key (it looks like: `AIzaSy...`)

### Step 2: Configure Your Project
1. Open the `.env` file in your project
2. Replace `your_gemini_api_key_here` with your actual API key:

```env
GEMINI_API_KEY=AIzaSyYourActualApiKeyHere
```

### Step 3: Verify Installation
The required package is already installed:
```bash
google-generativeai>=0.3.0  # ✅ Already installed
```

## 🚀 Start Using Gemini

### Quick Test
Run the demo to test Gemini integration:
```bash
python demo.py
```

### Interactive Mode
```bash
python main.py
```

## 📊 Gemini Free Tier Details

**Model:** `gemini-1.5-flash` (Free tier)

**Free Tier Limits:**
- 15 requests per minute
- 1,500 requests per day
- Great for development and testing

**Why Gemini 1.5 Flash?**
- Fast response times
- Good for text generation
- Free tier available
- Works well for expense tracking

## 🔧 Configuration Options

### Using Different Gemini Models
Edit `.env` to change models:

```env
# For faster responses (free tier)
GEMINI_MODEL=gemini-1.5-flash

# For more complex tasks (may have costs)
GEMINI_MODEL=gemini-1.5-pro
```

### Fallback to Rule-Based Mode
If API key is not set or API fails, the app automatically falls back to rule-based mode (still works perfectly!).

## 🎯 Current Status

✅ **Gemini Integration:** Added to agent.py
✅ **Package Installed:** google-generativeai ready
✅ **Configuration:** .env file updated
✅ **Fallback System:** Rule-based mode as backup
✅ **Error Handling:** Graceful degradation

## 📝 Example Usage

Once configured, the agent will use Gemini for:
- Better natural language understanding
- More intelligent categorization
- Improved conversation flow
- Smarter expense analysis

### Example Conversation with Gemini:
```
You: I spent 500 on lunch at the new Italian restaurant
Agent: I've recorded Rs. 500.00 for food (lunch at Italian restaurant).
       Would you like me to track how often you eat out?

You: Yes, that would be helpful
Agent: I'll monitor your restaurant spending patterns and alert you
       if it exceeds your usual budget.
```

## 🛠️ Troubleshooting

### Issue: "GEMINI_API_KEY not set"
**Solution:** Add your API key to `.env` file

### Issue: "Quota exceeded"
**Solution:** Wait a few minutes or upgrade to paid tier

### Issue: "API connection error"
**Solution:** Check internet connection; app will use rule-based mode

### Issue: "Model not found"
**Solution:** Ensure model name is correct in `.env` (gemini-1.5-flash)

## 🔄 Switching Back to Rule-Based Mode

If you want to disable Gemini temporarily:

```env
LLM_PROVIDER=rule-based
```

Or simply remove/comment the API key:
```env
# GEMINI_API_KEY=your_gemini_api_key_here
```

## 📚 Additional Resources

- [Google AI Studio Documentation](https://ai.google.dev/docs)
- [Gemini API Reference](https://ai.google.dev/docs/api_quickstart)
- [Pricing Information](https://ai.google.dev/pricing)

---

**Ready to use your free Gemini API!** 🚀
