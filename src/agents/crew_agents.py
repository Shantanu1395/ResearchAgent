"""CrewAI agents for startup research."""

import logging
from crewai import Agent
from ..config.settings import LLM_MODEL_SMART, LLM_MODEL_FAST
from ..tools.crew_tools import (
    search_recent_startups_tool,
    search_google_tool,
    search_product_hunt_tool,
    fetch_url_content_tool
)

logger = logging.getLogger(__name__)


def create_discovery_agent() -> Agent:
    """Create the startup discovery agent."""
    return Agent(
        role="Global Startup Discovery Agent",
        goal="Find and research startups founded in the last 1 month globally",
        backstory="""You are an expert startup researcher with access to multiple sources.
        You excel at finding new startups, extracting key information, and organizing data.
        You use multiple search strategies to ensure comprehensive coverage.""",
        tools=[
            search_recent_startups_tool,
            search_google_tool,
            search_product_hunt_tool,
            fetch_url_content_tool
        ],
        model=LLM_MODEL_SMART,
        verbose=True,
        memory=True
    )


def create_market_fit_agent() -> Agent:
    """Create the India market fit analyzer agent."""
    return Agent(
        role="India Market Fit Analyzer",
        goal="Analyze startups for their viability and fit in the Indian market",
        backstory="""You are an expert in Indian market dynamics, business models, and startup ecosystems.
        You understand regulatory environments, cultural nuances, and market opportunities in India.
        You provide detailed analysis with scores and recommendations.""",
        tools=[
            search_google_tool,
            fetch_url_content_tool
        ],
        model=LLM_MODEL_SMART,
        verbose=True,
        memory=True
    )


def create_tier_agent() -> Agent:
    """Create the tier categorization agent."""
    return Agent(
        role="Tier Categorization Agent",
        goal="Categorize startups by Indian city tiers (Tier 1, 2, 3)",
        backstory="""You are an expert in Indian geography, city infrastructure, and market dynamics.
        You understand the differences between Tier 1, 2, and 3 cities in India.
        You can categorize startups based on their business model and market fit.""",
        tools=[
            search_google_tool,
            fetch_url_content_tool
        ],
        model=LLM_MODEL_SMART,
        verbose=True,
        memory=True
    )


def create_report_agent() -> Agent:
    """Create the report generation agent."""
    return Agent(
        role="Report Generation Agent",
        goal="Generate comprehensive monthly summary reports",
        backstory="""You are an expert report writer and data analyst.
        You excel at synthesizing information, identifying trends, and providing actionable insights.
        You format reports in JSON for easy consumption and analysis.""",
        tools=[],
        model=LLM_MODEL_FAST,
        verbose=True,
        memory=True
    )

