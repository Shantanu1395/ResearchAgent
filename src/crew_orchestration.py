"""CrewAI crew orchestration for startup research."""

import json
import logging
import re
from datetime import datetime
from pathlib import Path
from crewai import Crew, Process
from .tasks.crew_tasks import create_all_tasks
from .database.db import init_database, insert_startup, insert_run_metadata, get_all_startups
from .utils.agent_tracker import AgentTracker
from .tools.email_tools import send_startup_report_email
from .config.settings import ENABLE_EMAIL_NOTIFICATIONS, EMAIL_RECIPIENTS

logger = logging.getLogger(__name__)


class StartupResearchCrew:
    """Main crew for startup research."""

    def __init__(self):
        """Initialize the crew."""
        self.tasks, self.agents = create_all_tasks()
        self.crew = None
        self.run_id = None
        self.tracker = None
        self.start_time = None

    def setup_crew(self):
        """Setup the crew with all agents and tasks."""
        self.crew = Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=True,
            cache=True
        )
        print("✅ Crew setup complete")

    def generate_run_id(self) -> str:
        """Generate unique run ID."""
        return f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    def parse_startup_data(self, text: str) -> list:
        """Parse startup data from agent output."""
        startups = []
        try:
            # Try to parse as JSON first
            if text.strip().startswith('[') or text.strip().startswith('{'):
                data = json.loads(text)
                if isinstance(data, list):
                    startups = data
                elif isinstance(data, dict):
                    # Check for various possible keys
                    if 'startups' in data:
                        startups = data['startups']
                    elif 'top_opportunities' in data:
                        startups = data['top_opportunities']
                    elif 'opportunities' in data:
                        startups = data['opportunities']
                    else:
                        # If it's a dict with startup-like data, wrap it
                        if 'name' in data:
                            startups = [data]
            else:
                # Try to extract JSON from text
                json_match = re.search(r'\[.*\]|\{.*\}', text, re.DOTALL)
                if json_match:
                    startups = json.loads(json_match.group())
                    if isinstance(startups, dict) and 'startups' in startups:
                        startups = startups['startups']
                    elif isinstance(startups, dict) and 'top_opportunities' in startups:
                        startups = startups['top_opportunities']
                    elif isinstance(startups, dict):
                        startups = [startups]
        except json.JSONDecodeError:
            logger.warning("Could not parse JSON from agent output")

        return startups if isinstance(startups, list) else []

    def extract_tier_info(self, text: str) -> dict:
        """Extract tier information from agent output."""
        tier_info = {}
        try:
            if text.strip().startswith('[') or text.strip().startswith('{'):
                data = json.loads(text)
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict):
                            name = item.get('name') or item.get('startup_name')
                            tier_info[name] = {
                                'primary_tier': item.get('primary_tier') or item.get('tier'),
                                'secondary_tiers': item.get('secondary_tiers') or item.get('secondary_tier'),
                                'reasoning': item.get('reasoning') or item.get('reason')
                            }
                elif isinstance(data, dict):
                    for key, value in data.items():
                        if isinstance(value, dict):
                            tier_info[key] = value
        except json.JSONDecodeError:
            logger.warning("Could not parse tier data from agent output")

        return tier_info

    def extract_market_fit(self, text: str) -> dict:
        """Extract market fit scores from agent output."""
        fit_info = {}
        try:
            if text.strip().startswith('[') or text.strip().startswith('{'):
                data = json.loads(text)
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict):
                            name = item.get('name') or item.get('startup_name')
                            fit_info[name] = {
                                'score': item.get('india_fit_score') or item.get('score'),
                                'analysis': item.get('india_fit_analysis') or item.get('analysis')
                            }
                elif isinstance(data, dict):
                    for key, value in data.items():
                        if isinstance(value, dict):
                            fit_info[key] = value
        except json.JSONDecodeError:
            logger.warning("Could not parse market fit data from agent output")

        return fit_info

    def run(self) -> dict:
        """Run the crew."""
        try:
            self.start_time = datetime.now()
            print("\n" + "="*60)
            print("🚀 Starting Startup Research Agent System")
            print("="*60 + "\n")

            # Initialize database
            init_database()

            # Setup crew
            self.setup_crew()

            # Generate run ID
            self.run_id = self.generate_run_id()
            print(f"📊 Run ID: {self.run_id}\n")

            # Initialize tracker
            self.tracker = AgentTracker(self.run_id)

            # Execute crew
            print("⏳ Executing crew tasks...\n")

            # Log agent start
            for agent in self.agents:
                self.tracker.start_agent(
                    agent.role,
                    f"Executing {agent.role}",
                    {'role': agent.role, 'goal': agent.goal}
                )

            result = self.crew.kickoff()

            # Log agent completion
            for agent in self.agents:
                self.tracker.end_agent(agent.role, str(result)[:500], 'completed')

            # Process results
            print("\n" + "="*60)
            print("✅ Crew execution completed")
            print("="*60 + "\n")

            # Extract and save results
            self._process_and_save_results(result)

            # Save reports
            self.tracker.save_all_reports()

            # Send email notification if enabled
            self._send_email_notification()

            return {
                'success': True,
                'run_id': self.run_id,
                'result': str(result),
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"❌ Error running crew: {e}", exc_info=True)
            print(f"\n❌ Error running crew: {e}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def _process_and_save_results(self, result):
        """Process crew results and save to database."""
        try:
            result_str = str(result)

            # Debug: Print first 500 chars of result
            logger.info(f"📊 Crew result (first 500 chars): {result_str[:500]}")

            # Parse startups from discovery agent output
            startups = self.parse_startup_data(result_str)

            # Debug: Print parsed startups
            if startups:
                logger.info(f"📊 Parsed startups: {json.dumps(startups[:2], indent=2)}")

            logger.info(f"📊 Found {len(startups)} startups to process")

            # Extract tier and market fit info
            tier_info = self.extract_tier_info(result_str)
            fit_info = self.extract_market_fit(result_str)

            # Insert startups into database
            inserted_count = 0
            for startup in startups:
                if not isinstance(startup, dict):
                    continue

                name = startup.get('name') or startup.get('startup_name')
                if not name:
                    continue

                # Merge tier and fit info
                startup_data = {
                    'name': name,
                    'website': startup.get('website') or startup.get('url'),
                    'description': startup.get('description'),
                    'category': startup.get('category'),
                    'founded_date': startup.get('founded_date') or startup.get('date'),
                    'country': startup.get('country'),
                    'source': startup.get('source'),
                    'source_url': startup.get('source_url'),
                    'hash': hash(name)
                }

                # Add tier info - check both extracted tier_info and startup dict
                if name in tier_info:
                    startup_data['primary_tier'] = tier_info[name].get('primary_tier')
                    startup_data['secondary_tiers'] = tier_info[name].get('secondary_tiers')
                elif 'primary_tier' in startup:
                    startup_data['primary_tier'] = startup.get('primary_tier')
                    startup_data['secondary_tiers'] = startup.get('secondary_tiers')

                # Add market fit info - check both extracted fit_info and startup dict
                if name in fit_info:
                    startup_data['india_fit_score'] = fit_info[name].get('score', 0)
                    startup_data['india_fit_analysis'] = fit_info[name].get('analysis')
                elif 'india_fit_score' in startup:
                    startup_data['india_fit_score'] = startup.get('india_fit_score', 0)
                    startup_data['india_fit_analysis'] = startup.get('india_fit_analysis')

                # Insert into database
                if insert_startup(startup_data):
                    inserted_count += 1

            logger.info(f"✅ Inserted {inserted_count} startups into database")

            # Get final counts
            all_startups = get_all_startups()
            tier_1_count = len([s for s in all_startups if s.get('primary_tier') == 'Tier 1'])
            tier_2_count = len([s for s in all_startups if s.get('primary_tier') == 'Tier 2'])
            tier_3_count = len([s for s in all_startups if s.get('primary_tier') == 'Tier 3'])

            # Save run metadata
            processing_time = (datetime.now() - self.start_time).total_seconds()
            run_data = {
                'run_id': self.run_id,
                'total_startups_found': len(all_startups),
                'tier_1_count': tier_1_count,
                'tier_2_count': tier_2_count,
                'tier_3_count': tier_3_count,
                'processing_time_seconds': processing_time,
                'status': 'completed',
                'report_path': str(self.tracker.output_dir)
            }

            insert_run_metadata(run_data)

            print(f"\n📊 Summary:")
            print(f"   Total startups: {len(all_startups)}")
            print(f"   Tier 1: {tier_1_count}")
            print(f"   Tier 2: {tier_2_count}")
            print(f"   Tier 3: {tier_3_count}")
            print(f"   Processing time: {processing_time:.2f}s")
            print(f"   Reports saved to: {self.tracker.output_dir}\n")

        except Exception as e:
            logger.error(f"❌ Error processing results: {e}", exc_info=True)

    def _send_email_notification(self) -> None:
        """Send email notification with report."""
        if not ENABLE_EMAIL_NOTIFICATIONS or not EMAIL_RECIPIENTS:
            return

        try:
            # Get startup counts by tier
            all_startups = get_all_startups()
            tier_breakdown = {
                'Tier 1': len([s for s in all_startups if s.get('primary_tier') == 'Tier 1']),
                'Tier 2': len([s for s in all_startups if s.get('primary_tier') == 'Tier 2']),
                'Tier 3': len([s for s in all_startups if s.get('primary_tier') == 'Tier 3']),
            }

            # Send email
            success = send_startup_report_email(
                recipient_emails=EMAIL_RECIPIENTS,
                run_id=self.run_id,
                report_dir=self.tracker.output_dir,
                startup_count=len(all_startups),
                tier_breakdown=tier_breakdown,
            )

            if success:
                print("📧 Email notification sent successfully")
            else:
                print("⚠️  Email notification failed - check configuration")

        except Exception as e:
            logger.error(f"❌ Error sending email notification: {e}")


def main():
    """Main entry point."""
    crew = StartupResearchCrew()
    result = crew.run()
    
    print("\n" + "="*60)
    print("📋 EXECUTION SUMMARY")
    print("="*60)
    print(json.dumps(result, indent=2))
    print("="*60 + "\n")
    
    return result


if __name__ == "__main__":
    main()

