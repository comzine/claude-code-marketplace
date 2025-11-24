#!/usr/bin/env python3
"""
Metrics Tracker
Tracks actual time saved vs estimates
Measures real impact of automation
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class MetricsTracker:
    """Tracks automation effectiveness metrics"""

    def __init__(self, session_id: str, storage_path: str = None):
        self.session_id = session_id
        if storage_path:
            self.storage_path = Path(storage_path)
        else:
            self.storage_path = Path(f".claude/meta-automation/metrics/{session_id}.json")

        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.metrics = self._load_or_create()

    def _load_or_create(self) -> Dict:
        """Load existing metrics or create new"""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, 'r') as f:
                    return json.load(f)
            except:
                return self._create_new()
        return self._create_new()

    def _create_new(self) -> Dict:
        """Create new metrics structure"""
        return {
            'session_id': self.session_id,
            'created_at': datetime.now().isoformat(),
            'project_info': {},
            'automation_generated': {
                'agents': [],
                'skills': [],
                'commands': [],
                'hooks': []
            },
            'time_tracking': {
                'setup_time_minutes': 0,
                'estimated_time_saved_hours': 0,
                'actual_time_saved_hours': 0,
                'accuracy': 0
            },
            'usage_metrics': {
                'skills_run_count': {},
                'commands_run_count': {},
                'automation_frequency': []
            },
            'value_metrics': {
                'issues_prevented': 0,
                'quality_improvements': [],
                'deployment_count': 0,
                'test_failures_caught': 0
            },
            'cost_metrics': {
                'setup_cost': 0,
                'ongoing_cost': 0,
                'total_cost': 0
            },
            'user_feedback': {
                'satisfaction_ratings': [],
                'comments': [],
                'pain_points_resolved': []
            }
        }

    def _save(self):
        """Save metrics to disk"""
        with open(self.storage_path, 'w') as f:
            json.dump(self.metrics, f, indent=2)

    def set_project_info(self, info: Dict):
        """Set project information"""
        self.metrics['project_info'] = {
            **info,
            'recorded_at': datetime.now().isoformat()
        }
        self._save()

    def record_automation_generated(self, category: str, items: List[str]):
        """
        Record what automation was generated

        Args:
            category: 'agents', 'skills', 'commands', 'hooks'
            items: List of generated items
        """
        if category in self.metrics['automation_generated']:
            self.metrics['automation_generated'][category].extend(items)
            self._save()

    def record_setup_time(self, minutes: int):
        """Record time spent setting up automation"""
        self.metrics['time_tracking']['setup_time_minutes'] = minutes
        self._save()

    def record_estimated_time_saved(self, hours: float):
        """Record estimated time savings"""
        self.metrics['time_tracking']['estimated_time_saved_hours'] = hours
        self._save()

    def record_actual_time_saved(self, hours: float, description: str):
        """
        Record actual time saved from automation

        Args:
            hours: Hours actually saved
            description: What was automated
        """
        current = self.metrics['time_tracking']['actual_time_saved_hours']
        self.metrics['time_tracking']['actual_time_saved_hours'] = current + hours

        # Calculate accuracy
        estimated = self.metrics['time_tracking']['estimated_time_saved_hours']
        if estimated > 0:
            actual = self.metrics['time_tracking']['actual_time_saved_hours']
            self.metrics['time_tracking']['accuracy'] = round((actual / estimated) * 100, 1)

        # Track individual savings
        if 'time_savings_breakdown' not in self.metrics:
            self.metrics['time_savings_breakdown'] = []

        self.metrics['time_savings_breakdown'].append({
            'hours_saved': hours,
            'description': description,
            'recorded_at': datetime.now().isoformat()
        })

        self._save()

    def record_skill_usage(self, skill_name: str):
        """Record that a skill was used"""
        if skill_name not in self.metrics['usage_metrics']['skills_run_count']:
            self.metrics['usage_metrics']['skills_run_count'][skill_name] = 0

        self.metrics['usage_metrics']['skills_run_count'][skill_name] += 1
        self._save()

    def record_command_usage(self, command_name: str):
        """Record that a command was used"""
        if command_name not in self.metrics['usage_metrics']['commands_run_count']:
            self.metrics['usage_metrics']['commands_run_count'][command_name] = 0

        self.metrics['usage_metrics']['commands_run_count'][command_name] += 1
        self._save()

    def record_issue_prevented(self, issue_type: str, description: str):
        """Record that automation prevented an issue"""
        self.metrics['value_metrics']['issues_prevented'] += 1

        if 'prevented_issues' not in self.metrics['value_metrics']:
            self.metrics['value_metrics']['prevented_issues'] = []

        self.metrics['value_metrics']['prevented_issues'].append({
            'type': issue_type,
            'description': description,
            'prevented_at': datetime.now().isoformat()
        })

        self._save()

    def record_quality_improvement(self, metric: str, before: float, after: float):
        """
        Record quality improvement

        Args:
            metric: What improved (e.g., 'test_coverage', 'build_success_rate')
            before: Value before automation
            after: Value after automation
        """
        improvement = {
            'metric': metric,
            'before': before,
            'after': after,
            'improvement_percent': round(((after - before) / before) * 100, 1) if before > 0 else 0,
            'recorded_at': datetime.now().isoformat()
        }

        self.metrics['value_metrics']['quality_improvements'].append(improvement)
        self._save()

    def record_user_feedback(self, rating: int, comment: str = None):
        """
        Record user satisfaction

        Args:
            rating: 1-5 rating
            comment: Optional comment
        """
        self.metrics['user_feedback']['satisfaction_ratings'].append({
            'rating': rating,
            'comment': comment,
            'recorded_at': datetime.now().isoformat()
        })

        self._save()

    def get_roi(self) -> Dict:
        """Calculate return on investment"""
        setup_time = self.metrics['time_tracking']['setup_time_minutes'] / 60  # hours
        actual_saved = self.metrics['time_tracking']['actual_time_saved_hours']

        if setup_time == 0:
            return {
                'roi': 0,
                'message': 'No setup time recorded'
            }

        roi = actual_saved / setup_time

        return {
            'roi': round(roi, 1),
            'setup_hours': round(setup_time, 1),
            'saved_hours': round(actual_saved, 1),
            'net_gain_hours': round(actual_saved - setup_time, 1),
            'break_even_reached': actual_saved > setup_time
        }

    def get_effectiveness(self) -> Dict:
        """Calculate automation effectiveness"""
        generated = self.metrics['automation_generated']
        usage = self.metrics['usage_metrics']

        total_generated = sum(len(items) for items in generated.values())
        total_used = (
            len(usage['skills_run_count']) +
            len(usage['commands_run_count'])
        )

        if total_generated == 0:
            return {
                'effectiveness': 0,
                'message': 'No automation generated yet'
            }

        effectiveness = (total_used / total_generated) * 100

        return {
            'effectiveness_percent': round(effectiveness, 1),
            'total_generated': total_generated,
            'total_used': total_used,
            'unused': total_generated - total_used
        }

    def get_summary(self) -> Dict:
        """Get comprehensive metrics summary"""
        roi = self.get_roi()
        effectiveness = self.get_effectiveness()

        avg_satisfaction = 0
        if self.metrics['user_feedback']['satisfaction_ratings']:
            ratings = [r['rating'] for r in self.metrics['user_feedback']['satisfaction_ratings']]
            avg_satisfaction = round(sum(ratings) / len(ratings), 1)

        return {
            'session_id': self.session_id,
            'project': self.metrics['project_info'].get('project_type', 'unknown'),
            'automation_generated': {
                category: len(items)
                for category, items in self.metrics['automation_generated'].items()
            },
            'time_metrics': {
                'setup_time_hours': round(self.metrics['time_tracking']['setup_time_minutes'] / 60, 1),
                'estimated_saved_hours': self.metrics['time_tracking']['estimated_time_saved_hours'],
                'actual_saved_hours': self.metrics['time_tracking']['actual_time_saved_hours'],
                'accuracy': f"{self.metrics['time_tracking']['accuracy']}%",
                'net_gain_hours': roi.get('net_gain_hours', 0)
            },
            'roi': roi,
            'effectiveness': effectiveness,
            'value': {
                'issues_prevented': self.metrics['value_metrics']['issues_prevented'],
                'quality_improvements_count': len(self.metrics['value_metrics']['quality_improvements']),
                'average_satisfaction': avg_satisfaction
            },
            'most_used': {
                'skills': sorted(
                    self.metrics['usage_metrics']['skills_run_count'].items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:3],
                'commands': sorted(
                    self.metrics['usage_metrics']['commands_run_count'].items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:3]
            }
        }

    def export_report(self) -> str:
        """Export formatted metrics report"""
        summary = self.get_summary()

        report = f"""
