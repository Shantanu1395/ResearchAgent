# 🚀 Setup Guide: Running on Another Laptop

This guide will help you set up and run the Startup Research Agent on a new laptop.

---

## 📋 Prerequisites

Before starting, ensure you have:
- ✅ Git installed
- ✅ Python 3.11+ installed
- ✅ Internet connection
- ✅ OpenAI API key
- ✅ (Optional) Google Search API key
- ✅ (Optional) Gmail App Password for email notifications

---

## 🔧 Step-by-Step Setup

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/Shantanu1395/ResearchAgent.git

# Navigate to the project directory
cd ResearchAgent/startup_research_agent
```

### Step 2: Install UV Package Manager

UV is a fast Python package manager. Install it:

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```bash
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Or using pip:**
```bash
pip install uv
```

Verify installation:
```bash
uv --version
```

### Step 3: Create .env File

Copy the example file and update with your credentials:

```bash
# Copy the example file
cp .env.example .env
```

Edit `.env` and add your credentials:

```bash
# Required: OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Google Search API (for better search results)
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id_here

# Optional: Email Notifications
ENABLE_EMAIL_NOTIFICATIONS=false
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password_here
EMAIL_RECIPIENTS=recipient@example.com
```

### Step 4: Install Dependencies

```bash
# Install all dependencies using UV
uv sync

# Or if you prefer pip
pip install -r requirements.txt
```

### Step 5: Verify Installation

```bash
# Check if all imports work
python -c "from src.crew_orchestration import CrewOrchestrator; print('✅ Installation successful!')"
```

### Step 6: Run the Project

```bash
# Run the startup research agent
uv run main.py

# Or using Python directly
python main.py
```

---

## 📊 Expected Output

When you run the project, you should see:

```
🚀 Starting Startup Research Agent...
📊 Running agents...
✅ Global Startup Discovery Agent completed
✅ India Market Fit Analyzer completed
✅ Tier Categorization Agent completed
✅ Report Generation Agent completed
📁 Reports saved to: reports/run_YYYYMMDD_HHMMSS/
✅ Process completed successfully!
```

---

## 📁 Project Structure

```
startup_research_agent/
├── main.py                 # Entry point
├── pyproject.toml         # Project configuration
├── .env                   # Environment variables (create this)
├── startup_research.db    # SQLite database (auto-created)
├── src/
│   ├── agents/           # CrewAI agents
│   ├── tasks/            # Agent tasks
│   ├── tools/            # Search and email tools
│   ├── config/           # Configuration
│   ├── database/         # Database operations
│   ├── models/           # Data models
│   └── utils/            # Utilities
├── reports/              # Generated reports (auto-created)
└── tests/                # Unit tests
```

---

## 🔑 Getting API Keys

### OpenAI API Key (Required)
1. Go to: https://platform.openai.com/api-keys
2. Sign up or log in
3. Create a new API key
4. Copy and paste into `.env`

### Google Search API (Optional)
1. Go to: https://console.cloud.google.com/
2. Create a new project
3. Enable Custom Search API
4. Create credentials (API key)
5. Create a Custom Search Engine: https://cse.google.com/cse/
6. Copy API key and Search Engine ID to `.env`

### Gmail App Password (Optional - for email notifications)
1. Go to: https://myaccount.google.com/apppasswords
2. Select "Mail" and "Windows Computer"
3. Generate 16-character password
4. Copy to `.env` as `EMAIL_PASSWORD`

---

## 🧪 Testing the Setup

### Test 1: Check Imports
```bash
python -c "import crewai; print('✅ CrewAI installed')"
```

### Test 2: Check Database
```bash
python -c "from src.database.db import get_all_startups; print(f'✅ Database ready: {len(get_all_startups())} startups')"
```

### Test 3: Check Configuration
```bash
python -c "from src.config.settings import OPENAI_API_KEY; print('✅ Configuration loaded')"
```

### Test 4: Run Full System
```bash
uv run main.py
```

---

## 🐛 Troubleshooting

### Issue: "uv: command not found"
**Solution**: Install UV or use pip instead
```bash
pip install uv
# Or use pip directly
pip install -r requirements.txt
```

### Issue: "ModuleNotFoundError: No module named 'crewai'"
**Solution**: Install dependencies
```bash
uv sync
# Or
pip install -r requirements.txt
```

### Issue: "OPENAI_API_KEY not found"
**Solution**: Create `.env` file with your API key
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### Issue: "429 Too Many Requests"
**Solution**: This is rate limiting. The system has built-in delays. Just wait and retry.

### Issue: "Email not sending"
**Solution**: 
1. Check `ENABLE_EMAIL_NOTIFICATIONS=true` in `.env`
2. Verify Gmail App Password (not regular password)
3. Check email configuration in `.env`

---

## 📊 Viewing Results

### View Generated Reports
```bash
# List all reports
ls -la reports/run_*/

# View latest report
cat reports/run_*/agents_summary.json | jq '.'
```

### View Database
```bash
# View all startups
sqlite3 startup_research.db "SELECT name, country, india_fit_score, primary_tier FROM startups LIMIT 10;"

# Count startups
sqlite3 startup_research.db "SELECT COUNT(*) as total FROM startups;"
```

### View Logs
```bash
# View application logs
tail -f logs/startup_research.log
```

---

## 🔄 Updating the Project

To get the latest updates from GitHub:

```bash
# Pull latest changes
git pull origin main

# Update dependencies
uv sync

# Run the project
uv run main.py
```

---

## 📝 Configuration Options

### Enable/Disable Features

**Email Notifications:**
```bash
ENABLE_EMAIL_NOTIFICATIONS=true  # or false
```

**Logging Level:**
```bash
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR
```

**Environment:**
```bash
ENVIRONMENT=development  # or production
```

---

## 🚀 Quick Start Summary

```bash
# 1. Clone repository
git clone https://github.com/Shantanu1395/ResearchAgent.git
cd ResearchAgent/startup_research_agent

# 2. Install UV (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. Create .env file
cp .env.example .env
# Edit .env with your API keys

# 4. Install dependencies
uv sync

# 5. Run the project
uv run main.py

# 6. Check results
cat reports/run_*/agents_summary.json | jq '.'
```

---

## 📞 Support

### Common Commands

```bash
# Run the project
uv run main.py

# Run tests
uv run pytest tests/

# Check Python version
python --version

# Check UV version
uv --version

# View help
uv --help
```

### Documentation Files

- **README.md** - Project overview
- **QUICK_EMAIL_SETUP.md** - Email configuration
- **EMAIL_NOTIFICATIONS_SETUP.md** - Email troubleshooting
- **IMPLEMENTATION_COMPLETE.md** - Feature summary

---

## ✅ Verification Checklist

- [ ] Git installed and repository cloned
- [ ] Python 3.11+ installed
- [ ] UV installed
- [ ] `.env` file created with API keys
- [ ] Dependencies installed (`uv sync`)
- [ ] Imports verified
- [ ] Database initialized
- [ ] First run completed successfully
- [ ] Reports generated in `reports/` folder
- [ ] Startups visible in database

---

## 🎉 You're Ready!

Once you've completed all steps, your Startup Research Agent is ready to use on your new laptop!

Run `uv run main.py` to start researching startups! 🚀

---

## 📚 Next Steps

1. **Configure Email** (optional): Follow `QUICK_EMAIL_SETUP.md`
2. **Customize Search**: Edit search queries in `src/tools/search_tools.py`
3. **Add More Agents**: Extend functionality in `src/agents/`
4. **Schedule Runs**: Use cron (Linux/Mac) or Task Scheduler (Windows)

Happy researching! 🚀

