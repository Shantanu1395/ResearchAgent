"""CrewAI tasks for startup research."""

import logging
from crewai import Task
from ..agents.crew_agents import (
    create_discovery_agent,
    create_market_fit_agent,
    create_tier_agent,
    create_report_agent
)

logger = logging.getLogger(__name__)


def create_discovery_task(agent) -> Task:
    """Create task for startup discovery."""
    return Task(
        description="""Search for startups founded in the last 1 month globally.
        Use multiple sources:
        1. Google Search for "startup founded last month"
        2. Product Hunt for recent launches
        3. AngelList for new startups
        4. GitHub for new tech projects

        For each startup found, extract:
        - Name
        - Website
        - Description
        - Category
        - Founded date
        - Country
        - Founder information

        Return a JSON array of at least 20 startups with complete information.
        Format: [{"name": "...", "website": "...", "description": "...", "category": "...", "founded_date": "...", "country": "...", "source": "..."}]""",
        expected_output="""A JSON array of startups with this exact format:
        [
            {
                "name": "Startup Name",
                "website": "https://example.com",
                "description": "2-3 sentence description",
                "category": "Category",
                "founded_date": "YYYY-MM-DD",
                "country": "Country",
                "source": "Source name"
            }
        ]
        Return ONLY valid JSON, no other text.""",
        agent=agent,
        async_execution=False
    )


def create_market_fit_task(agent) -> Task:
    """Create task for India market fit analysis."""
    return Task(
        description="""Analyze each startup for India market fit.
        For each startup, evaluate:
        1. Market demand in India (0-100)
        2. Competition landscape
        3. Regulatory environment
        4. Cultural fit
        5. Business model adaptability
        6. Potential barriers

        Provide a score from 0-100 where:
        - 80-100: Excellent fit
        - 60-79: Good fit
        - 40-59: Moderate fit
        - 0-39: Poor fit

        Return results as a JSON array with detailed analysis for each startup.""",
        expected_output="""Return a JSON array with this exact format:
        [
            {
                "name": "Startup Name",
                "india_fit_score": 75,
                "india_fit_analysis": "Detailed analysis of fit",
                "market_demand": "Assessment",
                "competition": "Analysis",
                "regulatory": "Considerations",
                "cultural_fit": "Analysis",
                "recommended_adaptations": "List of adaptations"
            }
        ]
        Return ONLY valid JSON, no other text.""",
        agent=agent,
        async_execution=False
    )


def create_tier_task(agent) -> Task:
    """Create task for tier categorization."""
    return Task(
        description="""Categorize each startup by city tier.

        Tier 1 Cities: Delhi, Mumbai, Bangalore
        Tier 2 Cities: Pune, Hyderabad, Chennai
        Tier 3 Cities: Jaipur, Lucknow, Chandigarh, Ahmedabad, Kolkata

        For each startup, determine:
        1. Primary tier (best market fit)
        2. Secondary tiers (alternative markets)
        3. Reasoning for categorization

        Consider:
        - Market size and growth
        - Infrastructure availability
        - Talent pool
        - Investor presence
        - Cost of operations

        Return results as a JSON array.""",
        expected_output="""Return a JSON array with this exact format:
        [
            {
                "name": "Startup Name",
                "primary_tier": "Tier 1",
                "secondary_tiers": ["Tier 2", "Tier 3"],
                "reasoning": "Detailed reasoning",
                "market_size_estimate": "Large/Medium/Small",
                "revenue_opportunity": "High/Medium/Low"
            }
        ]
        Return ONLY valid JSON, no other text.""",
        agent=agent,
        async_execution=False
    )


def create_report_task(agent) -> Task:
    """Create task for report generation."""
    return Task(
        description="""Generate a comprehensive monthly summary report.

        Include:
        1. Executive summary
        2. Total startups found
        3. Breakdown by tier:
           - Tier 1 count and top opportunities
           - Tier 2 count and top opportunities
           - Tier 3 count and top opportunities
        4. Market insights:
           - Trending categories
           - Market gaps
           - Opportunities
        5. Top 10 opportunities with details INCLUDING tier classification for each
        6. Recommendations

        IMPORTANT: For the top_opportunities array, include BOTH india_fit_score AND primary_tier for each startup.
        Format as JSON for easy consumption.""",
        expected_output="""A JSON report containing:
        - run_id
        - run_date
        - total_startups_found
        - by_tier breakdown
        - top_opportunities (top 10) - MUST include "primary_tier" field for each startup
        - market_insights
        - recommendations
        - generated_at timestamp

        Example top_opportunities format:
        [
            {
                "name": "Startup Name",
                "india_fit_score": 75,
                "primary_tier": "Tier 1",
                "secondary_tiers": ["Tier 2"],
                ...other fields...
            }
        ]""",
        agent=agent,
        async_execution=False
    )


def create_all_tasks():
    """Create all tasks."""
    discovery_agent = create_discovery_agent()
    market_fit_agent = create_market_fit_agent()
    tier_agent = create_tier_agent()
    report_agent = create_report_agent()
    
    tasks = [
        create_discovery_task(discovery_agent),
        create_market_fit_task(market_fit_agent),
        create_tier_task(tier_agent),
        create_report_task(report_agent)
    ]
    
    return tasks, [discovery_agent, market_fit_agent, tier_agent, report_agent]


if __name__ == "__main__":
    tasks, agents = create_all_tasks()
    print(f"✅ Created {len(tasks)} tasks")
    for task in tasks:
        print(f"  - {task.description[:50]}...")

