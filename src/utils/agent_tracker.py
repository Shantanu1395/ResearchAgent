"""Track and log agent execution details."""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class AgentTracker:
    """Track agent inputs, outputs, and tool usage."""
    
    def __init__(self, run_id: str):
        self.run_id = run_id
        self.agents_data = {}
        self.output_dir = Path(__file__).parent.parent.parent / "reports" / f"run_{run_id}"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def start_agent(self, agent_name: str, task_description: str, input_data: Dict[str, Any] = None):
        """Record agent start."""
        self.agents_data[agent_name] = {
            "name": agent_name,
            "task": task_description,
            "input": input_data or {},
            "tools_used": [],
            "output": None,
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "status": "running"
        }
        logger.info(f"🤖 Agent Started: {agent_name}")
        
    def log_tool_usage(self, agent_name: str, tool_name: str, tool_input: Dict[str, Any], tool_output: Any):
        """Log tool usage by an agent."""
        if agent_name not in self.agents_data:
            logger.warning(f"Agent {agent_name} not found in tracker")
            return
            
        tool_record = {
            "tool_name": tool_name,
            "input": tool_input,
            "output": str(tool_output)[:500],  # Truncate long outputs
            "timestamp": datetime.now().isoformat()
        }
        self.agents_data[agent_name]["tools_used"].append(tool_record)
        logger.info(f"🔧 Tool Used: {tool_name} by {agent_name}")
        
    def end_agent(self, agent_name: str, output: Any, status: str = "completed"):
        """Record agent completion."""
        if agent_name not in self.agents_data:
            logger.warning(f"Agent {agent_name} not found in tracker")
            return
            
        self.agents_data[agent_name]["output"] = output
        self.agents_data[agent_name]["end_time"] = datetime.now().isoformat()
        self.agents_data[agent_name]["status"] = status
        logger.info(f"✅ Agent Completed: {agent_name} (Status: {status})")
        
    def save_agent_report(self, agent_name: str):
        """Save individual agent report."""
        if agent_name not in self.agents_data:
            logger.warning(f"Agent {agent_name} not found in tracker")
            return
            
        agent_data = self.agents_data[agent_name]
        report_path = self.output_dir / f"{agent_name}_report.json"
        
        with open(report_path, 'w') as f:
            json.dump(agent_data, f, indent=2, default=str)
        
        logger.info(f"📄 Agent Report Saved: {report_path}")
        
    def save_all_reports(self):
        """Save all agent reports."""
        for agent_name in self.agents_data:
            self.save_agent_report(agent_name)
            
        # Save summary
        summary_path = self.output_dir / "agents_summary.json"
        summary = {
            "run_id": self.run_id,
            "timestamp": datetime.now().isoformat(),
            "agents": list(self.agents_data.keys()),
            "total_agents": len(self.agents_data),
            "agents_data": self.agents_data
        }
        
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        logger.info(f"📊 Summary Report Saved: {summary_path}")
        
    def print_agent_summary(self):
        """Print summary of all agents."""
        print("\n" + "="*80)
        print("🤖 AGENT EXECUTION SUMMARY")
        print("="*80)
        
        for agent_name, data in self.agents_data.items():
            print(f"\n📋 Agent: {agent_name}")
            print(f"   Status: {data['status']}")
            print(f"   Task: {data['task']}")
            print(f"   Tools Used: {len(data['tools_used'])}")
            
            for i, tool in enumerate(data['tools_used'], 1):
                print(f"      {i}. {tool['tool_name']}")
                print(f"         Input: {tool['input']}")
                print(f"         Output: {tool['output'][:100]}...")
                
            if data['output']:
                output_str = str(data['output'])[:200]
                print(f"   Output: {output_str}...")
                
        print("\n" + "="*80 + "\n")

