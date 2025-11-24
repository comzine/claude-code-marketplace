#!/usr/bin/env python3
"""
User Preference Learning
Learns from user's choices to provide better recommendations over time
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from collections import defaultdict

class UserPreferences:
    """Learns and stores user preferences for automation"""

    def __init__(self, storage_path: str = ".claude/meta-automation/user_preferences.json"):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.preferences = self._load()

    def _load(self) -> Dict:
        """Load existing preferences or create new"""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, 'r') as f:
                    return json.load(f)
            except:
                return self._create_new()
        return self._create_new()

    def _create_new(self) -> Dict:
        """Create new preferences structure"""
        return {
            'version': '1.0',
            'created_at': datetime.now().isoformat(),
            'projects_analyzed': 0,
            'automation_mode_preferences': {
                'quick': 0,
                'focused': 0,
                'comprehensive': 0
            },
            'agent_usage': {},
            'skill_usage': {},
            'project_type_history': {},
            'time_saved_total': 0,
            'cost_spent_total': 0,
            'satisfaction_ratings': [],
            'most_valuable_automations': [],
            'rarely_used': [],
            'integration_preferences': {
                'focus_on_gaps': 0,
                'enhance_existing': 0,
                'independent': 0
            },
            'sessions': []
        }

    def _save(self):
        """Save preferences to disk"""
        with open(self.storage_path, 'w') as f:
            json.dump(self.preferences, f, indent=2)

    def record_session(self, session_data: Dict):
        """
        Record a new automation session

        Args:
            session_data: {
                'session_id': str,
                'project_type': str,
                'mode': 'quick|focused|comprehensive',
                'agents_used': List[str],
                'skills_generated': List[str],
                'time_spent_minutes': int,
                'cost': float,
                'time_saved_estimate': int,  # hours
                'user_satisfaction': int,  # 1-5
                'integration_choice': str,  # gaps|enhance|independent
            }
        """
        # Update counts
        self.preferences['projects_analyzed'] += 1

        # Record mode preference
        mode = session_data.get('mode', 'quick')
        self.preferences['automation_mode_preferences'][mode] += 1

        # Record agent usage
        for agent in session_data.get('agents_used', []):
            if agent not in self.preferences['agent_usage']:
                self.preferences['agent_usage'][agent] = 0
            self.preferences['agent_usage'][agent] += 1

        # Record skill usage
        for skill in session_data.get('skills_generated', []):
            if skill not in self.preferences['skill_usage']:
                self.preferences['skill_usage'][skill] = 0
            self.preferences['skill_usage'][skill] += 1

        # Record project type
        project_type = session_data.get('project_type', 'unknown')
        if project_type not in self.preferences['project_type_history']:
            self.preferences['project_type_history'][project_type] = 0
        self.preferences['project_type_history'][project_type] += 1

        # Track totals
        self.preferences['time_saved_total'] += session_data.get('time_saved_estimate', 0)
        self.preferences['cost_spent_total'] += session_data.get('cost', 0)

        # Track satisfaction
        satisfaction = session_data.get('user_satisfaction')
        if satisfaction:
            self.preferences['satisfaction_ratings'].append({
                'session_id': session_data.get('session_id'),
                'rating': satisfaction,
                'date': datetime.now().isoformat()
            })

        # Track integration preference
        integration = session_data.get('integration_choice')
        if integration in self.preferences['integration_preferences']:
            self.preferences['integration_preferences'][integration] += 1

        # Store full session
        self.preferences['sessions'].append({
            **session_data,
            'recorded_at': datetime.now().isoformat()
        })

        self._save()

    def get_recommended_mode(self) -> str:
        """Get recommended automation mode based on history"""
        prefs = self.preferences['automation_mode_preferences']

        if self.preferences['projects_analyzed'] == 0:
            return 'quick'  # Default for first-time users

        # Return mode user uses most
        return max(prefs.items(), key=lambda x: x[1])[0]

    def get_recommended_agents(self, project_type: str, count: int = 5) -> List[str]:
        """Get recommended agents based on past usage and project type"""
        # Get agents user has used
        agent_usage = self.preferences['agent_usage']

        if not agent_usage:
            # Default recommendations for new users
            defaults = {
                'programming': ['project-analyzer', 'security-analyzer', 'test-coverage-analyzer'],
                'academic_writing': ['project-analyzer', 'latex-structure-analyzer', 'citation-analyzer'],
                'educational': ['project-analyzer', 'learning-path-analyzer', 'assessment-analyzer'],
            }
            return defaults.get(project_type, ['project-analyzer'])

        # Sort by usage count
        sorted_agents = sorted(agent_usage.items(), key=lambda x: x[1], reverse=True)

        return [agent for agent, _ in sorted_agents[:count]]

    def get_rarely_used(self) -> List[str]:
        """Get agents/skills that user never finds valuable"""
        rarely_used = []

        # Check for agents used only once or twice
        for agent, count in self.preferences['agent_usage'].items():
            if count <= 2 and self.preferences['projects_analyzed'] > 5:
                rarely_used.append(agent)

        return rarely_used

    def should_skip_agent(self, agent_name: str) -> bool:
        """Check if this agent is rarely useful for this user"""
        rarely_used = self.get_rarely_used()
        return agent_name in rarely_used

    def get_integration_preference(self) -> str:
        """Get preferred integration approach"""
        prefs = self.preferences['integration_preferences']

        if sum(prefs.values()) == 0:
            return 'focus_on_gaps'  # Default

        return max(prefs.items(), key=lambda x: x[1])[0]

    def get_statistics(self) -> Dict:
        """Get usage statistics"""
        total_sessions = self.preferences['projects_analyzed']

        if total_sessions == 0:
            return {
                'total_sessions': 0,
                'message': 'No automation sessions yet'
            }

        avg_satisfaction = 0
        if self.preferences['satisfaction_ratings']:
            avg_satisfaction = sum(r['rating'] for r in self.preferences['satisfaction_ratings']) / len(self.preferences['satisfaction_ratings'])

        return {
            'total_sessions': total_sessions,
            'time_saved_total_hours': self.preferences['time_saved_total'],
            'cost_spent_total': round(self.preferences['cost_spent_total'], 2),
            'average_satisfaction': round(avg_satisfaction, 1),
            'preferred_mode': self.get_recommended_mode(),
            'most_used_agents': sorted(
                self.preferences['agent_usage'].items(),
                key=lambda x: x[1],
                reverse=True
            )[:5],
            'project_types': self.preferences['project_type_history'],
            'roi': round(self.preferences['time_saved_total'] / max(1, self.preferences['cost_spent_total'] * 60), 1)
        }

    def get_recommendations_for_user(self, project_type: str) -> Dict:
        """Get personalized recommendations"""
        stats = self.get_statistics()

        if stats['total_sessions'] == 0:
            return {
                'recommended_mode': 'quick',
                'reason': 'First time - start with quick analysis to see how it works',
                'recommended_agents': ['project-analyzer'],
                'skip_agents': []
            }

        return {
            'recommended_mode': self.get_recommended_mode(),
            'reason': f"You've used {self.get_recommended_mode()} mode {self.preferences['automation_mode_preferences'][self.get_recommended_mode()]} times",
            'recommended_agents': self.get_recommended_agents(project_type),
            'skip_agents': self.get_rarely_used(),
            'integration_preference': self.get_integration_preference(),
            'stats': {
                'total_time_saved': f"{stats['time_saved_total_hours']} hours",
                'average_satisfaction': stats.get('average_satisfaction', 0),
                'roi': f"{stats.get('roi', 0)}x return on investment"
            }
        }

    def export_report(self) -> str:
        """Export usage report"""
        stats = self.get_statistics()

        report = f"""
