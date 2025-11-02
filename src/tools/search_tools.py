"""Search and data gathering tools."""

import logging
import requests
import hashlib
from typing import List, Dict, Any
from bs4 import BeautifulSoup
from difflib import SequenceMatcher

from ..config.settings import (
    GOOGLE_API_KEY, GOOGLE_SEARCH_ENGINE_ID, REQUESTS_TIMEOUT,
    DEDUPLICATION_THRESHOLD, MAX_RETRIES, RETRY_DELAY
)

logger = logging.getLogger(__name__)


def search_google(query: str, num_results: int = 10) -> List[Dict[str, str]]:
    """Search using Google Custom Search API with retry logic."""
    if not GOOGLE_API_KEY or not GOOGLE_SEARCH_ENGINE_ID:
        logger.warning("⚠️  Google API keys not configured")
        return []

    for attempt in range(MAX_RETRIES):
        try:
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                "q": query,
                "key": GOOGLE_API_KEY,
                "cx": GOOGLE_SEARCH_ENGINE_ID,
                "num": min(num_results, 10)
            }

            response = requests.get(url, params=params, timeout=REQUESTS_TIMEOUT)
            response.raise_for_status()

            results = []
            data = response.json()

            if "items" in data:
                for item in data["items"]:
                    results.append({
                        "title": item.get("title", ""),
                        "link": item.get("link", ""),
                        "snippet": item.get("snippet", "")
                    })

            logger.info(f"✅ Google search found {len(results)} results for: {query}")
            return results
        except requests.RequestException as e:
            logger.warning(f"⚠️  Google search attempt {attempt + 1}/{MAX_RETRIES} failed: {e}")
            if attempt < MAX_RETRIES - 1:
                import time
                time.sleep(RETRY_DELAY)
        except Exception as e:
            logger.error(f"❌ Unexpected error in Google search: {e}")
            return []

    logger.error(f"❌ Google search failed after {MAX_RETRIES} attempts")
    return []


def search_product_hunt(query: str) -> List[Dict[str, str]]:
    """Search Product Hunt for recent launches."""
    try:
        # Product Hunt API endpoint (free tier)
        url = "https://api.producthunt.com/v2/posts"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        params = {
            "order": "newest",
            "per_page": 20
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=REQUESTS_TIMEOUT)
        response.raise_for_status()
        
        results = []
        data = response.json()
        
        if "data" in data:
            for item in data["data"]:
                results.append({
                    "title": item.get("name", ""),
                    "link": item.get("url", ""),
                    "snippet": item.get("tagline", "")
                })
        
        return results
    except Exception as e:
        print(f"⚠️  Product Hunt search error: {e}")
        return []


def fetch_url_content(url: str) -> str:
    """Fetch and extract text content from a URL."""
    try:
        response = requests.get(url, timeout=REQUESTS_TIMEOUT)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Get text
        text = soup.get_text()

        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)

        return text[:1000]  # Return first 1000 chars
    except Exception as e:
        print(f"⚠️  Error fetching URL: {e}")
        return ""


def generate_hash(name: str, website: str, founded_date: str) -> str:
    """Generate hash for deduplication."""
    data = f"{name.lower()}{website.lower()}{founded_date}".encode()
    return hashlib.md5(data).hexdigest()


def fuzzy_match(str1: str, str2: str, threshold: float = DEDUPLICATION_THRESHOLD) -> bool:
    """Check if two strings are similar using fuzzy matching."""
    ratio = SequenceMatcher(None, str1.lower(), str2.lower()).ratio()
    return ratio >= threshold


def is_duplicate(startup_name: str, existing_startups: List[Dict[str, Any]]) -> bool:
    """Check if startup is duplicate using fuzzy matching."""
    for existing in existing_startups:
        if fuzzy_match(startup_name, existing.get('name', '')):
            logger.debug(f"⚠️  Duplicate detected: {startup_name} matches {existing.get('name')}")
            return True
    return False


def search_web_fallback(query: str) -> List[Dict[str, Any]]:
    """Fallback web search using DuckDuckGo (no API key required)."""
    try:
        # Using DuckDuckGo HTML search (no API key needed)
        url = "https://html.duckduckgo.com/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        params = {"q": query}

        response = requests.get(url, params=params, headers=headers, timeout=REQUESTS_TIMEOUT)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        results = []

        # Extract results from DuckDuckGo
        for result in soup.find_all('div', class_='result'):
            try:
                title_elem = result.find('a', class_='result__a')
                snippet_elem = result.find('a', class_='result__snippet')

                if title_elem and snippet_elem:
                    results.append({
                        "title": title_elem.get_text(strip=True),
                        "link": title_elem.get('href', ''),
                        "snippet": snippet_elem.get_text(strip=True)
                    })
            except Exception as e:
                logger.debug(f"Error parsing result: {e}")
                continue

        logger.info(f"✅ DuckDuckGo found {len(results)} results for: {query}")
        return results
    except Exception as e:
        logger.warning(f"⚠️  DuckDuckGo search failed: {e}")
        return []


def search_recent_startups(days: int = 30) -> List[Dict[str, Any]]:
    """Search for startups founded in the last N days with multiple fallback sources."""
    from datetime import datetime, timedelta

    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    # Get current year and month for dynamic queries
    current_year = end_date.year
    current_month = end_date.strftime('%B')  # e.g., "November"
    previous_month = (end_date.replace(day=1) - timedelta(days=1)).strftime('%B')

    # Format dates for Google search (YYYY-MM-DD)
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    # More specific queries with date filters
    queries = [
        # Recent date-specific queries
        f"startup founded after:{start_date_str} before:{end_date_str}",
        f"new startup launch after:{start_date_str} before:{end_date_str}",
        f"startup announcement after:{start_date_str} before:{end_date_str}",

        # Month-specific queries
        f"startup founded {current_month} {current_year}",
        f"startup founded {previous_month} {current_year}",

        # Category-specific with year
        f"AI startup founded {current_year}",
        f"FinTech startup founded {current_year}",
        f"SaaS startup founded {current_year}",
        f"tech startup founded {current_year}",

        # Recent news queries
        f"startup news {current_month} {current_year}",
        f"new company founded {current_month} {current_year}"
    ]

    all_results = []
    seen_titles = set()  # Track seen titles to avoid duplicates

    for query in queries:
        logger.info(f"🔍 Searching: {query}")

        # Try Google first
        results = search_google(query, num_results=10)

        # If Google fails, use DuckDuckGo fallback
        if not results:
            logger.info(f"   Google failed, trying DuckDuckGo...")
            results = search_web_fallback(query)

        # Filter out duplicates and old results
        for result in results:
            title = result.get('title', '')
            # Skip if we've seen this title before
            if title not in seen_titles:
                # Check if result mentions current year or recent months
                snippet = result.get('snippet', '').lower()
                if str(current_year) in snippet or current_month.lower() in snippet or previous_month.lower() in snippet:
                    all_results.append(result)
                    seen_titles.add(title)

        logger.info(f"   Found {len(results)} results, {len([r for r in results if r.get('title') not in seen_titles])} new")

    logger.info(f"✅ Total unique results from all queries: {len(all_results)}")
    return all_results


if __name__ == "__main__":
    # Test search
    results = search_recent_startups()
    print(f"Found {len(results)} results")
    for result in results[:3]:
        print(f"- {result['title']}")

