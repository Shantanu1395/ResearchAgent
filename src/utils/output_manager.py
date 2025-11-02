"""Output management and file generation utilities."""

import json
import logging
import csv
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class OutputManager:
    """Manages output file generation for each run."""
    
    def __init__(self, run_id: str, output_dir: Optional[Path] = None):
        """Initialize output manager.
        
        Args:
            run_id: Unique run identifier
            output_dir: Directory to save outputs (default: ./reports)
        """
        self.run_id = run_id
        self.output_dir = output_dir or Path(__file__).parent.parent.parent / "reports"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create run-specific directory
        self.run_dir = self.output_dir / run_id
        self.run_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"✅ Output directory created: {self.run_dir}")
    
    def save_agent_output(self, agent_name: str, output: Any, format: str = "json") -> Path:
        """Save agent output to file.
        
        Args:
            agent_name: Name of the agent
            output: Output data to save
            format: File format (json or txt)
            
        Returns:
            Path to saved file
        """
        timestamp = datetime.now().strftime("%H%M%S")
        filename = f"{agent_name.replace(' ', '_')}_{timestamp}.{format}"
        filepath = self.run_dir / filename
        
        try:
            if format == "json":
                with open(filepath, 'w') as f:
                    if isinstance(output, str):
                        json.dump({"output": output}, f, indent=2)
                    else:
                        json.dump(output, f, indent=2, default=str)
            else:  # txt format
                with open(filepath, 'w') as f:
                    f.write(str(output))
            
            logger.info(f"✅ Saved {agent_name} output to: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"❌ Error saving agent output: {e}")
            return None
    
    def save_discovery_output(self, startups: List[Dict[str, Any]]) -> Path:
        """Save discovery agent output.
        
        Args:
            startups: List of discovered startups
            
        Returns:
            Path to saved file
        """
        data = {
            "run_id": self.run_id,
            "timestamp": datetime.now().isoformat(),
            "total_found": len(startups),
            "startups": startups
        }
        return self.save_agent_output("discovery_agent", data)
    
    def save_market_analysis_output(self, analyses: List[Dict[str, Any]]) -> Path:
        """Save market analysis agent output.
        
        Args:
            analyses: List of market analyses
            
        Returns:
            Path to saved file
        """
        data = {
            "run_id": self.run_id,
            "timestamp": datetime.now().isoformat(),
            "total_analyzed": len(analyses),
            "analyses": analyses
        }
        return self.save_agent_output("market_analysis_agent", data)
    
    def save_tier_analysis_output(self, analyses: List[Dict[str, Any]]) -> Path:
        """Save tier analysis agent output.
        
        Args:
            analyses: List of tier analyses
            
        Returns:
            Path to saved file
        """
        data = {
            "run_id": self.run_id,
            "timestamp": datetime.now().isoformat(),
            "total_categorized": len(analyses),
            "analyses": analyses
        }
        return self.save_agent_output("tier_analysis_agent", data)
    
    def save_final_report(self, report: Dict[str, Any]) -> Path:
        """Save final report.
        
        Args:
            report: Final report data
            
        Returns:
            Path to saved file
        """
        filepath = self.run_dir / "final_report.json"
        
        try:
            with open(filepath, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            
            logger.info(f"✅ Saved final report to: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"❌ Error saving final report: {e}")
            return None
    
    def save_csv_export(self, startups: List[Dict[str, Any]], filename: str = "startups.csv") -> Path:
        """Save startups as CSV.
        
        Args:
            startups: List of startups
            filename: CSV filename
            
        Returns:
            Path to saved file
        """
        filepath = self.run_dir / filename
        
        try:
            if not startups:
                logger.warning("No startups to export")
                return None
            
            # Get all unique keys
            fieldnames = set()
            for startup in startups:
                fieldnames.update(startup.keys())
            fieldnames = sorted(list(fieldnames))
            
            with open(filepath, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(startups)
            
            logger.info(f"✅ Saved CSV export to: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"❌ Error saving CSV: {e}")
            return None
    
    def get_run_summary(self) -> Dict[str, Any]:
        """Get summary of generated files.
        
        Returns:
            Dictionary with file paths and counts
        """
        files = list(self.run_dir.glob("*"))
        
        return {
            "run_id": self.run_id,
            "output_directory": str(self.run_dir),
            "total_files": len(files),
            "files": [str(f.name) for f in files],
            "generated_at": datetime.now().isoformat()
        }

