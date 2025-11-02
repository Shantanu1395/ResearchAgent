"""CrewAI BaseTool implementations for startup research."""

from crewai.tools import BaseTool
from typing import List, Dict, Any
from .search_tools import (
    search_google as search_google_impl,
    search_product_hunt as search_product_hunt_impl,
    fetch_url_content as fetch_url_content_impl,
    search_recent_startups as search_recent_startups_impl
)


class SearchGoogleTool(BaseTool):
    """Tool for searching using Google Custom Search API."""
    name: str = "search_google"
    description: str = "Search using Google Custom Search API to find startups and information"
    
    def _run(self, query: str, num_results: int = 10) -> str:
        """Execute the search."""
        results = search_google_impl(query, num_results)
        return str(results)


class SearchProductHuntTool(BaseTool):
    """Tool for searching Product Hunt for recent launches."""
    name: str = "search_product_hunt"
    description: str = "Search Product Hunt for recent startup launches"
    
    def _run(self, query: str = "") -> str:
        """Execute the search."""
        results = search_product_hunt_impl(query)
        return str(results)


class FetchUrlContentTool(BaseTool):
    """Tool for fetching and extracting text content from a URL."""
    name: str = "fetch_url_content"
    description: str = "Fetch and extract text content from a URL"
    
    def _run(self, url: str) -> str:
        """Execute the fetch."""
        content = fetch_url_content_impl(url)
        return content


class SearchRecentStartupsTool(BaseTool):
    """Tool for searching startups founded in the last N days."""
    name: str = "search_recent_startups"
    description: str = "Search for startups founded in the last N days with date filters"
    
    def _run(self, days: int = 30) -> str:
        """Execute the search."""
        results = search_recent_startups_impl(days)
        return str(results)


# Create tool instances
search_google_tool = SearchGoogleTool()
search_product_hunt_tool = SearchProductHuntTool()
fetch_url_content_tool = FetchUrlContentTool()
search_recent_startups_tool = SearchRecentStartupsTool()

