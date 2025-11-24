# Meta-Automation Architect - System Overview

A comprehensive skill that analyzes projects and generates tailored automation systems with parallel subagents, custom skills, commands, and hooks.

## Quick Links

- **[README.md](README.md)** - Main usage guide
- **[SKILL.md](SKILL.md)** - Full skill definition
- **[Communication Protocol](references/COMMUNICATION_PROTOCOL.md)** - Agent Communication Protocol (ACP) specification
- **[Examples](examples/)** - Complete examples for different project types
- **[Templates](templates/)** - Templates for generated artifacts

## Directory Structure

```
.claude/skills/meta-automation-architect/
├── SKILL.md                           # Main skill definition
├── README.md                          # Usage guide
├── OVERVIEW.md                        # This file
│
├── scripts/                           # Generation scripts
│   ├── detect_project.py              # Project analysis
│   ├── generate_agents.py             # Agent generation (11 templates)
│   └── generate_coordinator.py        # Coordinator generation
│
├── templates/                         # Output templates
│   ├── example-skill-template.md      # Skill template structure
│   ├── example-command-template.md    # Command template structure
│   └── example-hook-template.py       # Hook template structure
│
├── examples/                          # Complete examples
│   ├── EXAMPLE_WEB_APP.md            # Next.js web app automation
│   └── EXAMPLE_PYTHON_CLI.md         # Python CLI tool automation
│
└── references/                        # Technical docs
    └── COMMUNICATION_PROTOCOL.md      # ACP specification
```

## What This Meta-Skill Does

### 1. Interactive Discovery
- Analyzes project structure and tech stack
- Provides data-driven recommendations
- Asks targeted questions with smart defaults
- Never guesses - always validates with user

### 2. Generates Parallel Subagent System
- **Analysis Agents** - Run in parallel to analyze different domains
- **Implementation Agents** - Generate automation artifacts
- **Validation Agents** - Test and validate the system
- **Coordinator Agent** - Orchestrates the entire workflow

### 3. Creates Complete Automation
- **Custom Agents** - Specialized for project patterns
- **Skills** - Auto-invoked capabilities
- **Commands** - Slash commands for workflows
- **Hooks** - Event-driven automation
- **MCP Integrations** - External service connections

### 4. Enables Agent Communication
Uses **Agent Communication Protocol (ACP)** for coordination:
- File-based communication at `.claude/agents/context/{session-id}/`
- Coordination file for status tracking
- Message bus for event transparency
- Standardized reports for findings
- Data artifacts for detailed exchange

## Available Agent Templates

### Analysis Agents (Run in Parallel)
1. **security-analyzer** - Security vulnerabilities, auth flaws, secret exposure
2. **performance-analyzer** - Bottlenecks, inefficient algorithms, optimization opportunities
3. **code-quality-analyzer** - Code complexity, duplication, maintainability
4. **dependency-analyzer** - Outdated packages, vulnerabilities, conflicts
5. **documentation-analyzer** - Documentation completeness and quality

### Implementation Agents
6. **skill-generator** - Creates custom skills from findings
7. **command-generator** - Creates slash commands for workflows
8. **hook-generator** - Creates automation hooks
9. **mcp-configurator** - Configures external integrations

### Validation Agents
10. **integration-tester** - Validates all components work together
11. **documentation-validator** - Ensures comprehensive documentation

## Agent Communication Protocol (ACP)

### Core Concept
Parallel agents with isolated contexts communicate via structured files:

```
.claude/agents/context/{session-id}/
  ├── coordination.json       # Status tracking
  ├── messages.jsonl          # Event log (append-only)
  ├── reports/               # Agent outputs
  │   └── {agent-name}.json
  └── data/                  # Shared artifacts
```

### Key Features
- ✅ **Asynchronous** - Agents don't block each other
- ✅ **Discoverable** - Any agent can read any report
- ✅ **Persistent** - Survives crashes
- ✅ **Transparent** - Complete audit trail
- ✅ **Orchestratable** - Coordinator manages dependencies

See [COMMUNICATION_PROTOCOL.md](references/COMMUNICATION_PROTOCOL.md) for full specification.

## Usage Patterns

