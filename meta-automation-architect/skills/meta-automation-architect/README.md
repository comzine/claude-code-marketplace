# Meta-Automation Architect

A meta-skill that analyzes your project and generates a comprehensive automation system with custom subagents, skills, commands, and hooks.

## What It Creates

The meta-skill generates:

1. **Custom Subagents** - Specialized analysis and implementation agents that run in parallel
2. **Skills** - Auto-invoked capabilities for common patterns in your project
3. **Commands** - Slash commands for frequent workflows
4. **Hooks** - Event-driven automation at lifecycle points
5. **MCP Configurations** - External service integrations
6. **Complete Documentation** - Usage guides and quick references

## How to Use

### Basic Invocation

Simply describe what you want:

```
"Set up automation for my project"
```

Or be more specific:

```
"Create comprehensive automation for my Next.js e-commerce project"
```

```
"Generate a custom automation system for my Python data science workflow"
```

### What Happens

1. **Interactive Discovery** - You'll be asked questions about:
   - Project type (with smart detection and recommendations)
   - Tech stack and frameworks
   - Team size and workflow
   - Pain points and priorities
   - Desired automation scope

2. **Smart Recommendations** - Every question includes:
   - Data-driven analysis of your project
   - Confidence scores and reasoning
   - Recommended options based on evidence
   - Clear trade-offs and explanations

3. **Multi-Agent Generation** - The system creates:
   - A coordinator agent that orchestrates everything
   - Specialized analysis agents (security, performance, quality, etc.)
   - Implementation agents (skill/command/hook generators)
   - Validation agents (testing and documentation)

4. **Parallel Execution** - Agents run concurrently and communicate via the Agent Communication Protocol (ACP)

5. **Complete Delivery** - You receive:
   - All automation artifacts
   - Comprehensive documentation
   - Usage examples
   - Customization guides

## Example Sessions

### Web Application Project

```
User: "Set up automation for my React TypeScript project"

Meta-Skill:
1. Detects: Web application (95% confidence)
   - Found package.json with React dependencies
   - Found src/App.tsx and TypeScript config
   - Detected testing with Jest and React Testing Library

2. Asks: "What are your main pain points?"
   - Recommends: Testing automation (detected low test coverage)
   - Recommends: Code quality checks (found 47 bug-fix commits recently)

3. Recommends: 6 agents for comprehensive coverage
   - Analysis: Security, Performance, Code Quality, Dependencies
   - Implementation: Skill Generator, Command Generator
   - Validation: Integration Tester

4. Generates automation system with:
   - /test-fix command for TDD workflow
   - PostToolUse hook for auto-formatting
   - GitHub MCP integration for PR automation
   - Custom skills for common React patterns
```

### Python Data Science Project

```
User: "Create automation for my machine learning project"

Meta-Skill:
1. Detects: Data Science (88% confidence)
   - Found notebooks/ directory with 15 .ipynb files
   - Found requirements.txt with pandas, scikit-learn, tensorflow
   - Found data/ and models/ directories

2. Asks: "What would you like to automate first?"
   - Recommends: Experiment tracking (detected many model versions)
   - Recommends: Documentation generation (missing architecture docs)
   - Recommends: Data validation (found data pipeline code)

3. Generates automation system with:
   - /run-experiment command for standardized ML runs
   - Custom skill for model comparison and analysis
   - Hooks for auto-documenting experiments
   - MCP integration for MLflow or Weights & Biases
```

## Agent Communication Protocol (ACP)

The generated subagents communicate via a file-based protocol:

### Directory Structure

```
.claude/agents/context/{session-id}/
  ├── coordination.json       # Tracks agent status and dependencies
  ├── messages.jsonl          # Append-only event log
  ├── reports/               # Standardized agent outputs
  │   ├── security-analyzer.json
  │   ├── performance-analyzer.json
  │   └── ...
  └── data/                  # Shared data artifacts
      ├── vulnerabilities.json
      ├── performance-metrics.json
      └── ...
```

### How Agents Communicate

1. **Check Dependencies** - Read `coordination.json` to see which agents have completed
2. **Read Context** - Review reports from other agents
3. **Log Progress** - Write events to `messages.jsonl`
4. **Share Findings** - Create standardized report in `reports/`
5. **Share Data** - Store detailed artifacts in `data/`
6. **Update Status** - Mark completion in `coordination.json`

### Report Format

Every agent writes a standardized JSON report:

```json
{
  "agent_name": "security-analyzer",
  "timestamp": "2025-01-23T10:00:00Z",
  "status": "completed",
  "summary": "Found 5 security vulnerabilities requiring immediate attention",
  "findings": [
    {
      "type": "issue",
      "severity": "high",
      "title": "SQL Injection Risk",
      "description": "User input not sanitized in query builder",
      "location": "src/db/queries.ts:42",
      "recommendation": "Use parameterized queries",
      "example": "db.query('SELECT * FROM users WHERE id = ?', [userId])"
    }
  ],
  "metrics": {
    "items_analyzed": 150,
    "issues_found": 5,
    "time_taken": "2m 34s"
  },
  "recommendations_for_automation": [
    "Skill: SQL injection checker",
    "Hook: Validate queries on PreToolUse",
    "Command: /security-scan for quick checks"
  ]
}
```

