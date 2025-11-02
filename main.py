"""Main entry point for Startup Research Agent System."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.crew_orchestration import StartupResearchCrew
from src.database.db import init_database, get_all_startups, get_startups_by_tier


def main():
    """Main entry point."""
    print("\n" + "="*70)
    print("🚀 STARTUP RESEARCH AGENT SYSTEM")
    print("="*70 + "\n")
    
    # Initialize database
    print("📦 Initializing database...")
    init_database()
    
    # Create and run crew
    print("🤖 Creating crew...\n")
    crew = StartupResearchCrew()
    result = crew.run()
    
    # Display results
    if result['success']:
        print("\n✅ Execution successful!")
        print(f"Run ID: {result['run_id']}")
        
        # Get results from database
        all_startups = get_all_startups()
        print(f"\n📊 Total startups in database: {len(all_startups)}")
        
        # Show by tier
        for tier in ["Tier 1", "Tier 2", "Tier 3"]:
            tier_startups = get_startups_by_tier(tier)
            print(f"  {tier}: {len(tier_startups)} startups")
    else:
        print(f"\n❌ Execution failed: {result.get('error')}")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()