### Basic Invocation
```
"Set up automation for my project"
```

### Specific Project Type
```
"Create automation for my Next.js web app"
"Generate automation for my Python CLI tool"
"Set up automation for my data science workflow"
```

### With Priorities
```
"Focus automation on testing and security"
"Prioritize documentation and code quality"
```

### With Scope
```
"Create comprehensive automation with 8 agents"
"Generate basic automation (3-4 agents)"
```

## Example Output

For a typical web application, generates:

```
.claude/
├── agents/
│   ├── security-analyzer.md
│   ├── performance-analyzer.md
│   ├── code-quality-analyzer.md
│   ├── skill-generator.md
│   ├── command-generator.md
│   └── automation-coordinator.md
│
├── skills/
│   ├── tdd-workflow/
│   ├── api-doc-generator/
│   └── security-checker/
│
├── commands/
│   ├── test-fix.md
│   ├── security-scan.md
│   └── perf-check.md
│
├── hooks/
│   ├── security_validation.py
│   └── run_tests.py
│
├── settings.json (updated)
├── AUTOMATION_README.md
└── QUICK_REFERENCE.md
```

Plus complete session data:
```
.claude/agents/context/{session-id}/
├── coordination.json
├── messages.jsonl
├── reports/
│   ├── security-analyzer.json
│   ├── performance-analyzer.json
│   └── ...
└── data/
    └── ...
```

## Workflow Phases

### Phase 1: Discovery (Interactive)
- Project type detection with confidence scores
- Tech stack analysis
- Team size and workflow questions
- Pain point identification
- Priority setting
- Agent count recommendation

### Phase 2: Setup
- Generate unique session ID
- Create communication directory structure
- Initialize coordination file
- Export environment variables

### Phase 3: Analysis (Parallel)
- Launch analysis agents concurrently
- Each agent analyzes specific domain
- Agents log progress to message bus
- Generate standardized reports
- Update coordination status

### Phase 4: Synthesis
- Coordinator reads all reports
- Aggregates findings
- Identifies patterns
- Makes decisions on what to generate

### Phase 5: Implementation (Parallel)
- Launch implementation agents
- Generate skills, commands, hooks
- Configure MCP servers
- Create artifacts

### Phase 6: Validation (Sequential)
- Test all components
- Validate documentation
- Ensure everything works

### Phase 7: Delivery
- Generate documentation
- Create usage guides
- Report to user

## Key Scripts

### `detect_project.py`
```python
# Analyzes project to determine:
# - Project type (web app, CLI, data science, etc.)
# - Tech stack (frameworks, languages)
# - Pain points (testing, docs, dependencies)
# - Statistics (file counts, test coverage)

python scripts/detect_project.py
```

### `generate_agents.py`
```python
# Generates specialized agents with communication protocol
# Available types: security-analyzer, performance-analyzer, etc.

python scripts/generate_agents.py \
  --session-id "abc-123" \
  --agent-type "security-analyzer" \
  --output ".claude/agents/security-analyzer.md"
```

### `generate_coordinator.py`
```python
# Creates coordinator agent that orchestrates workflow

python scripts/generate_coordinator.py \
  --session-id "abc-123" \
  --agents "security,performance,quality" \
  --output ".claude/agents/coordinator.md"
```

## Benefits

### For Solo Developers
- Automates tedious documentation and testing
- Provides instant code quality feedback
- Reduces context switching
- Focuses on writing code, not boilerplate

### For Small Teams
- Standardizes workflows across team
- Ensures consistent code quality
- Automates code reviews
- Improves onboarding with documentation

### For Large Projects
- Comprehensive analysis across domains
- Identifies technical debt systematically
- Provides actionable recommendations
- Scales with multiple parallel agents

## Customization

All generated artifacts can be customized:

- **Agents** - Edit `.claude/agents/{agent-name}.md`
- **Skills** - Modify `.claude/skills/{skill-name}/SKILL.md`
- **Commands** - Update `.claude/commands/{command-name}.md`
- **Hooks** - Change `.claude/hooks/{hook-name}.py`
- **Settings** - Adjust `.claude/settings.json`

## Monitoring & Debugging

