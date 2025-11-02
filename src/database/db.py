"""SQLite database setup and management."""

import sqlite3
import json
import logging
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any, Generator

from ..config.settings import DB_PATH

logger = logging.getLogger(__name__)


@contextmanager
def get_db_connection() -> Generator[sqlite3.Connection, None, None]:
    """Context manager for database connections."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_database() -> None:
    """Initialize database with required tables."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # Create startups table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS startups (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    website TEXT,
                    description TEXT,
                    category TEXT,
                    founded_date TEXT,
                    country TEXT,
                    india_fit_score INTEGER DEFAULT 0,
                    india_fit_analysis TEXT,
                    primary_tier TEXT,
                    secondary_tiers TEXT,
                    source TEXT,
                    source_url TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    hash TEXT UNIQUE
                )
            """)

            # Create run_metadata table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS run_metadata (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id TEXT UNIQUE NOT NULL,
                    run_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    total_startups_found INTEGER DEFAULT 0,
                    tier_1_count INTEGER DEFAULT 0,
                    tier_2_count INTEGER DEFAULT 0,
                    tier_3_count INTEGER DEFAULT 0,
                    processing_time_seconds REAL,
                    status TEXT DEFAULT 'completed',
                    report_path TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create knowledge_base table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS knowledge_base (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT UNIQUE NOT NULL,
                    value TEXT,
                    category TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.commit()
            logger.info("✅ Database initialized successfully")
    except Exception as e:
        logger.error(f"❌ Error initializing database: {e}")
        raise


def insert_startup(startup_data: Dict[str, Any]) -> bool:
    """Insert a startup into the database."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # Convert secondary_tiers list to JSON string if needed
            secondary_tiers = startup_data.get('secondary_tiers')
            if isinstance(secondary_tiers, list):
                secondary_tiers = json.dumps(secondary_tiers)

            cursor.execute("""
                INSERT INTO startups (
                    name, website, description, category, founded_date,
                    country, india_fit_score, india_fit_analysis,
                    primary_tier, secondary_tiers, source, source_url, hash
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                startup_data.get('name'),
                startup_data.get('website'),
                startup_data.get('description'),
                startup_data.get('category'),
                startup_data.get('founded_date'),
                startup_data.get('country'),
                startup_data.get('india_fit_score', 0),
                startup_data.get('india_fit_analysis'),
                startup_data.get('primary_tier'),
                secondary_tiers,
                startup_data.get('source'),
                startup_data.get('source_url'),
                startup_data.get('hash')
            ))

            conn.commit()
            logger.debug(f"✅ Inserted startup: {startup_data.get('name')}")
            return True
    except sqlite3.IntegrityError:
        logger.warning(f"⚠️  Duplicate startup: {startup_data.get('name')}")
        return False
    except Exception as e:
        logger.error(f"❌ Error inserting startup: {e}")
        return False


def get_all_startups() -> List[Dict]:
    """Get all startups from database."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM startups ORDER BY created_at DESC")
            startups = [dict(row) for row in cursor.fetchall()]
            logger.debug(f"✅ Retrieved {len(startups)} startups")
            return startups
    except Exception as e:
        logger.error(f"❌ Error retrieving startups: {e}")
        return []


def get_startups_by_tier(tier: str) -> List[Dict]:
    """Get startups by tier."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM startups WHERE primary_tier = ? ORDER BY india_fit_score DESC",
                (tier,)
            )
            startups = [dict(row) for row in cursor.fetchall()]
            logger.debug(f"✅ Retrieved {len(startups)} startups for tier {tier}")
            return startups
    except Exception as e:
        logger.error(f"❌ Error retrieving startups by tier: {e}")
        return []


def insert_run_metadata(run_data: Dict[str, Any]) -> bool:
    """Insert run metadata."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO run_metadata (
                    run_id, total_startups_found, tier_1_count,
                    tier_2_count, tier_3_count, processing_time_seconds,
                    status, report_path
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                run_data.get('run_id'),
                run_data.get('total_startups_found', 0),
                run_data.get('tier_1_count', 0),
                run_data.get('tier_2_count', 0),
                run_data.get('tier_3_count', 0),
                run_data.get('processing_time_seconds'),
                run_data.get('status', 'completed'),
                run_data.get('report_path')
            ))

            conn.commit()
            logger.info(f"✅ Inserted run metadata: {run_data.get('run_id')}")
            return True
    except Exception as e:
        logger.error(f"❌ Error inserting run metadata: {e}")
        return False


def get_latest_run() -> Optional[Dict]:
    """Get latest run metadata."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM run_metadata ORDER BY run_date DESC LIMIT 1")
            row = cursor.fetchone()
            logger.debug("✅ Retrieved latest run metadata")
            return dict(row) if row else None
    except Exception as e:
        logger.error(f"❌ Error retrieving latest run: {e}")
        return None


if __name__ == "__main__":
    init_database()

