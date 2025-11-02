"""Tests for database functions."""

import sys
import unittest
import tempfile
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database.db import (
    init_database,
    insert_startup,
    get_all_startups,
    get_startups_by_tier,
    insert_run_metadata,
    get_latest_run
)


class TestDatabaseOperations(unittest.TestCase):
    """Test database operations."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test database."""
        init_database()
        print("✅ Test database initialized")
    
    def test_insert_startup_success(self):
        """Test successful startup insertion."""
        startup_data = {
            'name': 'TestStartup1',
            'website': 'https://test1.com',
            'description': 'Test startup 1',
            'category': 'Tech',
            'founded_date': '2024-11-01',
            'country': 'USA',
            'india_fit_score': 75,
            'india_fit_analysis': 'Good fit',
            'primary_tier': 'Tier 1',
            'secondary_tiers': 'Tier 2',
            'source': 'Google',
            'source_url': 'https://google.com',
            'hash': 'test_hash_1'
        }
        
        result = insert_startup(startup_data)
        self.assertTrue(result)
        print("✅ test_insert_startup_success passed")
    
    def test_insert_duplicate_startup(self):
        """Test duplicate startup insertion."""
        startup_data = {
            'name': 'TestStartup2',
            'website': 'https://test2.com',
            'description': 'Test startup 2',
            'category': 'Tech',
            'founded_date': '2024-11-01',
            'country': 'USA',
            'india_fit_score': 80,
            'india_fit_analysis': 'Excellent fit',
            'primary_tier': 'Tier 1',
            'secondary_tiers': 'Tier 2',
            'source': 'Google',
            'source_url': 'https://google.com',
            'hash': 'test_hash_2'
        }
        
        # First insert should succeed
        result1 = insert_startup(startup_data)
        self.assertTrue(result1)
        
        # Duplicate insert should fail
        result2 = insert_startup(startup_data)
        self.assertFalse(result2)
        print("✅ test_insert_duplicate_startup passed")
    
    def test_get_all_startups(self):
        """Test retrieving all startups."""
        startups = get_all_startups()
        self.assertIsInstance(startups, list)
        self.assertGreater(len(startups), 0)
        print(f"✅ test_get_all_startups passed (found {len(startups)} startups)")
    
    def test_get_startups_by_tier(self):
        """Test retrieving startups by tier."""
        # Insert a Tier 1 startup
        startup_data = {
            'name': 'Tier1Startup',
            'website': 'https://tier1.com',
            'description': 'Tier 1 startup',
            'category': 'Tech',
            'founded_date': '2024-11-01',
            'country': 'USA',
            'india_fit_score': 85,
            'india_fit_analysis': 'Excellent',
            'primary_tier': 'Tier 1',
            'secondary_tiers': None,
            'source': 'Google',
            'source_url': 'https://google.com',
            'hash': 'tier1_hash'
        }
        
        insert_startup(startup_data)
        
        # Retrieve Tier 1 startups
        tier1_startups = get_startups_by_tier('Tier 1')
        self.assertIsInstance(tier1_startups, list)
        self.assertGreater(len(tier1_startups), 0)
        print(f"✅ test_get_startups_by_tier passed (found {len(tier1_startups)} Tier 1 startups)")
    
    def test_insert_run_metadata(self):
        """Test inserting run metadata."""
        run_data = {
            'run_id': 'test_run_001',
            'total_startups_found': 10,
            'tier_1_count': 3,
            'tier_2_count': 4,
            'tier_3_count': 3,
            'processing_time_seconds': 45.5,
            'status': 'completed',
            'report_path': '/reports/test_run_001.json'
        }
        
        result = insert_run_metadata(run_data)
        self.assertTrue(result)
        print("✅ test_insert_run_metadata passed")
    
    def test_get_latest_run(self):
        """Test retrieving latest run metadata."""
        # Insert a run first
        run_data = {
            'run_id': 'test_run_002',
            'total_startups_found': 15,
            'tier_1_count': 5,
            'tier_2_count': 5,
            'tier_3_count': 5,
            'processing_time_seconds': 60.0,
            'status': 'completed',
            'report_path': '/reports/test_run_002.json'
        }
        
        insert_run_metadata(run_data)
        
        # Retrieve latest run
        latest_run = get_latest_run()
        self.assertIsNotNone(latest_run)
        self.assertEqual(latest_run['run_id'], 'test_run_002')
        print("✅ test_get_latest_run passed")


class TestDatabaseIntegrity(unittest.TestCase):
    """Test database integrity."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test database."""
        init_database()
    
    def test_startup_data_integrity(self):
        """Test that startup data is stored and retrieved correctly."""
        startup_data = {
            'name': 'IntegrityTest',
            'website': 'https://integrity.com',
            'description': 'Integrity test startup',
            'category': 'AI',
            'founded_date': '2024-11-01',
            'country': 'India',
            'india_fit_score': 90,
            'india_fit_analysis': 'Perfect fit',
            'primary_tier': 'Tier 1',
            'secondary_tiers': 'Tier 2',
            'source': 'Product Hunt',
            'source_url': 'https://producthunt.com',
            'hash': 'integrity_hash'
        }
        
        # Insert
        insert_startup(startup_data)
        
        # Retrieve
        all_startups = get_all_startups()
        found = False
        for startup in all_startups:
            if startup['name'] == 'IntegrityTest':
                found = True
                self.assertEqual(startup['website'], 'https://integrity.com')
                self.assertEqual(startup['india_fit_score'], 90)
                self.assertEqual(startup['primary_tier'], 'Tier 1')
                break
        
        self.assertTrue(found)
        print("✅ test_startup_data_integrity passed")


if __name__ == "__main__":
    unittest.main(verbosity=2)

