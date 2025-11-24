# Example: Web Application Automation

This example shows what the meta-automation-architect generates for a typical Next.js web application project.

## Project Context

- **Type**: Web Application
- **Stack**: Next.js, TypeScript, React, TailwindCSS
- **Team Size**: Small (3-5 developers)
- **Pain Points**: Testing coverage, security checks, performance optimization
- **Priority**: Testing automation and code quality

## User Conversation

```
User: "Set up automation for my Next.js project"

Meta-Skill: Analyzing project...
- Detected: Web Application (92% confidence)
  - Found package.json with Next.js and React
  - Found TypeScript configuration
  - Found src/app/ directory (App Router)
  - Found TailwindCSS configuration

Meta-Skill: What are your main pain points?
Options:
- Low test coverage (RECOMMENDED: 15 test files for 87 components)
- Frequent bug fixes (RECOMMENDED: 23 bug-fix commits last month)
- Performance issues
- Security concerns
- Documentation gaps (RECOMMENDED: Missing API docs)

User: [Selects: Low test coverage, Security concerns]

Meta-Skill: How many agents should we create?
- Few (2-3): Basic analysis
- Moderate (4-6): Multi-domain coverage (RECOMMENDED)
- Many (7+): Comprehensive automation

User: [Selects: Moderate]

Meta-Skill: Generating automation system...
Session ID: a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

## Generated Automation System

### 1. Custom Subagents (6)

All agents created in `.claude/agents/`:

#### Analysis Agents (Run in Parallel)

**security-analyzer.md**
- Scans for XSS, CSRF, SQL injection vulnerabilities
- Checks authentication/authorization patterns
- Identifies exposed secrets or API keys
- Reviews dependency vulnerabilities

**performance-analyzer.md**
- Analyzes bundle sizes and code splitting
- Identifies slow rendering components
- Checks for N+1 query patterns
- Reviews asset optimization

**code-quality-analyzer.md**
- Measures code complexity
- Detects duplication
- Checks naming conventions
- Reviews error handling patterns

**testing-analyzer.md**
- Measures test coverage
- Identifies untested critical paths
- Reviews test quality and patterns
- Suggests testing strategies

#### Implementation Agents (Run After Analysis)

**skill-generator.md**
- Creates custom skills based on findings
- Generated: `tdd-workflow`, `api-doc-generator`, `security-checker`

**command-generator.md**
- Creates slash commands for common tasks
- Generated: `/test-fix`, `/security-scan`, `/perf-check`

### 2. Custom Skills (3)

**`.claude/skills/tdd-workflow/SKILL.md`**
```markdown
---
name: tdd-workflow
description: Enforces test-driven development by requiring tests before implementation
allowed-tools: ["Read", "Write", "Bash", "Grep"]
---

# TDD Workflow

Automatically invoked when user requests new features or modifications.

## Process

1. Check if tests exist for the target code
2. If no tests, create test file first
3. Write failing test
4. Implement minimal code to pass
5. Refactor while keeping tests green
6. Run full test suite

[... detailed implementation ...]
```

**`.claude/skills/api-doc-generator/SKILL.md`**
```markdown
---
name: api-doc-generator
description: Generates OpenAPI documentation from Next.js API routes
allowed-tools: ["Read", "Write", "Grep", "Glob", "Bash"]
---

# API Documentation Generator

Automatically generates OpenAPI 3.0 documentation from your API routes.

## Process

1. Scan src/app/api/ for route handlers
2. Extract types from TypeScript
3. Generate OpenAPI schemas
4. Create interactive documentation
5. Validate against actual implementation

[... detailed implementation ...]
```

**`.claude/skills/security-checker/SKILL.md`**
```markdown
---
name: security-checker
description: Quick security validation for code changes
allowed-tools: ["Read", "Grep", "Bash"]
---

# Security Checker

Runs security checks on code before commits.

## Checks

- XSS vulnerabilities in JSX
- CSRF protection on mutations
- Exposed secrets or API keys
- Insecure dependencies
- Missing input validation

[... detailed implementation ...]
```

### 3. Custom Commands (3)

**`.claude/commands/test-fix.md`**
```markdown
---
description: Run tests and iteratively fix failures
allowed-tools: ["Bash", "Read", "Write", "Grep"]
---

# Test Fix Command

Runs your test suite and automatically fixes failures.

## Usage

```bash
/test-fix
/test-fix src/components
/test-fix --watch
```

## Process

1. Run test suite
2. Identify failures
3. Analyze failure causes
4. Propose fixes
5. Apply fixes with user approval
6. Re-run tests
7. Repeat until green

