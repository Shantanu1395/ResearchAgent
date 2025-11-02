"""Pydantic models for structured data."""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, validator


class StartupBasic(BaseModel):
    """Basic startup information."""
    name: str = Field(..., description="Startup name")
    website: Optional[str] = Field(None, description="Website URL")
    description: Optional[str] = Field(None, description="Brief description")
    category: str = Field(..., description="Business category")
    founded_date: Optional[str] = Field(None, description="Founded date")
    country: str = Field(..., description="Country of origin")
    founder_info: Optional[str] = Field(None, description="Founder information")
    source: Optional[str] = Field(None, description="Source of information")
    source_url: Optional[str] = Field(None, description="Source URL")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "TechStartup Inc",
                "website": "https://techstartup.com",
                "description": "AI-powered analytics platform",
                "category": "AI/ML",
                "founded_date": "2024-10-15",
                "country": "USA",
                "founder_info": "John Doe",
                "source": "Product Hunt",
                "source_url": "https://producthunt.com/..."
            }
        }


class StartupMarketAnalysis(BaseModel):
    """Market fit analysis for a startup."""
    startup_name: str = Field(..., description="Startup name")
    india_fit_score: int = Field(..., ge=0, le=100, description="India market fit score 0-100")
    market_demand: str = Field(..., description="Market demand assessment")
    competition_analysis: str = Field(..., description="Competition landscape")
    regulatory_considerations: str = Field(..., description="Regulatory environment")
    cultural_fit: str = Field(..., description="Cultural fit analysis")
    recommended_adaptations: List[str] = Field(default_factory=list, description="Recommended changes")
    barriers: List[str] = Field(default_factory=list, description="Potential barriers")

    class Config:
        json_schema_extra = {
            "example": {
                "startup_name": "TechStartup Inc",
                "india_fit_score": 85,
                "market_demand": "High demand for AI solutions",
                "competition_analysis": "Moderate competition",
                "regulatory_considerations": "Compliant with data protection laws",
                "cultural_fit": "Good fit for Indian market",
                "recommended_adaptations": ["Localize content", "Partner with local vendors"],
                "barriers": ["High customer acquisition cost"]
            }
        }


class StartupTierAnalysis(BaseModel):
    """Tier categorization for a startup."""
    startup_name: str = Field(..., description="Startup name")
    primary_tier: str = Field(..., description="Primary tier (Tier 1, 2, or 3)")
    secondary_tiers: List[str] = Field(default_factory=list, description="Secondary tiers")
    reasoning: str = Field(..., description="Reasoning for categorization")
    market_size_estimate: str = Field(..., description="Market size estimate")
    potential_revenue_opportunity: str = Field(..., description="Revenue opportunity")

    class Config:
        json_schema_extra = {
            "example": {
                "startup_name": "TechStartup Inc",
                "primary_tier": "Tier 1",
                "secondary_tiers": ["Tier 2"],
                "reasoning": "Large market size and high investor presence",
                "market_size_estimate": "High",
                "potential_revenue_opportunity": "Significant"
            }
        }


class StartupComplete(StartupBasic):
    """Complete startup information with analysis."""
    india_fit_score: int = Field(default=0, ge=0, le=100)
    india_fit_analysis: Optional[str] = None
    primary_tier: Optional[str] = None
    secondary_tiers: Optional[List[str]] = None
    market_size_estimate: Optional[str] = None
    potential_revenue_opportunity: Optional[str] = None


class DiscoveryOutput(BaseModel):
    """Output from discovery agent."""
    startups_found: int = Field(..., description="Number of startups found")
    startups: List[StartupBasic] = Field(..., description="List of discovered startups")
    search_queries_used: List[str] = Field(default_factory=list, description="Queries used")
    timestamp: datetime = Field(default_factory=datetime.now)

    class Config:
        json_schema_extra = {
            "example": {
                "startups_found": 5,
                "startups": [],
                "search_queries_used": ["startup founded last month"],
                "timestamp": "2024-11-02T10:00:00"
            }
        }


class MarketAnalysisOutput(BaseModel):
    """Output from market fit analysis agent."""
    analyzed_startups: int = Field(..., description="Number of startups analyzed")
    analyses: List[StartupMarketAnalysis] = Field(..., description="Market analyses")
    timestamp: datetime = Field(default_factory=datetime.now)


class TierAnalysisOutput(BaseModel):
    """Output from tier categorization agent."""
    categorized_startups: int = Field(..., description="Number of startups categorized")
    analyses: List[StartupTierAnalysis] = Field(..., description="Tier analyses")
    timestamp: datetime = Field(default_factory=datetime.now)


class ReportSummary(BaseModel):
    """Final report summary."""
    run_id: str = Field(..., description="Unique run identifier")
    run_date: datetime = Field(default_factory=datetime.now)
    total_startups_found: int = Field(..., description="Total startups discovered")
    tier_1_count: int = Field(default=0)
    tier_2_count: int = Field(default=0)
    tier_3_count: int = Field(default=0)
    top_opportunities: List[StartupComplete] = Field(default_factory=list)
    trending_categories: List[str] = Field(default_factory=list)
    market_gaps: List[str] = Field(default_factory=list)
    opportunities: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        json_schema_extra = {
            "example": {
                "run_id": "run_20241102_100000",
                "run_date": "2024-11-02T10:00:00",
                "total_startups_found": 20,
                "tier_1_count": 10,
                "tier_2_count": 7,
                "tier_3_count": 3,
                "top_opportunities": [],
                "trending_categories": ["AI/ML", "FinTech"],
                "market_gaps": ["Localized solutions"],
                "opportunities": ["Partnership opportunities"],
                "recommendations": ["Focus on Tier 1 cities"],
                "generated_at": "2024-11-02T10:30:00"
            }
        }

