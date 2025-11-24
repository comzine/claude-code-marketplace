#!/usr/bin/env python3
"""
Agent Reuse Manager
Avoids regenerating automation for similar projects
Reuses successful configurations
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from difflib import SequenceMatcher

class AgentReuseManager:
    """Manages reuse of automation configurations"""

    def __init__(self, storage_path: str = ".claude/meta-automation/configurations"):
        self.storage_dir = Path(storage_path)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.index_path = self.storage_dir / "index.json"
        self.index = self._load_index()

    def _load_index(self) -> Dict:
        """Load configuration index"""
        if self.index_path.exists():
            try:
                with open(self.index_path, 'r') as f:
                    return json.load(f)
            except:
                return {'configurations': []}
        return {'configurations': []}

    def _save_index(self):
        """Save configuration index"""
        with open(self.index_path, 'w') as f:
            json.dump(self.index, f, indent=2)

    def save_configuration(self, config: Dict) -> str:
        """
        Save a successful automation configuration

        Args:
            config: {
                'project_type': str,
                'project_name': str,
                'tech_stack': List[str],
                'agents_used': List[str],
                'skills_generated': List[str],
                'commands_generated': List[str],
                'hooks_generated': List[str],
                'success_metrics': Dict,
                'user_satisfaction': int (1-5)
            }

        Returns:
            Configuration ID
        """
        config_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Add metadata
        config_with_meta = {
            **config,
            'config_id': config_id,
            'created_at': datetime.now().isoformat(),
            'reuse_count': 0
        }

        # Save full configuration
        config_path = self.storage_dir / f"{config_id}.json"
        with open(config_path, 'w') as f:
            json.dump(config_with_meta, f, indent=2)

        # Update index
        self.index['configurations'].append({
            'config_id': config_id,
            'project_type': config['project_type'],
            'project_name': config.get('project_name', 'unknown'),
            'tech_stack': config.get('tech_stack', []),
            'created_at': config_with_meta['created_at'],
            'reuse_count': 0
        })
        self._save_index()

        return config_id

    def find_similar_configurations(self, project_info: Dict, min_similarity: float = 0.7) -> List[Dict]:
        """
        Find similar configurations that could be reused

        Args:
            project_info: {
                'project_type': str,
                'tech_stack': List[str],
                'existing_tools': List[str]
            }
            min_similarity: Minimum similarity score (0-1)

        Returns:
            List of similar configurations sorted by similarity
        """
        similar = []

        for config_ref in self.index['configurations']:
            config = self._load_configuration(config_ref['config_id'])
            if not config:
                continue

            similarity = self._calculate_similarity(project_info, config)

            if similarity >= min_similarity:
                similar.append({
                    **config_ref,
                    'similarity': round(similarity, 2),
                    'full_config': config
                })

        # Sort by similarity (descending)
        similar.sort(key=lambda x: x['similarity'], reverse=True)

        return similar

    def _calculate_similarity(self, project_info: Dict, config: Dict) -> float:
        """
        Calculate similarity between project and configuration

        Returns:
            Similarity score 0-1
        """
        score = 0.0
        weights = {
            'project_type': 0.4,
            'tech_stack': 0.4,
            'size': 0.2
        }

        # Project type match
        if project_info.get('project_type') == config.get('project_type'):
            score += weights['project_type']

        # Tech stack similarity
        project_stack = set(project_info.get('tech_stack', []))
        config_stack = set(config.get('tech_stack', []))

        if project_stack and config_stack:
            intersection = len(project_stack & config_stack)
            union = len(project_stack | config_stack)
            tech_similarity = intersection / union if union > 0 else 0
            score += weights['tech_stack'] * tech_similarity

        return min(score, 1.0)

    def reuse_configuration(self, config_id: str) -> Dict:
        """
        Reuse a configuration

        Args:
            config_id: ID of configuration to reuse

        Returns:
            Configuration to apply
        """
        config = self._load_configuration(config_id)
        if not config:
            return None

        # Increment reuse count
        config['reuse_count'] += 1
        self._save_configuration(config_id, config)

        # Update index
        for cfg in self.index['configurations']:
            if cfg['config_id'] == config_id:
                cfg['reuse_count'] += 1
        self._save_index()

        return config

    def get_reuse_recommendation(self, project_info: Dict) -> Optional[Dict]:
        """
        Get recommendation for reusing a configuration

        Args:
            project_info: Information about current project

        Returns:
            Recommendation or None if no good match
        """
        similar = self.find_similar_configurations(project_info, min_similarity=0.75)

        if not similar:
            return None

        best_match = similar[0]

        return {
            'recommended': True,
            'config_id': best_match['config_id'],
            'similarity': best_match['similarity'],
            'project_name': best_match['project_name'],
            'created_at': best_match['created_at'],
            'reuse_count': best_match['reuse_count'],
            'time_saved': '5-10 minutes (no need to regenerate)',
            'agents': best_match['full_config']['agents_used'],
            'skills': best_match['full_config']['skills_generated'],
            'reason': f"This configuration was successful for a similar {best_match['project_type']} project"
        }

    def _load_configuration(self, config_id: str) -> Optional[Dict]:
        """Load a configuration file"""
        config_path = self.storage_dir / f"{config_id}.json"
        if not config_path.exists():
            return None

        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except:
            return None

    def _save_configuration(self, config_id: str, config: Dict):
        """Save a configuration file"""
        config_path = self.storage_dir / f"{config_id}.json"
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)

    def get_statistics(self) -> Dict:
        """Get reuse statistics"""
        total_configs = len(self.index['configurations'])
        total_reuses = sum(cfg['reuse_count'] for cfg in self.index['configurations'])

        project_types = {}
        for cfg in self.index['configurations']:
            ptype = cfg['project_type']
            if ptype not in project_types:
                project_types[ptype] = 0
            project_types[ptype] += 1

        return {
            'total_configurations': total_configs,
            'total_reuses': total_reuses,
            'average_reuses': round(total_reuses / total_configs, 1) if total_configs > 0 else 0,
            'project_types': project_types,
            'most_reused': sorted(
                self.index['configurations'],
                key=lambda x: x['reuse_count'],
                reverse=True
            )[:3]
        }

# Example usage
if __name__ == '__main__':
    manager = AgentReuseManager()

    # Save a configuration
    print("Saving successful configuration...")
    config_id = manager.save_configuration({
        'project_type': 'programming',
        'project_name': 'my-web-app',
        'tech_stack': ['TypeScript', 'React', 'Next.js'],
        'agents_used': ['project-analyzer', 'security-analyzer', 'test-coverage-analyzer'],
        'skills_generated': ['security-scanner', 'test-generator'],
        'commands_generated': ['/security-check', '/generate-tests'],
        'hooks_generated': ['pre-commit-security'],
        'success_metrics': {
            'time_saved': 50,
            'issues_prevented': 3
        },
        'user_satisfaction': 5
    })

    print(f"Saved configuration: {config_id}\n")

    # Find similar
    print("Finding similar configurations for new project...")
    similar = manager.find_similar_configurations({
        'project_type': 'programming',
        'tech_stack': ['TypeScript', 'React', 'Vite'],  # Similar but not exact
        'existing_tools': ['ESLint']
    })

    print(f"Found {len(similar)} similar configurations\n")

    if similar:
        print("Best match:")
        print(json.dumps({
            'config_id': similar[0]['config_id'],
            'similarity': similar[0]['similarity'],
            'project_name': similar[0]['project_name']
        }, indent=2))

        # Get recommendation
        print("\nRecommendation:")
        rec = manager.get_reuse_recommendation({
            'project_type': 'programming',
            'tech_stack': ['TypeScript', 'React', 'Vite']
        })
        print(json.dumps(rec, indent=2))

    # Statistics
    print("\nReuse Statistics:")
    stats = manager.get_statistics()
    print(json.dumps(stats, indent=2))