[... detailed implementation ...]
```

**`.claude/commands/security-scan.md`**
```markdown
---
description: Quick security audit of project
allowed-tools: ["Bash", "Read", "Grep"]
---

# Security Scan

Fast security check for common vulnerabilities.

## Usage

```bash
/security-scan
/security-scan src/
/security-scan --full
```

[... detailed implementation ...]
```

**`.claude/commands/perf-check.md`**
```markdown
---
description: Analyze performance and bundle size
allowed-tools: ["Bash", "Read", "Glob"]
---

# Performance Check

Analyzes bundle size, rendering performance, and optimization opportunities.

[... detailed implementation ...]
```

### 4. Hooks (2)

**`.claude/hooks/security_validation.py`**
```python
#!/usr/bin/env python3
"""
Security Validation Hook
Type: PreToolUse
Blocks writes to sensitive files and validates security patterns
"""

import sys
import json

def main():
    context = json.load(sys.stdin)
    tool = context.get('tool')
    params = context.get('parameters', {})

    # Block writes to sensitive files
    if tool in ['Write', 'Edit']:
        file_path = params.get('file_path', '')

        if file_path.endswith('.env') or 'secrets' in file_path.lower():
            print("❌ Blocked: Writing to sensitive file", file=sys.stderr)
            sys.exit(2)  # Block operation

    # Validate API route security
    if tool == 'Write' and '/api/' in params.get('file_path', ''):
        content = params.get('content', '')

        if 'export async function POST' in content:
            if 'csrf' not in content.lower():
                print("⚠️  Warning: API route missing CSRF protection", file=sys.stderr)

    sys.exit(0)

if __name__ == '__main__':
    main()
```

**`.claude/hooks/run_tests.py`**
```python
#!/usr/bin/env python3
"""
Run Tests Hook
Type: Stop
Runs test suite when session ends
"""

import sys
import json
import subprocess

def main():
    context = json.load(sys.stdin)

    # Run tests
    print("🧪 Running test suite...", file=sys.stderr)
    result = subprocess.run(['npm', 'test', '--', '--run'],
                          capture_output=True, text=True)

    if result.returncode != 0:
        print("❌ Tests failed:", file=sys.stderr)
        print(result.stdout, file=sys.stderr)
    else:
        print("✅ All tests passed", file=sys.stderr)

    sys.exit(0)

if __name__ == '__main__':
    main()
