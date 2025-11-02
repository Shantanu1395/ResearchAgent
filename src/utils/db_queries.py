"""Database query utilities for easy data retrieval."""

import logging
import sqlite3
from pathlib import Path
from typing import List, Dict, Any, Optional
from tabulate import tabulate

from ..config.settings import DB_PATH

logger = logging.getLogger(__name__)


class DatabaseQueries:
    """Utility class for database queries."""
    
    def __init__(self, db_path: Path = DB_PATH):
        """Initialize database queries.
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
    
    def _get_connection(self):
        """Get database connection."""
        return sqlite3.connect(self.db_path)
    
    def get_all_startups(self) -> List[Dict[str, Any]]:
        """Get all startups from database.
        
        Returns:
            List of startup dictionaries
        """
        try:
            conn = self._get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM startups ORDER BY created_at DESC")
            rows = cursor.fetchall()
            
            startups = [dict(row) for row in rows]
            conn.close()
            
            logger.info(f"✅ Retrieved {len(startups)} startups from database")
            return startups
        except Exception as e:
            logger.error(f"❌ Error retrieving startups: {e}")
            return []
    
    def get_startups_by_tier(self, tier: str) -> List[Dict[str, Any]]:
        """Get startups by tier.
        
        Args:
            tier: Tier name (Tier 1, Tier 2, Tier 3)
            
        Returns:
            List of startup dictionaries
        """
        try:
            conn = self._get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT * FROM startups WHERE primary_tier = ? ORDER BY india_fit_score DESC",
                (tier,)
            )
            rows = cursor.fetchall()
            
            startups = [dict(row) for row in rows]
            conn.close()
            
            logger.info(f"✅ Retrieved {len(startups)} startups for {tier}")
            return startups
        except Exception as e:
            logger.error(f"❌ Error retrieving startups by tier: {e}")
            return []
    
    def get_top_startups(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top startups by India fit score.
        
        Args:
            limit: Number of startups to return
            
        Returns:
            List of startup dictionaries
        """
        try:
            conn = self._get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT * FROM startups ORDER BY india_fit_score DESC LIMIT ?",
                (limit,)
            )
            rows = cursor.fetchall()
            
            startups = [dict(row) for row in rows]
            conn.close()
            
            logger.info(f"✅ Retrieved top {len(startups)} startups")
            return startups
        except Exception as e:
            logger.error(f"❌ Error retrieving top startups: {e}")
            return []
    
    def get_startups_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get startups by category.
        
        Args:
            category: Category name
            
        Returns:
            List of startup dictionaries
        """
        try:
            conn = self._get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT * FROM startups WHERE category LIKE ? ORDER BY india_fit_score DESC",
                (f"%{category}%",)
            )
            rows = cursor.fetchall()
            
            startups = [dict(row) for row in rows]
            conn.close()
            
            logger.info(f"✅ Retrieved {len(startups)} startups in category: {category}")
            return startups
        except Exception as e:
            logger.error(f"❌ Error retrieving startups by category: {e}")
            return []
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics.
        
        Returns:
            Dictionary with statistics
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Total startups
            cursor.execute("SELECT COUNT(*) FROM startups")
            total = cursor.fetchone()[0]
            
            # By tier
            cursor.execute("SELECT primary_tier, COUNT(*) FROM startups GROUP BY primary_tier")
            tier_counts = dict(cursor.fetchall())
            
            # By category
            cursor.execute("SELECT category, COUNT(*) FROM startups GROUP BY category")
            category_counts = dict(cursor.fetchall())
            
            # Average India fit score
            cursor.execute("SELECT AVG(india_fit_score) FROM startups")
            avg_score = cursor.fetchone()[0] or 0
            
            # By country
            cursor.execute("SELECT country, COUNT(*) FROM startups GROUP BY country ORDER BY COUNT(*) DESC LIMIT 10")
            top_countries = dict(cursor.fetchall())
            
            conn.close()
            
            stats = {
                "total_startups": total,
                "by_tier": tier_counts,
                "by_category": category_counts,
                "average_india_fit_score": round(avg_score, 2),
                "top_countries": top_countries
            }
            
            logger.info(f"✅ Retrieved database statistics")
            return stats
        except Exception as e:
            logger.error(f"❌ Error retrieving statistics: {e}")
            return {}
    
    def print_table(self, startups: List[Dict[str, Any]], columns: Optional[List[str]] = None):
        """Print startups as formatted table.
        
        Args:
            startups: List of startups
            columns: Columns to display (default: name, category, country, india_fit_score)
        """
        if not startups:
            print("No startups to display")
            return
        
        if columns is None:
            columns = ["name", "category", "country", "india_fit_score", "primary_tier"]
        
        # Filter columns that exist
        available_columns = [col for col in columns if col in startups[0]]
        
        # Extract data
        data = []
        for startup in startups:
            row = [startup.get(col, "N/A") for col in available_columns]
            data.append(row)
        
        # Print table
        print(tabulate(data, headers=available_columns, tablefmt="grid"))
    
    def print_statistics(self):
        """Print database statistics in formatted way."""
        stats = self.get_statistics()
        
        print("\n" + "="*60)
        print("📊 DATABASE STATISTICS")
        print("="*60)
        print(f"Total Startups: {stats.get('total_startups', 0)}")
        print(f"Average India Fit Score: {stats.get('average_india_fit_score', 0)}")
        
        print("\nBy Tier:")
        for tier, count in stats.get('by_tier', {}).items():
            print(f"  {tier}: {count}")
        
        print("\nTop Categories:")
        for category, count in sorted(stats.get('by_category', {}).items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  {category}: {count}")
        
        print("\nTop Countries:")
        for country, count in stats.get('top_countries', {}).items():
            print(f"  {country}: {count}")
        print("="*60 + "\n")

