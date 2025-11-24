# Example: Python CLI Tool Automation

This example shows what the meta-automation-architect generates for a Python command-line tool project.

## Project Context

- **Type**: CLI Tool
- **Stack**: Python 3.11, Click framework, SQLite
- **Team Size**: Solo developer
- **Pain Points**: Documentation, testing, dependency management
- **Priority**: User documentation and testing

## User Conversation

```
User: "Create automation for my Python CLI project"

Meta-Skill: Analyzing project...
- Detected: CLI Tool (87% confidence)
  - Found cli.py with Click decorators
  - Found setup.py with console_scripts entry point
  - Found requirements.txt with CLI dependencies
  - Found README.md but missing detailed docs

Meta-Skill: What are your main pain points?
Options:
- Low test coverage (RECOMMENDED: 8 test files for 42 modules)
- Missing documentation (RECOMMENDED: No docs/ directory)
- Dependency issues
- Release process

User: [Selects: Low test coverage, Missing documentation]

Meta-Skill: How many agents should we create?
- Few (2-3): Basic analysis (RECOMMENDED for solo projects)
- Moderate (4-6): Multi-domain coverage
- Many (7+): Comprehensive automation

User: [Selects: Few]

Meta-Skill: Generating automation system...
Session ID: b2c3d4e5-f6a7-8901-bcde-f23456789012
```

## Generated Automation System

### 1. Custom Subagents (4)

All agents created in `.claude/agents/`:

#### Analysis Agents (Run in Parallel)

**code-quality-analyzer.md**
- Checks PEP 8 compliance
- Analyzes function complexity
- Identifies code duplication
- Reviews error handling

**testing-analyzer.md**
- Measures test coverage
- Identifies untested CLI commands
- Reviews test patterns
- Checks for integration tests

#### Implementation Agents

**skill-generator.md**
- Creates custom skills for Python patterns
- Generated: `docstring-generator`, `cli-test-helper`

**command-generator.md**
- Creates commands for Python workflows
- Generated: `/test-cov`, `/release-prep`

### 2. Custom Skills (2)

**`.claude/skills/docstring-generator/SKILL.md`**
```markdown
---
name: docstring-generator
description: Generates comprehensive docstrings for Python functions and modules
allowed-tools: ["Read", "Write", "Grep", "Glob"]
---

# Docstring Generator

Automatically generates NumPy-style docstrings for Python code.

## When This Activates

- User asks to "add documentation" to Python files
- User requests "docstrings" for functions
- User says "document this module"

## Process

1. Scan Python files for functions/classes without docstrings
2. Analyze function signatures, type hints, and logic
3. Generate NumPy-style docstrings with:
   - Brief description
   - Parameters with types
   - Returns with type
   - Raises (exceptions)
   - Examples
4. Insert docstrings into code
5. Validate with pydocstyle

## Example

**Input:**
```python
def parse_config(path, validate=True):
    with open(path) as f:
        config = json.load(f)
    if validate:
        validate_config(config)
    return config
```

**Output:**
```python
def parse_config(path: str, validate: bool = True) -> dict:
    """
    Parse configuration from JSON file.

    Parameters
    ----------
    path : str
        Path to configuration file
    validate : bool, optional
        Whether to validate configuration (default: True)

    Returns
    -------
    dict
        Parsed configuration dictionary

    Raises
    ------
    FileNotFoundError
        If configuration file doesn't exist
    ValidationError
        If configuration is invalid and validate=True

    Examples
    --------
    >>> config = parse_config('config.json')
    >>> config['database']['host']
    'localhost'
    """
    with open(path) as f:
        config = json.load(f)
    if validate:
        validate_config(config)
    return config
```

[... detailed implementation ...]
```