# Automation Metrics Report
**Session:** {summary['session_id']}
**Project Type:** {summary['project']}

## Automation Generated
- **Agents:** {summary['automation_generated']['agents']}
- **Skills:** {summary['automation_generated']['skills']}
- **Commands:** {summary['automation_generated']['commands']}
- **Hooks:** {summary['automation_generated']['hooks']}

## Time Savings
- **Setup Time:** {summary['time_metrics']['setup_time_hours']} hours
- **Estimated Savings:** {summary['time_metrics']['estimated_saved_hours']} hours
- **Actual Savings:** {summary['time_metrics']['actual_saved_hours']} hours
- **Accuracy:** {summary['time_metrics']['accuracy']}
- **Net Gain:** {summary['time_metrics']['net_gain_hours']} hours

## ROI
- **Return on Investment:** {summary['roi']['roi']}x
- **Break-Even:** {'✅ Yes' if summary['roi']['break_even_reached'] else '❌ Not yet'}

## Effectiveness
- **Usage Rate:** {summary['effectiveness']['effectiveness_percent']}%
- **Generated:** {summary['effectiveness']['total_generated']} items
- **Actually Used:** {summary['effectiveness']['total_used']} items
- **Unused:** {summary['effectiveness']['unused']} items

## Value Delivered
- **Issues Prevented:** {summary['value']['issues_prevented']}
- **Quality Improvements:** {summary['value']['quality_improvements_count']}
- **User Satisfaction:** {summary['value']['average_satisfaction']}/5

