#!/usr/bin/env python3
"""
Cost & Performance Estimator
Provides transparent estimates for automation operations
"""

import json
from typing import Dict, List
from dataclasses import dataclass, asdict

@dataclass
class AgentEstimate:
    """Estimate for a single agent"""
    agent_name: str
    description: str
    estimated_tokens: int
    estimated_minutes: int
    priority: str  # high, medium, low
    purpose: str

@dataclass
class AutomationEstimate:
    """Complete automation estimate"""
    mode: str  # quick, focused, comprehensive
    total_agents: int
    agents: List[AgentEstimate]
    total_tokens_min: int
    total_tokens_max: int
    total_minutes_min: int
    total_minutes_max: int
    total_cost_min: float
    total_cost_max: float
    recommendations: List[str]

class CostEstimator:
    """Estimates cost and time for automation"""

    # Token costs (as of Jan 2025, Claude Sonnet)
    TOKEN_COST_INPUT = 0.000003  # $3 per 1M input tokens
    TOKEN_COST_OUTPUT = 0.000015  # $15 per 1M output tokens

    # Approximate tokens per agent type
    AGENT_TOKEN_ESTIMATES = {
        'project-analyzer': {'input': 2000, 'output': 1500, 'minutes': 3},
        'structure-analyzer': {'input': 1000, 'output': 800, 'minutes': 2},
        'security-analyzer': {'input': 1500, 'output': 1000, 'minutes': 3},
        'performance-analyzer': {'input': 1500, 'output': 1000, 'minutes': 4},
        'test-coverage-analyzer': {'input': 1200, 'output': 800, 'minutes': 3},
        'latex-structure-analyzer': {'input': 1000, 'output': 800, 'minutes': 3},
        'citation-analyzer': {'input': 800, 'output': 600, 'minutes': 2},
        'link-validator': {'input': 1000, 'output': 700, 'minutes': 2},
    }

    # Default estimate for unknown agents
    DEFAULT_ESTIMATE = {'input': 1000, 'output': 800, 'minutes': 3}

    def estimate_agent(self, agent_name: str, priority: str = 'medium', purpose: str = '') -> AgentEstimate:
        """
        Estimate cost/time for a single agent

        Args:
            agent_name: Name of the agent
            priority: high, medium, or low
            purpose: What this agent does

        Returns:
            AgentEstimate object
        """
        estimate = self.AGENT_TOKEN_ESTIMATES.get(agent_name, self.DEFAULT_ESTIMATE)

        total_tokens = estimate['input'] + estimate['output']
        minutes = estimate['minutes']

        return AgentEstimate(
            agent_name=agent_name,
            description=purpose or f"Analyzes {agent_name.replace('-', ' ')}",
            estimated_tokens=total_tokens,
            estimated_minutes=minutes,
            priority=priority,
            purpose=purpose
        )

    def estimate_quick_mode(self) -> AutomationEstimate:
        """Estimate for quick analysis mode"""
        agents = [
            self.estimate_agent('project-analyzer', 'high', 'Intelligent project analysis'),
        ]

        return self._calculate_total_estimate('quick', agents, [
            'Fastest way to understand your project',
            'Low cost, high value',
            'Can expand to full automation after'
        ])

    def estimate_focused_mode(self, focus_areas: List[str]) -> AutomationEstimate:
        """Estimate for focused automation mode"""
        # Map focus areas to agents
        area_to_agents = {
            'security': ['security-analyzer'],
            'testing': ['test-coverage-analyzer'],
            'performance': ['performance-analyzer'],
            'structure': ['structure-analyzer'],
            'latex': ['latex-structure-analyzer', 'citation-analyzer'],
            'links': ['link-validator'],
        }

        agents = [self.estimate_agent('project-analyzer', 'high', 'Initial analysis')]

        for area in focus_areas:
            for agent_name in area_to_agents.get(area, []):
                agents.append(self.estimate_agent(agent_name, 'high', f'Analyze {area}'))

        return self._calculate_total_estimate('focused', agents, [
            'Targeted automation for your specific needs',
            'Medium cost, high relevance',
            'Focuses on what matters most to you'
        ])

    def estimate_comprehensive_mode(self, project_type: str) -> AutomationEstimate:
        """Estimate for comprehensive automation mode"""
        agents = [
            self.estimate_agent('project-analyzer', 'high', 'Project analysis'),
            self.estimate_agent('structure-analyzer', 'high', 'Structure analysis'),
        ]

        # Add type-specific agents
        if project_type in ['programming', 'web_app', 'cli']:
            agents.extend([
                self.estimate_agent('security-analyzer', 'high', 'Security audit'),
                self.estimate_agent('performance-analyzer', 'medium', 'Performance check'),
                self.estimate_agent('test-coverage-analyzer', 'high', 'Test coverage'),
            ])

        elif project_type in ['academic_writing', 'research']:
            agents.extend([
                self.estimate_agent('latex-structure-analyzer', 'high', 'LaTeX structure'),
                self.estimate_agent('citation-analyzer', 'high', 'Citations & bibliography'),
                self.estimate_agent('link-validator', 'medium', 'Link validation'),
            ])

        return self._calculate_total_estimate('comprehensive', agents, [
            'Complete automation system',
            'Highest cost, most comprehensive',
            'Full agent suite, skills, commands, hooks'
        ])

    def _calculate_total_estimate(self, mode: str, agents: List[AgentEstimate], recommendations: List[str]) -> AutomationEstimate:
        """Calculate total estimates from agent list"""
        total_tokens = sum(a.estimated_tokens for a in agents)
        total_minutes = max(5, sum(a.estimated_minutes for a in agents) // 2)  # Parallel execution

        # Add buffer (20-50% uncertainty)
        tokens_min = total_tokens
        tokens_max = int(total_tokens * 1.5)
        minutes_min = total_minutes
        minutes_max = int(total_minutes * 1.3)

        # Calculate costs (rough approximation: 60% input, 40% output)
        cost_min = (tokens_min * 0.6 * self.TOKEN_COST_INPUT) + (tokens_min * 0.4 * self.TOKEN_COST_OUTPUT)
        cost_max = (tokens_max * 0.6 * self.TOKEN_COST_INPUT) + (tokens_max * 0.4 * self.TOKEN_COST_OUTPUT)

        return AutomationEstimate(
            mode=mode,
            total_agents=len(agents),
            agents=agents,
            total_tokens_min=tokens_min,
            total_tokens_max=tokens_max,
            total_minutes_min=minutes_min,
            total_minutes_max=minutes_max,
            total_cost_min=round(cost_min, 3),
            total_cost_max=round(cost_max, 3),
            recommendations=recommendations
        )

    def format_estimate(self, estimate: AutomationEstimate) -> str:
        """Format estimate for display"""
        lines = []

        lines.append(f"╔══════════════════════════════════════════════════╗")
        lines.append(f"║ Automation Estimate - {estimate.mode.upper()} Mode")
        lines.append(f"╚══════════════════════════════════════════════════╝")
        lines.append("")

        # Agent list
        for agent in estimate.agents:
            priority_icon = "⭐" if agent.priority == "high" else "•"
            lines.append(f"{priority_icon} {agent.agent_name}")
            lines.append(f"   {agent.description}")
            lines.append(f"   ⏱️  ~{agent.estimated_minutes} min | 💰 ~{agent.estimated_tokens} tokens")
            lines.append("")

        lines.append("────────────────────────────────────────────────────")

        # Totals
        lines.append(f"Total Agents: {estimate.total_agents}")
        lines.append(f"Estimated Time: {estimate.total_minutes_min}-{estimate.total_minutes_max} minutes")
        lines.append(f"Estimated Tokens: {estimate.total_tokens_min:,}-{estimate.total_tokens_max:,}")
        lines.append(f"Estimated Cost: ${estimate.total_cost_min:.3f}-${estimate.total_cost_max:.3f}")

        lines.append("")
        lines.append("💡 Notes:")
        for rec in estimate.recommendations:
            lines.append(f"   • {rec}")

        return "\n".join(lines)

    def export_estimate(self, estimate: AutomationEstimate, output_path: str = None) -> Dict:
        """Export estimate as JSON"""
        data = asdict(estimate)

        if output_path:
            with open(output_path, 'w') as f:
                json.dump(data, f, indent=2)

        return data

# Example usage
if __name__ == '__main__':
    estimator = CostEstimator()

    print("1. QUICK MODE ESTIMATE")
    print("="*60)
    quick = estimator.estimate_quick_mode()
    print(estimator.format_estimate(quick))

    print("\n\n2. FOCUSED MODE ESTIMATE (Security + Testing)")
    print("="*60)
    focused = estimator.estimate_focused_mode(['security', 'testing'])
    print(estimator.format_estimate(focused))

    print("\n\n3. COMPREHENSIVE MODE ESTIMATE (Programming Project)")
    print("="*60)
    comprehensive = estimator.estimate_comprehensive_mode('programming')
    print(estimator.format_estimate(comprehensive))