### Watch Agent Progress
```bash
watch -n 2 'cat .claude/agents/context/*/coordination.json | jq ".agents"'
```

### Follow Live Events
```bash
tail -f .claude/agents/context/*/messages.jsonl | jq
```

### Check Reports
```bash
ls .claude/agents/context/*/reports/
cat .claude/agents/context/*/reports/security-analyzer.json | jq
```

### Aggregate Findings
```bash
jq -s 'map(.findings[]) | map(select(.severity == "high"))' \
  .claude/agents/context/*/reports/*.json
```

## Best Practices

### When Invoking
1. Let the skill analyze your project first
2. Answer questions honestly
3. Use recommendations when unsure
4. Start with moderate agent count
5. Review generated automation

### After Generation
1. Read AUTOMATION_README.md
2. Try example invocations
3. Customize for your needs
4. Review session logs to understand decisions
5. Iterate based on usage

### For Maintenance
1. Review agent reports periodically
2. Update skills as patterns evolve
3. Add new commands for new workflows
4. Adjust hooks as needed
5. Keep documentation current

## Technical Details

### Requirements
- Python 3.8+
- Claude Code with Task tool support
- Write access to `.claude/` directory

### Dependencies
Scripts use only Python standard library:
- `json` - JSON parsing
- `subprocess` - Git analysis
- `pathlib` - File operations
- `argparse` - CLI parsing

### Performance
- Analysis phase: 3-5 minutes (parallel execution)
- Implementation phase: 2-3 minutes (parallel execution)
- Validation phase: 1-2 minutes (sequential)
- **Total: ~10-15 minutes** for complete automation system

### Scalability
- 2-3 agents: Basic projects, solo developers
- 4-6 agents: Medium projects, small teams
- 7-10 agents: Large projects, comprehensive coverage
- 10+ agents: Enterprise projects, all domains

## Examples

### Web Application (Next.js)
See [EXAMPLE_WEB_APP.md](examples/EXAMPLE_WEB_APP.md)
- 6 agents (4 analysis, 2 implementation)
- 3 skills (TDD workflow, API docs, security checker)
- 3 commands (test-fix, security-scan, perf-check)
- 2 hooks (security validation, run tests)
- GitHub MCP integration

### Python CLI Tool
See [EXAMPLE_PYTHON_CLI.md](examples/EXAMPLE_PYTHON_CLI.md)
- 4 agents (2 analysis, 2 implementation)
- 2 skills (docstring generator, CLI test helper)
- 2 commands (test-cov, release-prep)
- 1 hook (auto-lint Python)
- Focused on documentation and testing

## Related Claude Code Features

This meta-skill leverages:
- **Task Tool** - For parallel agent execution
- **Skills System** - Creates auto-invoked capabilities
- **Commands** - Creates user-invoked shortcuts
- **Hooks** - Enables event-driven automation
- **MCP** - Connects to external services

## Support & Troubleshooting

### Check Session Logs
```bash
# Review what happened
cat .claude/agents/context/{session-id}/messages.jsonl | jq

# Find errors
jq 'select(.type == "error")' .claude/agents/context/{session-id}/messages.jsonl
```

### Agent Failed
```bash
# Check status
jq '.agents | to_entries | map(select(.value.status == "failed"))' \
  .claude/agents/context/{session-id}/coordination.json

# Options:
# 1. Retry the agent
# 2. Continue without it
# 3. Manual intervention
```

### Missing Reports
```bash
# List what was generated
ls .claude/agents/context/{session-id}/reports/

# Check if agent completed
jq '.agents["agent-name"]' \
  .claude/agents/context/{session-id}/coordination.json
```

## Future Enhancements

Potential additions:
- Language-specific analyzers (Go, Rust, Java)
- CI/CD integration agents
- Database optimization agent
- API design analyzer
- Accessibility checker
- Performance profiling agent
- Machine learning workflow agent

## License & Attribution

Part of the Claude Code ecosystem.
Generated with Meta-Automation Architect skill.

---

**Ready to use?** Simply say: `"Set up automation for my project"`

The meta-skill will guide you through the entire process with smart recommendations and generate a complete, customized automation system!