# Meta-Automation Usage Report

## Overview
- **Total Sessions:** {stats['total_sessions']}
- **Time Saved:** {stats.get('time_saved_total_hours', 0)} hours
- **Cost Spent:** ${stats.get('cost_spent_total', 0):.2f}
- **ROI:** {stats.get('roi', 0)}x (hours saved per dollar spent × 60)
- **Avg Satisfaction:** {stats.get('average_satisfaction', 0)}/5

## Your Preferences
- **Preferred Mode:** {stats.get('preferred_mode', 'quick')}
- **Integration Style:** {self.get_integration_preference()}

## Most Used Agents
"""

        for agent, count in stats.get('most_used_agents', []):
            report += f"- {agent}: {count} times\n"

        report += "\n## Project Types\n"
        for ptype, count in self.preferences['project_type_history'].items():
            report += f"- {ptype}: {count} projects\n"

        return report

# Example usage
if __name__ == '__main__':
    prefs = UserPreferences()

    # Simulate some sessions
    print("Simulating usage...\n")

    prefs.record_session({
        'session_id': 'session-1',
        'project_type': 'programming',
        'mode': 'quick',
        'agents_used': ['project-analyzer'],
        'skills_generated': [],
        'time_spent_minutes': 5,
        'cost': 0.03,
        'time_saved_estimate': 10,
        'user_satisfaction': 4,
        'integration_choice': 'focus_on_gaps'
    })

    prefs.record_session({
        'session_id': 'session-2',
        'project_type': 'programming',
        'mode': 'focused',
        'agents_used': ['project-analyzer', 'security-analyzer', 'test-coverage-analyzer'],
        'skills_generated': ['security-scanner', 'test-generator'],
        'time_spent_minutes': 8,
        'cost': 0.09,
        'time_saved_estimate': 50,
        'user_satisfaction': 5,
        'integration_choice': 'focus_on_gaps'
    })

    print(prefs.export_report())

    print("\nRecommendations for next programming project:")
    recs = prefs.get_recommendations_for_user('programming')
    print(json.dumps(recs, indent=2))