**`.claude/skills/cli-test-helper/SKILL.md`**
```markdown
---
name: cli-test-helper
description: Generates tests for Click CLI commands with fixtures
allowed-tools: ["Read", "Write", "Bash", "Grep"]
---

# CLI Test Helper

Automatically generates pytest tests for Click commands.

## When This Activates

- User implements new CLI command
- User requests "test this command"
- User says "add CLI tests"

## Process

1. Identify Click commands in code
2. Extract command parameters, options, flags
3. Generate pytest tests with:
   - CliRunner fixtures
   - Success case tests
   - Error case tests
   - Edge case tests
   - Output validation
4. Create test fixtures for complex inputs
5. Run tests to verify

## Example

**CLI Command:**
```python
@click.command()
@click.option('--name', required=True, help='User name')
@click.option('--email', help='User email')
@click.option('--verbose', is_flag=True)
def create_user(name, email, verbose):
    """Create a new user."""
    user = User(name=name, email=email)
    db.save(user)
    if verbose:
        click.echo(f"Created user: {user}")
    else:
        click.echo(user.id)
```

**Generated Test:**
```python
import pytest
from click.testing import CliRunner
from myapp.cli import create_user

@pytest.fixture
def runner():
    return CliRunner()

def test_create_user_success(runner):
    """Test successful user creation."""
    result = runner.invoke(create_user, ['--name', 'Alice'])
    assert result.exit_code == 0
    assert 'user-' in result.output

def test_create_user_with_email(runner):
    """Test user creation with email."""
    result = runner.invoke(create_user, [
        '--name', 'Alice',
        '--email', 'alice@example.com'
    ])
    assert result.exit_code == 0

def test_create_user_verbose(runner):
    """Test verbose output."""
    result = runner.invoke(create_user, [
        '--name', 'Alice',
        '--verbose'
    ])
    assert result.exit_code == 0
    assert 'Created user:' in result.output

def test_create_user_missing_name(runner):
    """Test error when name is missing."""
    result = runner.invoke(create_user, [])
    assert result.exit_code != 0
    assert 'Missing option' in result.output
```

[... detailed implementation ...]
```

### 3. Custom Commands (2)

**`.claude/commands/test-cov.md`**
```markdown
---
description: Run tests with coverage report
allowed-tools: ["Bash", "Read"]
---

# Test Coverage Command

Runs pytest with coverage and generates detailed report.

## Usage

```bash
/test-cov                    # Full coverage
/test-cov tests/unit         # Specific directory
/test-cov --html             # Generate HTML report
```

## What This Does

1. **Run Tests with Coverage**
   ```bash
   pytest --cov=src --cov-report=term-missing $ARGUMENTS
   ```

2. **Generate Report**
   - Terminal: Coverage percentage by module
   - Missing lines highlighted
   - HTML report (if --html flag)

3. **Check Thresholds**
   - Warn if coverage < 80%
   - Error if coverage < 60%

4. **Identify Gaps**
   - List untested files
   - Highlight critical paths without tests

## Example Output

```
---------- coverage: platform darwin, python 3.11.5 -----------
Name                      Stmts   Miss  Cover   Missing
-------------------------------------------------------
src/__init__.py               2      0   100%
src/cli.py                  145     23    84%   67-73, 89-92
src/config.py                34      0   100%
src/database.py              89     45    49%   23-67, 78-89
src/utils.py                 23      2    91%   45-46
-------------------------------------------------------
TOTAL                       293     70    76%

⚠️  Coverage below 80% target
❌ database.py has only 49% coverage (critical module!)

Suggestions:
- Add integration tests for database.py
- Test error paths in cli.py lines 67-73
```

[... detailed implementation ...]
```

