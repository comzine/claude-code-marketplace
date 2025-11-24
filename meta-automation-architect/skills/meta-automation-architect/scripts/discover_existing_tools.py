#!/usr/bin/env python3
"""
Existing Tool Discovery
Checks what automation tools are already in place
Prevents duplication and suggests integration points
"""

import json
from pathlib import Path
from typing import Dict, List
from collections import defaultdict

class ExistingToolDiscovery:
    """Discovers existing automation tools in a project"""

    def __init__(self, project_root: str = "."):
        self.root = Path(project_root).resolve()

    def discover_all(self) -> Dict:
        """Discover all existing automation tools"""
        return {
            'linting': self._discover_linting(),
            'testing': self._discover_testing(),
            'ci_cd': self._discover_ci_cd(),
            'git_hooks': self._discover_git_hooks(),
            'formatting': self._discover_formatting(),
            'security': self._discover_security(),
            'documentation': self._discover_documentation(),
            'summary': self._generate_summary()
        }

    def _discover_linting(self) -> Dict:
        """Find linting tools"""
        tools = {}

        linting_patterns = {
            '.eslintrc*': {'tool': 'ESLint', 'language': 'JavaScript/TypeScript', 'purpose': 'Code linting'},
            '.pylintrc': {'tool': 'Pylint', 'language': 'Python', 'purpose': 'Code linting'},
            'pylint.rc': {'tool': 'Pylint', 'language': 'Python', 'purpose': 'Code linting'},
            '.flake8': {'tool': 'Flake8', 'language': 'Python', 'purpose': 'Code linting'},
            'tslint.json': {'tool': 'TSLint', 'language': 'TypeScript', 'purpose': 'Code linting'},
            '.rubocop.yml': {'tool': 'RuboCop', 'language': 'Ruby', 'purpose': 'Code linting'},
            'phpcs.xml': {'tool': 'PHP_CodeSniffer', 'language': 'PHP', 'purpose': 'Code linting'},
        }

        for pattern, info in linting_patterns.items():
            matches = list(self.root.glob(pattern))
            if matches:
                tools[info['tool']] = {
                    **info,
                    'config_file': str(matches[0].relative_to(self.root)),
                    'found': True
                }

        return {
            'tools_found': tools,
            'count': len(tools),
            'recommendation': self._linting_recommendation(tools)
        }

    def _discover_testing(self) -> Dict:
        """Find testing frameworks"""
        tools = {}

        testing_patterns = {
            'jest.config.js': {'tool': 'Jest', 'language': 'JavaScript', 'purpose': 'Unit testing'},
            'jest.config.ts': {'tool': 'Jest', 'language': 'TypeScript', 'purpose': 'Unit testing'},
            'pytest.ini': {'tool': 'Pytest', 'language': 'Python', 'purpose': 'Unit testing'},
            'phpunit.xml': {'tool': 'PHPUnit', 'language': 'PHP', 'purpose': 'Unit testing'},
            'karma.conf.js': {'tool': 'Karma', 'language': 'JavaScript', 'purpose': 'Test runner'},
            '.rspec': {'tool': 'RSpec', 'language': 'Ruby', 'purpose': 'Testing'},
            'go.mod': {'tool': 'Go test', 'language': 'Go', 'purpose': 'Testing'},
        }

        for pattern, info in testing_patterns.items():
            matches = list(self.root.glob(pattern))
            if matches:
                tools[info['tool']] = {
                    **info,
                    'config_file': str(matches[0].relative_to(self.root)),
                    'found': True
                }

        # Check for test directories
        test_dirs = []
        for pattern in ['tests/', 'test/', '__tests__/', 'spec/']:
            if (self.root / pattern).exists():
                test_dirs.append(pattern)

        return {
            'tools_found': tools,
            'test_directories': test_dirs,
            'count': len(tools),
            'recommendation': self._testing_recommendation(tools, test_dirs)
        }

    def _discover_ci_cd(self) -> Dict:
        """Find CI/CD configurations"""
        tools = {}

        ci_patterns = {
            '.github/workflows': {'tool': 'GitHub Actions', 'platform': 'GitHub', 'purpose': 'CI/CD'},
            '.gitlab-ci.yml': {'tool': 'GitLab CI', 'platform': 'GitLab', 'purpose': 'CI/CD'},
            '.circleci/config.yml': {'tool': 'CircleCI', 'platform': 'CircleCI', 'purpose': 'CI/CD'},
            'Jenkinsfile': {'tool': 'Jenkins', 'platform': 'Jenkins', 'purpose': 'CI/CD'},
            '.travis.yml': {'tool': 'Travis CI', 'platform': 'Travis', 'purpose': 'CI/CD'},
            'azure-pipelines.yml': {'tool': 'Azure Pipelines', 'platform': 'Azure', 'purpose': 'CI/CD'},
            '.drone.yml': {'tool': 'Drone CI', 'platform': 'Drone', 'purpose': 'CI/CD'},
        }

        for pattern, info in ci_patterns.items():
            path = self.root / pattern
            if path.exists():
                tools[info['tool']] = {
                    **info,
                    'config': str(Path(pattern)),
                    'found': True
                }

        return {
            'tools_found': tools,
            'count': len(tools),
            'recommendation': self._ci_cd_recommendation(tools)
        }

    def _discover_git_hooks(self) -> Dict:
        """Find git hooks configuration"""
        tools = {}

        hook_patterns = {
            '.pre-commit-config.yaml': {'tool': 'pre-commit', 'purpose': 'Pre-commit hooks'},
            '.husky': {'tool': 'Husky', 'purpose': 'Git hooks (Node.js)'},
            '.git/hooks': {'tool': 'Native Git hooks', 'purpose': 'Git hooks'},
            'lefthook.yml': {'tool': 'Lefthook', 'purpose': 'Git hooks'},
        }

        for pattern, info in hook_patterns.items():
            path = self.root / pattern
            if path.exists():
                tools[info['tool']] = {
                    **info,
                    'location': str(Path(pattern)),
                    'found': True
                }

        return {
            'tools_found': tools,
            'count': len(tools),
            'recommendation': self._git_hooks_recommendation(tools)
        }

    def _discover_formatting(self) -> Dict:
        """Find code formatting tools"""
        tools = {}

        formatting_patterns = {
            '.prettierrc*': {'tool': 'Prettier', 'language': 'JavaScript/TypeScript', 'purpose': 'Code formatting'},
            '.editorconfig': {'tool': 'EditorConfig', 'language': 'Universal', 'purpose': 'Editor settings'},
            'pyproject.toml': {'tool': 'Black (if configured)', 'language': 'Python', 'purpose': 'Code formatting'},
            '.php-cs-fixer.php': {'tool': 'PHP-CS-Fixer', 'language': 'PHP', 'purpose': 'Code formatting'},
        }

        for pattern, info in formatting_patterns.items():
            matches = list(self.root.glob(pattern))
            if matches:
                tools[info['tool']] = {
                    **info,
                    'config_file': str(matches[0].relative_to(self.root)),
                    'found': True
                }

        return {
            'tools_found': tools,
            'count': len(tools),
            'recommendation': self._formatting_recommendation(tools)
        }

    def _discover_security(self) -> Dict:
        """Find security scanning tools"""
        tools = {}

        # Check for dependency scanning
        if (self.root / 'package.json').exists():
            tools['npm audit'] = {
                'tool': 'npm audit',
                'platform': 'Node.js',
                'purpose': 'Dependency scanning',
                'found': True
            }

        if (self.root / 'Pipfile').exists():
            tools['pipenv check'] = {
                'tool': 'pipenv check',
                'platform': 'Python',
                'purpose': 'Dependency scanning',
                'found': True
            }

        # Check for security configs
        security_patterns = {
            '.snyk': {'tool': 'Snyk', 'purpose': 'Security scanning'},
            'sonar-project.properties': {'tool': 'SonarQube', 'purpose': 'Code quality & security'},
        }

        for pattern, info in security_patterns.items():
            if (self.root / pattern).exists():
                tools[info['tool']] = {
                    **info,
                    'config': pattern,
                    'found': True
                }

        return {
            'tools_found': tools,
            'count': len(tools),
            'recommendation': self._security_recommendation(tools)
        }

    def _discover_documentation(self) -> Dict:
        """Find documentation tools"""
        tools = {}

        doc_patterns = {
            'mkdocs.yml': {'tool': 'MkDocs', 'purpose': 'Documentation site'},
            'docusaurus.config.js': {'tool': 'Docusaurus', 'purpose': 'Documentation site'},
            'conf.py': {'tool': 'Sphinx', 'purpose': 'Documentation (Python)'},
            'jsdoc.json': {'tool': 'JSDoc', 'purpose': 'JavaScript documentation'},
            '.readthedocs.yml': {'tool': 'ReadTheDocs', 'purpose': 'Documentation hosting'},
        }

        for pattern, info in doc_patterns.items():
            if (self.root / pattern).exists():
                tools[info['tool']] = {
                    **info,
                    'config': pattern,
                    'found': True
                }

        return {
            'tools_found': tools,
            'count': len(tools),
            'recommendation': self._documentation_recommendation(tools)
        }

    def _generate_summary(self) -> Dict:
        """Generate overall summary"""
        all_discoveries = [
            self._discover_linting(),
            self._discover_testing(),
            self._discover_ci_cd(),
            self._discover_git_hooks(),
            self._discover_formatting(),
            self._discover_security(),
            self._discover_documentation(),
        ]

        total_tools = sum(d['count'] for d in all_discoveries)

        maturity_level = "minimal"
        if total_tools >= 10:
            maturity_level = "comprehensive"
        elif total_tools >= 5:
            maturity_level = "moderate"

        return {
            'total_tools_found': total_tools,
            'maturity_level': maturity_level,
            'gaps': self._identify_gaps(all_discoveries)
        }

    def _identify_gaps(self, discoveries: List[Dict]) -> List[str]:
        """Identify missing automation"""
        gaps = []

        # Check for common gaps
        linting = discoveries[0]
        testing = discoveries[1]
        ci_cd = discoveries[2]
        security = discoveries[5]

        if linting['count'] == 0:
            gaps.append('No linting tools configured')

        if testing['count'] == 0:
            gaps.append('No testing framework configured')

        if ci_cd['count'] == 0:
            gaps.append('No CI/CD pipeline configured')

        if security['count'] == 0:
            gaps.append('No security scanning tools')

        return gaps

    # Recommendation methods
    def _linting_recommendation(self, tools: Dict) -> str:
        if not tools:
            return "ADD: Set up linting (ESLint for JS/TS, Pylint for Python)"
        return "ENHANCE: Extend existing linting rules"

    def _testing_recommendation(self, tools: Dict, test_dirs: List) -> str:
        if not tools and not test_dirs:
            return "ADD: Set up testing framework (Jest, Pytest, etc.)"
        if tools and not test_dirs:
            return "ADD: Create test directories and write tests"
        return "ENHANCE: Increase test coverage"

    def _ci_cd_recommendation(self, tools: Dict) -> str:
        if not tools:
            return "ADD: Set up CI/CD (GitHub Actions, GitLab CI, etc.)"
        return "ENHANCE: Add more checks to existing CI/CD"

    def _git_hooks_recommendation(self, tools: Dict) -> str:
        if not tools:
            return "ADD: Set up pre-commit hooks for quality checks"
        return "ENHANCE: Add more hooks (pre-push, commit-msg, etc.)"

    def _formatting_recommendation(self, tools: Dict) -> str:
        if not tools:
            return "ADD: Set up code formatting (Prettier, Black, etc.)"
        return "OK: Formatting tools in place"

    def _security_recommendation(self, tools: Dict) -> str:
        if not tools:
            return "ADD: Set up security scanning (critical gap!)"
        return "ENHANCE: Add more security tools (SAST, dependency scanning)"

    def _documentation_recommendation(self, tools: Dict) -> str:
        if not tools:
            return "ADD: Set up documentation generation"
        return "OK: Documentation tools in place"

    def generate_report(self) -> Dict:
        """Generate complete discovery report"""
        return self.discover_all()

if __name__ == '__main__':
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    discoverer = ExistingToolDiscovery(path)
    report = discoverer.generate_report()
    print(json.dumps(report, indent=2))