## What Gets Generated

### 1. Custom Subagents

Specialized agents tailored to your project:

- **Analysis Agents** - Security, performance, code quality, dependencies, documentation
- **Implementation Agents** - Generate skills, commands, hooks, MCP configs
- **Validation Agents** - Test integration, validate documentation

Each agent:
- Has communication protocol built-in
- Knows how to coordinate with others
- Writes standardized reports
- Suggests automation opportunities

### 2. Skills

Auto-invoked capabilities for your specific patterns:

```
.claude/skills/
  ├── api-doc-generator/        # Generate API docs from code
  ├── tdd-enforcer/             # Test-driven development workflow
  ├── security-checker/         # Quick security validation
  └── ...
```

### 3. Commands

Slash commands for frequent tasks:

```
.claude/commands/
  ├── test-fix.md              # Run tests and fix failures
  ├── deploy-check.md          # Pre-deployment validation
  ├── security-scan.md         # Quick security audit
  └── ...
```

### 4. Hooks

Event-driven automation:

```
.claude/hooks/
  ├── format_on_save.py        # PostToolUse: Auto-format code
  ├── security_check.py        # PreToolUse: Validate operations
  └── run_tests.py             # Stop: Execute test suite
```

### 5. Documentation

Complete usage guides:

- `.claude/AUTOMATION_README.md` - Main system documentation
- `.claude/QUICK_REFERENCE.md` - Cheat sheet for all features
- `.claude/agents/context/{session-id}/` - Generation session details

## Monitoring the Generation Process

While agents work, you can monitor progress:

```bash
# Watch agent status
watch -n 2 'cat .claude/agents/context/*/coordination.json | jq ".agents"'

# Follow live events
tail -f .claude/agents/context/*/messages.jsonl | jq

# Check completion
cat .claude/agents/context/*/coordination.json | \
  jq '.agents | to_entries | map(select(.value.status == "completed")) | map(.key)'
```

## Customizing Generated Automation

All generated artifacts can be customized:

### Modify Agents
```bash
# Edit agent behavior
vim .claude/agents/security-analyzer.md

# Adjust analysis focus, tools, or process
```

### Customize Skills
```bash
# Update skill behavior
vim .claude/skills/api-doc-generator/SKILL.md

# Modify when skill triggers or what it does
```

### Update Commands
```bash
# Change command behavior
vim .claude/commands/test-fix.md

# Adjust workflow or add arguments
```

### Adjust Hooks
```bash
# Modify hook logic
vim .claude/hooks/format_on_save.py

# Change trigger conditions or actions
```

## Troubleshooting

### Agent Failed

```bash
# Check status
jq '.agents | to_entries | map(select(.value.status == "failed"))' \
  .claude/agents/context/{session-id}/coordination.json

# Find error
jq 'select(.from == "failed-agent") | select(.type == "error")' \
  .claude/agents/context/{session-id}/messages.jsonl | tail -1

# Options:
# 1. Retry the agent
# 2. Continue without it
# 3. Manual intervention
```

### Missing Reports

```bash
# List generated reports
ls .claude/agents/context/{session-id}/reports/

# Check if agent completed
jq '.agents["agent-name"]' \
  .claude/agents/context/{session-id}/coordination.json
```

### Review What Happened

```bash
# Full event log
cat .claude/agents/context/{session-id}/messages.jsonl | jq

# Agent-specific events
jq 'select(.from == "agent-name")' \
  .claude/agents/context/{session-id}/messages.jsonl

# Events by type
jq -s 'group_by(.type) | map({type: .[0].type, count: length})' \
  .claude/agents/context/{session-id}/messages.jsonl
```

## Advanced Usage

### Specify Agent Count

```
"Create automation with 8 parallel agents for comprehensive coverage"
```

### Target Specific Areas

```
"Focus automation on security and testing"
```

### Prioritize Implementation

```
"Generate skills and commands first, hooks later"
```

### Re-run Analysis

```bash
# Generate new session with different configuration
# Previous sessions remain in .claude/agents/context/
```

## Architecture

The meta-skill uses a multi-phase architecture:

1. **Discovery Phase** - Interactive questioning with recommendations
2. **Setup Phase** - Initialize communication infrastructure
3. **Analysis Phase** - Parallel agent execution for deep analysis
4. **Synthesis Phase** - Coordinator reads all reports and makes decisions
5. **Implementation Phase** - Parallel generation of automation artifacts
6. **Validation Phase** - Sequential testing and documentation checks
7. **Delivery Phase** - Complete documentation and user report

## Benefits

- **Parallel Execution** - Multiple agents work concurrently
- **Isolated Contexts** - Each agent has focused responsibility
- **Communication Protocol** - Agents share findings reliably
- **Data-Driven** - Recommendations based on actual project analysis
- **Comprehensive** - Covers security, performance, quality, testing, docs
- **Customizable** - All generated artifacts can be modified
- **Transparent** - Full event log shows what happened
- **Reusable** - Generated automation works immediately

## Support

For issues or questions:

1. Review agent reports in `reports/`
2. Check message log in `messages.jsonl`
3. Consult individual documentation
4. Review session details in context directory

---

*Generated automation is project-specific but follows Claude Code best practices for skills, commands, hooks, and MCP integration.*