**`.claude/commands/release-prep.md`**
```markdown
---
description: Prepare project for release (version bump, tests, build)
allowed-tools: ["Bash", "Read", "Write"]
---

# Release Preparation

Automates release preparation checklist.

## Usage

```bash
/release-prep               # Interactive mode
/release-prep patch         # Auto-bump patch version
/release-prep minor         # Auto-bump minor version
/release-prep major         # Auto-bump major version
```

## Process

1. **Run Full Test Suite**
   ```bash
   pytest -v
   ```

2. **Check Coverage**
   ```bash
   pytest --cov=src --cov-report=term
   ```

3. **Lint Code**
   ```bash
   ruff check src/
   mypy src/
   ```

4. **Bump Version**
   - Update version in setup.py, __version__.py
   - Update CHANGELOG.md
   - Create git tag

5. **Build Distributions**
   ```bash
   python -m build
   ```

6. **Test Installation**
   ```bash
   pip install dist/*.whl
   ```

7. **Generate Release Notes**
   - Extract commits since last tag
   - Categorize changes (features, fixes, breaking)
   - Write to RELEASE_NOTES.md

8. **Checklist Output**
   ```
   ✅ All tests pass (147 passed)
   ✅ Coverage: 87%
   ✅ Linting: No issues
   ✅ Version bumped: 1.2.3 → 1.2.4
   ✅ CHANGELOG.md updated
   ✅ Distribution built
   ✅ Installation tested
   ✅ Release notes generated

   Ready to release! Next steps:
   1. Review RELEASE_NOTES.md
   2. git push --tags
   3. twine upload dist/*
   ```

[... detailed implementation ...]
```

### 4. Hooks (1)

**`.claude/hooks/lint_python.py`**
```python
#!/usr/bin/env python3
"""
Python Linting Hook
Type: PostToolUse
Automatically lints Python files after edits
"""

import sys
import json
import subprocess
from pathlib import Path

def main():
    context = json.load(sys.stdin)
    tool = context.get('tool')
    params = context.get('parameters', {})

    # Only trigger on Write/Edit to Python files
    if tool not in ['Write', 'Edit']:
        sys.exit(0)

    file_path = params.get('file_path', '')
    if not file_path.endswith('.py'):
        sys.exit(0)

    # Run ruff
    print(f"🔍 Linting {file_path}...", file=sys.stderr)
    ruff_result = subprocess.run(
        ['ruff', 'check', '--fix', file_path],
        capture_output=True,
        text=True
    )

    if ruff_result.returncode != 0:
        print(f"⚠️  Ruff found issues:", file=sys.stderr)
        print(ruff_result.stdout, file=sys.stderr)

    # Run black
    print(f"🎨 Formatting {file_path}...", file=sys.stderr)
    black_result = subprocess.run(
        ['black', '--quiet', file_path],
        capture_output=True
    )

    if black_result.returncode == 0:
        print(f"✅ Formatted successfully", file=sys.stderr)
    else:
        print(f"❌ Formatting failed", file=sys.stderr)

    sys.exit(0)

if __name__ == '__main__':
    main()
```

### 5. Settings Configuration

**`.claude/settings.json`** (updated)
```json
{
  "hooks": {
    "PostToolUse": {
      "commands": [".claude/hooks/lint_python.py"]
    }
  }
}
```

### 6. Documentation

**`.claude/AUTOMATION_README.md`**
```markdown
# Automation System for Python CLI Tool

## Generated On
2025-01-23

## Session ID
b2c3d4e5-f6a7-8901-bcde-f23456789012

## What Was Created

### Analysis Phase

- **code-quality-analyzer**: Identified 8 PEP 8 violations and 3 complex functions
- **testing-analyzer**: Test coverage at 58%, many CLI commands untested

### Generated Artifacts

#### Custom Agents (4)
- **code-quality-analyzer**: Evaluates code quality and PEP 8 compliance
- **testing-analyzer**: Measures test coverage for CLI commands
- **skill-generator**: Created 2 custom skills
- **command-generator**: Created 2 slash commands

#### Skills (2)
- **docstring-generator**: Auto-generates NumPy-style docstrings
- **cli-test-helper**: Generates pytest tests for Click commands

#### Commands (2)
- **/test-cov**: Run tests with coverage report
- **/release-prep**: Prepare project for release

#### Hooks (1)
- **PostToolUse**: Auto-lint and format Python files

## Quick Start

1. Generate docstrings:
   ```bash
   "Add documentation to all functions in src/cli.py"
   # docstring-generator skill auto-invokes
   ```

2. Generate tests:
   ```bash
   "Create tests for the create_user command"
   # cli-test-helper skill auto-invokes
   ```

