# 🚀 Startup Research Agent System

A multi-agent AI system that discovers startups founded in the last month and analyzes their viability for implementation in India across Tier 1, 2, and 3 cities.

## 📋 Overview

This system uses CrewAI to orchestrate 4 specialized agents:

1. **Global Startup Discovery Agent** - Finds startups founded in the last 1 month globally
2. **India Market Fit Analyzer** - Analyzes viability for Indian market (0-100 score)
3. **Tier Categorization Agent** - Categorizes startups by city tier
4. **Report Generation Agent** - Creates comprehensive monthly summary reports

## 🏗️ Architecture

```
startup_research_agent/
├── src/
│   ├── agents/          # CrewAI agents
│   ├── tasks/           # CrewAI tasks
│   ├── tools/           # Search and utility tools
│   ├── database/        # SQLite database management
│   ├── config/          # Configuration settings
│   └── crew_orchestration.py  # Main crew orchestrator
├── main.py              # Entry point
├── .env                 # API keys (create from .env.example)
└── startup_research.db  # SQLite database (auto-created)
```

## 🛠️ Setup

### 1. Prerequisites
- Python 3.11+
- UV package manager (installed automatically)

### 2. Install Dependencies
```bash
cd startup_research_agent
uv sync
```

### 3. Configure API Keys
```bash
cp .env.example .env
# Edit .env and add your API keys:
# - OPENAI_API_KEY (required for CrewAI)
# - ANTHROPIC_API_KEY (for Claude models)
# - GOOGLE_API_KEY (for Google Search)
# - GOOGLE_SEARCH_ENGINE_ID (for Google Search)
```

### 4. Initialize Database
```bash
python src/database/db.py
```

## 🚀 Running the System

### Run the complete workflow:
```bash
python main.py
```

### Run individual components:
```bash
# Test database
python src/database/db.py

# Test configuration
python src/config/settings.py

# Test agents
python -m src.agents.crew_agents

# Test crew orchestration
python -m src.crew_orchestration
```

## 📊 Database Schema

### startups table
- `id` - Primary key
- `name` - Startup name
- `website` - Website URL
- `description` - Startup description
- `category` - Business category
- `founded_date` - Founding date
- `country` - Country of origin
- `india_fit_score` - India viability score (0-100)
- `india_fit_analysis` - Detailed analysis
- `primary_tier` - Primary market tier (Tier 1/2/3)
- `secondary_tiers` - Alternative market tiers
- `source` - Data source
- `source_url` - Source URL
- `hash` - Deduplication hash

### run_metadata table
- `run_id` - Unique run identifier
- `run_date` - Execution date
- `total_startups_found` - Count of startups
- `tier_1_count` - Tier 1 startups
- `tier_2_count` - Tier 2 startups
- `tier_3_count` - Tier 3 startups
- `processing_time_seconds` - Execution time
- `status` - Run status
- `report_path` - Report file path

### knowledge_base table
- `key` - Knowledge key
- `value` - Knowledge value
- `category` - Knowledge category

## 🎯 City Tiers

**Tier 1 Cities**: Delhi, Mumbai, Bangalore
**Tier 2 Cities**: Pune, Hyderabad, Chennai
**Tier 3 Cities**: Jaipur, Lucknow, Chandigarh, Ahmedabad, Kolkata

## 🔑 API Keys Required

1. **OpenAI API Key** (Required)
   - Get from: https://platform.openai.com/account/api-keys
   - Used for: CrewAI agent execution

2. **Anthropic API Key** (Optional)
   - Get from: https://console.anthropic.com
   - Used for: Claude models (faster, cheaper)

3. **Google Search API** (Optional)
   - Get from: https://programmablesearchengine.google.com
   - Used for: Startup discovery

## 📈 Output

The system generates:
- **JSON Report** - Structured startup data with analysis
- **Database Records** - Persistent storage in SQLite
- **Run Metadata** - Execution statistics and tracking

## 🧪 Testing

### Test Database
```bash
python src/database/db.py
# Expected: ✅ Database initialized successfully
```

### Test Configuration
```bash
python src/config/settings.py
# Expected: ✅ Configuration loaded successfully
```

### Test Agents
```bash
python -m src.agents.crew_agents
# Expected: ✅ Created [Agent Name]
```

### Test Full Workflow
```bash
python main.py
# Expected: Complete crew execution with results
```

## 📝 Configuration

Edit `src/config/settings.py` to customize:
- LLM models (fast vs smart)
- Search parameters
- Database path
- Output directory
- Logging level

## 🔄 Workflow

1. **Discovery** - Search for startups globally
2. **Analysis** - Evaluate India market fit
3. **Categorization** - Assign city tiers
4. **Reporting** - Generate summary report

## 📚 Documentation

- `MASTER_IMPLEMENTATION_GUIDE.md` - Complete implementation details
- `QUICK_REFERENCE.md` - Quick start guide
- `TOOLS_RESEARCH_AND_MCP_GUIDE.md` - Tools and MCP integration

## 🐛 Troubleshooting

### "OPENAI_API_KEY is required"
- Add your OpenAI API key to `.env` file

### "ModuleNotFoundError: No module named 'src'"
- Run from the `startup_research_agent` directory
- Use `python -m` for module execution

### Database errors
- Delete `startup_research.db` and run `python src/database/db.py`

## 📞 Support

For issues or questions, refer to the documentation files in the project root.

## 📄 License

This project is part of the Startup Research Agent System.

---

**Status**: ✅ Ready for Development  
**Last Updated**: 2024-11-02  
**Version**: 1.0