```

### 5. Settings Configuration

**`.claude/settings.json`** (updated)
```json
{
  "hooks": {
    "PreToolUse": {
      "commands": [".claude/hooks/security_validation.py"]
    },
    "Stop": {
      "commands": [".claude/hooks/run_tests.py"]
    }
  },
  "mcpServers": {
    "github": {
      "command": "mcp-github",
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

### 6. Documentation

**`.claude/AUTOMATION_README.md`**
```markdown
# Automation System for Next.js Project

## Generated On
2025-01-23

## Session ID
a1b2c3d4-e5f6-7890-abcd-ef1234567890

## What Was Created

### Analysis Phase

- **security-analyzer**: Found 3 high-severity issues requiring attention
- **performance-analyzer**: Identified 5 optimization opportunities
- **code-quality-analyzer**: Detected 12 code smells and complexity issues
- **testing-analyzer**: Test coverage at 45%, recommended 80%+ for critical paths

### Generated Artifacts

#### Custom Agents (6)
- **security-analyzer**: Scans for vulnerabilities and security issues
- **performance-analyzer**: Identifies performance bottlenecks
- **code-quality-analyzer**: Evaluates code maintainability
- **testing-analyzer**: Measures and improves test coverage
- **skill-generator**: Created 3 custom skills
- **command-generator**: Created 3 slash commands

#### Skills (3)
- **tdd-workflow**: Enforces test-driven development workflow
- **api-doc-generator**: Auto-generates API documentation from routes
- **security-checker**: Quick security validation for code changes

#### Commands (3)
- **/test-fix**: Run tests and fix failures iteratively
- **/security-scan**: Quick security audit
- **/perf-check**: Analyze performance and bundle size

#### Hooks (2)
- **PreToolUse**: Security validation (blocks sensitive file writes)
- **Stop**: Run test suite on session end

#### MCP Servers (1)
- **github**: PR automation and issue tracking

## Quick Start

1. Test an agent:
   ```bash
   "Use the security-analyzer agent on src/app"
   ```

2. Try a skill:
   ```bash
   "Implement user authentication feature"
   # tdd-workflow skill auto-invokes
   ```

3. Execute a command:
   ```bash
   /test-fix src/components
   ```

4. Hooks automatically run:
   - Security validation on file writes
   - Tests run when you end the session

## Customization

All generated automation can be customized:
- Edit agents in `.claude/agents/`
- Modify skills in `.claude/skills/`
- Update commands in `.claude/commands/`
- Adjust hooks in `.claude/hooks/`

[... more documentation ...]
```

**`.claude/QUICK_REFERENCE.md`**
```markdown
# Quick Reference

## Available Agents
- security-analyzer
- performance-analyzer
- code-quality-analyzer
- testing-analyzer
- skill-generator
- command-generator

## Available Commands
- /test-fix
- /security-scan
- /perf-check

## Available Skills
- tdd-workflow
- api-doc-generator
- security-checker

## Hooks Configured
- PreToolUse: security_validation.py
- Stop: run_tests.py

## MCP Servers
- github

## Usage Examples

### Use an agent:
"Use the security-analyzer agent to check src/app/api"

### Invoke a skill:
"Implement new feature X" (tdd-workflow auto-invokes)
"Generate API docs" (api-doc-generator auto-invokes)

### Execute command:
/test-fix src/
/security-scan
/perf-check

### Check hooks:
cat .claude/settings.json | jq '.hooks'

## Session Data

All agent communication is logged in:
`.claude/agents/context/a1b2c3d4-e5f6-7890-abcd-ef1234567890/`

Review this directory to understand what happened during generation.
```

## Agent Communication Example

During generation, agents communicated via ACP:

**`coordination.json`**
```json
{
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "started_at": "2025-01-23T10:00:00Z",
  "project_type": "web_app",
  "agents": {
    "security-analyzer": {
      "status": "completed",
      "started_at": "2025-01-23T10:00:00Z",
      "completed_at": "2025-01-23T10:05:00Z",
      "report_path": "reports/security-analyzer.json"
    },
    "performance-analyzer": {
      "status": "completed",
      "started_at": "2025-01-23T10:00:01Z",
      "completed_at": "2025-01-23T10:06:00Z",
      "report_path": "reports/performance-analyzer.json"
    },
    "testing-analyzer": {
      "status": "completed",
      "started_at": "2025-01-23T10:00:02Z",
      "completed_at": "2025-01-23T10:07:00Z",
      "report_path": "reports/testing-analyzer.json"
    },
    "skill-generator": {
      "status": "completed",
      "started_at": "2025-01-23T10:08:00Z",
      "completed_at": "2025-01-23T10:12:00Z",
      "report_path": "reports/skill-generator.json"
    }
  }
}
```

**`messages.jsonl`** (excerpt)
```json
{"timestamp":"2025-01-23T10:00:00Z","from":"security-analyzer","type":"status","message":"Starting security analysis"}
{"timestamp":"2025-01-23T10:02:15Z","from":"security-analyzer","type":"finding","severity":"high","data":{"title":"Missing CSRF protection","location":"src/app/api/users/route.ts"}}
{"timestamp":"2025-01-23T10:05:00Z","from":"security-analyzer","type":"completed","message":"Found 3 high-severity issues"}
{"timestamp":"2025-01-23T10:08:00Z","from":"skill-generator","type":"status","message":"Reading analysis reports"}
{"timestamp":"2025-01-23T10:09:30Z","from":"skill-generator","type":"status","message":"Generating TDD workflow skill"}
```

**`reports/security-analyzer.json`** (excerpt)
```json
{
  "agent_name": "security-analyzer",
  "timestamp": "2025-01-23T10:05:00Z",
  "status": "completed",
  "summary": "Found 3 high-severity security issues requiring immediate attention",
  "findings": [
    {
      "type": "issue",
      "severity": "high",
      "title": "Missing CSRF Protection",
      "description": "API routes lack CSRF token validation",
      "location": "src/app/api/users/route.ts:12",
      "recommendation": "Add CSRF token validation middleware",
      "example": "import { validateCsrf } from '@/lib/csrf';"
    }
  ],
  "recommendations_for_automation": [
    "Skill: CSRF validator that checks all API routes",
    "Hook: PreToolUse hook to validate new API routes",
    "Command: /security-scan for quick checks"
  ]
}
```

## Result

User now has a complete automation system:
- ✅ 6 specialized agents that can be run on-demand
- ✅ 3 skills that auto-invoke for common patterns
- ✅ 3 commands for quick workflows
- ✅ 2 hooks for automatic validation
- ✅ Complete documentation
- ✅ All agents communicated via ACP protocol
- ✅ Ready to use immediately

Total generation time: ~15 minutes (mostly analysis phase)