3. Check coverage:
   ```bash
   /test-cov
   ```

4. Prepare release:
   ```bash
   /release-prep patch
   ```

5. Auto-formatting:
   - Every time you write/edit a .py file, it's automatically linted and formatted

## Customization

- Edit skills in `.claude/skills/`
- Modify commands in `.claude/commands/`
- Adjust hook in `.claude/hooks/lint_python.py`
- Configure linters (ruff.toml, pyproject.toml)

[... more documentation ...]
```

## Agent Communication

**`coordination.json`**
```json
{
  "session_id": "b2c3d4e5-f6a7-8901-bcde-f23456789012",
  "started_at": "2025-01-23T14:00:00Z",
  "project_type": "cli",
  "agents": {
    "code-quality-analyzer": {
      "status": "completed",
      "started_at": "2025-01-23T14:00:00Z",
      "completed_at": "2025-01-23T14:03:00Z",
      "report_path": "reports/code-quality-analyzer.json"
    },
    "testing-analyzer": {
      "status": "completed",
      "started_at": "2025-01-23T14:00:01Z",
      "completed_at": "2025-01-23T14:04:00Z",
      "report_path": "reports/testing-analyzer.json"
    },
    "skill-generator": {
      "status": "completed",
      "started_at": "2025-01-23T14:05:00Z",
      "completed_at": "2025-01-23T14:08:00Z",
      "report_path": "reports/skill-generator.json"
    },
    "command-generator": {
      "status": "completed",
      "started_at": "2025-01-23T14:08:30Z",
      "completed_at": "2025-01-23T14:10:00Z",
      "report_path": "reports/command-generator.json"
    }
  }
}
```

**Key Report Excerpts:**

**`reports/testing-analyzer.json`**
```json
{
  "agent_name": "testing-analyzer",
  "summary": "Test coverage at 58%. Many CLI commands lack tests.",
  "findings": [
    {
      "type": "issue",
      "severity": "high",
      "title": "Untested CLI Commands",
      "description": "5 Click commands have no tests",
      "location": "src/cli.py",
      "recommendation": "Generate tests for each command"
    }
  ],
  "recommendations_for_automation": [
    "Skill: Auto-generate CLI tests using CliRunner",
    "Command: /test-cov for quick coverage checks"
  ]
}
```

**`reports/skill-generator.json`**
```json
{
  "agent_name": "skill-generator",
  "summary": "Generated 2 skills: docstring-generator and cli-test-helper",
  "findings": [
    {
      "type": "info",
      "title": "Created docstring-generator skill",
      "description": "Automates NumPy-style docstring generation",
      "location": ".claude/skills/docstring-generator/"
    },
    {
      "type": "info",
      "title": "Created cli-test-helper skill",
      "description": "Automates pytest test generation for Click commands",
      "location": ".claude/skills/cli-test-helper/"
    }
  ]
}
```

## Result

Solo developer now has efficient automation:
- ✅ 2 skills that handle tedious documentation and testing tasks
- ✅ 2 commands for common workflows (coverage, releases)
- ✅ 1 hook that auto-formats on every save
- ✅ Focuses on writing code, not boilerplate
- ✅ Complete documentation
- ✅ Ready to use immediately

Total generation time: ~10 minutes

## Before vs After

**Before:**
```bash
# Manual workflow
$ vim src/cli.py               # Add new command
$ vim tests/test_cli.py        # Manually write tests
$ pytest                       # Run tests
$ ruff check src/              # Manual linting
$ black src/                   # Manual formatting
$ pytest --cov                 # Check coverage
$ vim docs/                    # Update docs manually
# ~30-45 minutes per feature
```

**After:**
```bash
# Automated workflow
$ vim src/cli.py               # Add new command
# Hook auto-formats and lints immediately ✅

"Create tests for the new command"
# cli-test-helper generates comprehensive tests ✅

/test-cov
# Instant coverage report ✅

"Add docstrings to src/cli.py"
# docstring-generator adds complete documentation ✅

# ~10 minutes per feature (3-4x faster!)
```
