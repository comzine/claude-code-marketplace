#!/usr/bin/env python3
"""
Simple Project Metrics Collector
Just collects basic data - NO decision making or pattern matching
The project-analyzer agent does the intelligent analysis
"""

import json
from pathlib import Path
from collections import defaultdict
from typing import Dict

class ProjectMetricsCollector:
    """Collects basic project metrics for agent analysis"""

    def __init__(self, project_root: str = "."):
        self.root = Path(project_root).resolve()

    def collect_metrics(self) -> Dict:
        """Collect basic project metrics"""
        return {
            'file_analysis': self._analyze_files(),
            'directory_structure': self._get_directory_structure(),
            'key_files': self._find_key_files(),
            'project_stats': self._get_basic_stats()
        }

    def _analyze_files(self) -> Dict:
        """Count files by category"""
        type_categories = {
            'code': {'.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.go', '.rs', '.c', '.cpp', '.php', '.rb'},
            'markup': {'.html', '.xml', '.svg'},
            'stylesheet': {'.css', '.scss', '.sass', '.less'},
            'document': {'.md', '.txt', '.pdf', '.doc', '.docx', '.odt'},
            'latex': {'.tex', '.bib', '.cls', '.sty'},
            'spreadsheet': {'.xlsx', '.xls', '.ods', '.csv'},
            'image': {'.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp'},
            'video': {'.mp4', '.avi', '.mov', '.mkv'},
            'data': {'.json', '.yaml', '.yml', '.toml', '.xml'},
            'notebook': {'.ipynb'},
        }

        counts = defaultdict(int)
        files_by_type = defaultdict(list)

        for item in self.root.rglob('*'):
            if item.is_file() and not self._is_ignored(item):
                suffix = item.suffix.lower()
                categorized = False

                for category, extensions in type_categories.items():
                    if suffix in extensions:
                        counts[category] += 1
                        files_by_type[category].append(str(item.relative_to(self.root)))
                        categorized = True
                        break

                if not categorized:
                    counts['other'] += 1

        total = sum(counts.values()) or 1

        return {
            'counts': dict(counts),
            'percentages': {k: round((v / total) * 100, 1) for k, v in counts.items()},
            'total_files': total,
            'sample_files': {k: v[:5] for k, v in files_by_type.items()}  # First 5 of each type
        }

    def _get_directory_structure(self) -> Dict:
        """Get top-level directory structure"""
        dirs = []
        for item in self.root.iterdir():
            if item.is_dir() and not self._is_ignored(item):
                file_count = sum(1 for _ in item.rglob('*') if _.is_file())
                dirs.append({
                    'name': item.name,
                    'file_count': file_count
                })

        return {
            'top_level_directories': sorted(dirs, key=lambda x: x['file_count'], reverse=True),
            'total_directories': len(dirs)
        }

    def _find_key_files(self) -> Dict:
        """Find common configuration and important files"""
        key_patterns = {
            # Programming
            'package.json': 'Node.js project',
            'requirements.txt': 'Python project',
            'Cargo.toml': 'Rust project',
            'go.mod': 'Go project',
            'pom.xml': 'Java Maven project',
            'build.gradle': 'Java Gradle project',

            # Configuration
            '.eslintrc*': 'ESLint config',
            'tsconfig.json': 'TypeScript config',
            'jest.config.js': 'Jest testing',
            'pytest.ini': 'Pytest config',

            # CI/CD
            '.github/workflows': 'GitHub Actions',
            '.gitlab-ci.yml': 'GitLab CI',
            'Jenkinsfile': 'Jenkins',

            # Hooks
            '.pre-commit-config.yaml': 'Pre-commit hooks',
            '.husky': 'Husky hooks',

            # Documentation
            'README.md': 'README',
            'CONTRIBUTING.md': 'Contribution guide',
            'LICENSE': 'License file',

            # LaTeX
            'main.tex': 'LaTeX main',
            '*.bib': 'Bibliography',

            # Build tools
            'Makefile': 'Makefile',
            'CMakeLists.txt': 'CMake',
            'docker-compose.yml': 'Docker Compose',
            'Dockerfile': 'Docker',
        }

        found = {}
        for pattern, description in key_patterns.items():
            matches = list(self.root.glob(pattern))
            if matches:
                found[pattern] = {
                    'description': description,
                    'count': len(matches),
                    'paths': [str(m.relative_to(self.root)) for m in matches[:3]]
                }

        return found

    def _get_basic_stats(self) -> Dict:
        """Get basic project statistics"""
        total_files = 0
        total_dirs = 0
        total_size = 0
        max_depth = 0

        for item in self.root.rglob('*'):
            if self._is_ignored(item):
                continue

            if item.is_file():
                total_files += 1
                try:
                    total_size += item.stat().st_size
                except:
                    pass

                depth = len(item.relative_to(self.root).parts)
                max_depth = max(max_depth, depth)
            elif item.is_dir():
                total_dirs += 1

        return {
            'total_files': total_files,
            'total_directories': total_dirs,
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'deepest_nesting': max_depth
        }

    def _is_ignored(self, path: Path) -> bool:
        """Check if path should be ignored"""
        ignore_patterns = {
            'node_modules', '.git', '__pycache__', '.venv', 'venv',
            'dist', 'build', '.cache', '.pytest_cache', 'coverage',
            '.next', '.nuxt', 'out', 'target'
        }

        parts = path.parts
        return any(pattern in parts for pattern in ignore_patterns)

    def generate_report(self) -> Dict:
        """Generate complete metrics report"""
        metrics = self.collect_metrics()

        return {
            'project_root': str(self.root),
            'scan_purpose': 'Basic metrics collection for intelligent agent analysis',
            'metrics': metrics,
            'note': 'This is raw data. The project-analyzer agent will interpret it intelligently.'
        }

if __name__ == '__main__':
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    collector = ProjectMetricsCollector(path)
    report = collector.generate_report()
    print(json.dumps(report, indent=2))