## Most Used Automation
"""

        if summary['most_used']['skills']:
            report += "\n**Skills:**\n"
            for skill, count in summary['most_used']['skills']:
                report += f"- {skill}: {count} times\n"

        if summary['most_used']['commands']:
            report += "\n**Commands:**\n"
            for cmd, count in summary['most_used']['commands']:
                report += f"- {cmd}: {count} times\n"

        return report

# Example usage
if __name__ == '__main__':
    tracker = MetricsTracker('test-session-123')

    # Simulate automation setup
    tracker.set_project_info({
        'project_type': 'programming',
        'project_name': 'my-web-app'
    })

    tracker.record_automation_generated('skills', ['security-scanner', 'test-generator'])
    tracker.record_automation_generated('commands', ['/security-check', '/generate-tests'])

    tracker.record_setup_time(30)  # 30 minutes to set up
    tracker.record_estimated_time_saved(50)  # Estimated 50 hours saved

    # Simulate usage over time
    tracker.record_skill_usage('security-scanner')
    tracker.record_skill_usage('security-scanner')
    tracker.record_skill_usage('test-generator')

    tracker.record_command_usage('/security-check')

    # Record actual time saved
    tracker.record_actual_time_saved(5, 'Security scan caught 3 vulnerabilities before deployment')
    tracker.record_actual_time_saved(8, 'Auto-generated 15 test scaffolds')

    # Record quality improvements
    tracker.record_quality_improvement('test_coverage', 42, 75)

    # Record issues prevented
    tracker.record_issue_prevented('security', 'SQL injection vulnerability caught')

    # User feedback
    tracker.record_user_feedback(5, 'This saved me so much time!')

    print(tracker.export_report())
