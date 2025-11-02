"""Tests for utility functions."""

import sys
import unittest
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.tools.search_tools import (
    generate_hash,
    fuzzy_match,
    is_duplicate,
    DEDUPLICATION_THRESHOLD
)


class TestDeduplication(unittest.TestCase):
    """Test deduplication functions."""
    
    def test_generate_hash(self):
        """Test hash generation."""
        hash1 = generate_hash("TechStartup", "https://tech.com", "2024-11-01")
        hash2 = generate_hash("TechStartup", "https://tech.com", "2024-11-01")
        
        # Same inputs should produce same hash
        self.assertEqual(hash1, hash2)
        
        # Different inputs should produce different hash
        hash3 = generate_hash("OtherStartup", "https://other.com", "2024-11-02")
        self.assertNotEqual(hash1, hash3)
        
        print("✅ test_generate_hash passed")
    
    def test_fuzzy_match_exact(self):
        """Test fuzzy matching with exact match."""
        result = fuzzy_match("TechStartup", "TechStartup")
        self.assertTrue(result)
        print("✅ test_fuzzy_match_exact passed")
    
    def test_fuzzy_match_similar(self):
        """Test fuzzy matching with similar strings."""
        # Should match with high similarity
        result = fuzzy_match("TechStartup", "Tech Startup", threshold=0.85)
        self.assertTrue(result)
        print("✅ test_fuzzy_match_similar passed")
    
    def test_fuzzy_match_different(self):
        """Test fuzzy matching with different strings."""
        result = fuzzy_match("TechStartup", "CompletelyDifferent", threshold=0.85)
        self.assertFalse(result)
        print("✅ test_fuzzy_match_different passed")
    
    def test_fuzzy_match_case_insensitive(self):
        """Test fuzzy matching is case insensitive."""
        result = fuzzy_match("TECHSTARTUP", "techstartup")
        self.assertTrue(result)
        print("✅ test_fuzzy_match_case_insensitive passed")
    
    def test_is_duplicate_empty_list(self):
        """Test is_duplicate with empty list."""
        result = is_duplicate("NewStartup", [])
        self.assertFalse(result)
        print("✅ test_is_duplicate_empty_list passed")
    
    def test_is_duplicate_found(self):
        """Test is_duplicate when duplicate exists."""
        existing = [
            {"name": "TechStartup", "website": "https://tech.com"},
            {"name": "OtherStartup", "website": "https://other.com"}
        ]
        result = is_duplicate("Tech Startup", existing)
        self.assertTrue(result)
        print("✅ test_is_duplicate_found passed")
    
    def test_is_duplicate_not_found(self):
        """Test is_duplicate when no duplicate exists."""
        existing = [
            {"name": "TechStartup", "website": "https://tech.com"},
            {"name": "OtherStartup", "website": "https://other.com"}
        ]
        result = is_duplicate("NewStartup", existing)
        self.assertFalse(result)
        print("✅ test_is_duplicate_not_found passed")


class TestHashConsistency(unittest.TestCase):
    """Test hash consistency."""
    
    def test_hash_consistency_across_calls(self):
        """Test that hash is consistent across multiple calls."""
        name = "StartupXYZ"
        website = "https://startup.com"
        date = "2024-11-01"
        
        hashes = [generate_hash(name, website, date) for _ in range(5)]
        
        # All hashes should be identical
        self.assertTrue(all(h == hashes[0] for h in hashes))
        print("✅ test_hash_consistency_across_calls passed")
    
    def test_hash_length(self):
        """Test that hash is MD5 (32 characters)."""
        hash_val = generate_hash("Test", "https://test.com", "2024-11-01")
        self.assertEqual(len(hash_val), 32)
        print("✅ test_hash_length passed")


class TestFuzzyMatchThreshold(unittest.TestCase):
    """Test fuzzy matching with different thresholds."""
    
    def test_threshold_high(self):
        """Test with high threshold."""
        # High threshold should be strict
        result = fuzzy_match("TechStartup", "Tech", threshold=0.95)
        self.assertFalse(result)
        print("✅ test_threshold_high passed")
    
    def test_threshold_low(self):
        """Test with low threshold."""
        # Low threshold should be lenient
        result = fuzzy_match("TechStartup", "Tech", threshold=0.30)
        self.assertTrue(result)
        print("✅ test_threshold_low passed")


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)

