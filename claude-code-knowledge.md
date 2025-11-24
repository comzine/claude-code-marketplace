# Claude Code Master Knowledge Base
*Comprehensive Guide to Skills, Agents, Commands, Hooks, and MCP Integration*

**Last Updated:** 2025-01-23
**Purpose:** Foundation for building meta-automation systems for different project types

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Skills System](#skills-system)
3. [Agents & Task Tool](#agents--task-tool)
4. [Custom Commands (Slash Commands)](#custom-commands-slash-commands)
5. [Hooks System](#hooks-system)
6. [MCP Integration](#mcp-integration)
7. [Integration & Orchestration](#integration--orchestration)
8. [Meta-Analysis for Automation](#meta-analysis-for-automation)
9. [Advanced Patterns & Best Practices](#advanced-patterns--best-practices)

---

## Architecture Overview

### Claude Code Ecosystem

Claude Code operates as an agentic terminal tool with four primary extension mechanisms:

```
┌─────────────────────────────────────────────────┐
│              Claude Code Core                    │
│  (Sonnet 4.5 - default, Haiku, Opus options)   │
└──────────┬──────────────────────────────────────┘
           │
    ┌──────┴──────┐
    │             │
    ▼             ▼
┌────────┐   ┌────────┐   ┌─────────┐   ┌──────┐
│ Skills │   │ Agents │   │Commands │   │Hooks │
│        │   │        │   │         │   │      │
└────┬───┘   └───┬────┘   └────┬────┘   └──┬───┘
     │           │             │            │
     └───────────┴─────────────┴────────────┘
                     │
                     ▼
            ┌─────────────────┐
            │  MCP Servers    │
            │  (External I/O) │
            └─────────────────┘
```

### Key Principles

1. **Model-Invoked vs User-Invoked**
   - Skills: Claude decides when to use based on context
   - Commands: User explicitly triggers with `/command`
   - Agents: Delegated tasks, can be triggered by both
   - Hooks: Automatically triggered at lifecycle points

2. **Scope Levels**
   - **Global**: `~/.claude/` (all projects, personal)
   - **Project**: `.claude/` (shared via git, team-wide)
   - **Session**: Runtime-specific configurations

3. **Context Management**
   - Skills loaded on-demand (no context penalty until used)
   - Agents run in isolated contexts
   - MCP servers extend available tools
   - Hooks inject at execution boundaries

---

## Skills System

### Fundamentals

**Definition**: Skills are organized folders containing instructions, scripts, and resources that agents can discover and load dynamically to perform specialized tasks.

**Key Characteristics:**
- **Modular**: Self-contained functionality
- **Dynamic**: Loaded only when needed
- **Discoverable**: Claude identifies when to use them
- **Lightweight**: No context cost until invoked

### Skill Structure

```
my-skill/
├── SKILL.md              # Required: Main definition file
│   ├── YAML frontmatter  # Metadata
│   └── Markdown content  # Instructions
├── scripts/              # Optional: Executable code
│   ├── process.py
│   └── analyze.sh
├── references/           # Optional: Documentation/data
│   ├── schema.md
│   └── examples.json
└── assets/              # Optional: Templates, resources
    ├── template.html
    └── icon.svg
```

### SKILL.md Format

```markdown
---
name: my-skill-name
description: Clear, concise description of when to use this skill (critical for auto-invocation)
license: MIT                          # Optional
allowed-tools: ["Bash", "Read"]       # Optional: Tool restrictions
metadata:                             # Optional
  version: "1.0"
  author: "Your Name"
---

# Skill Purpose

[Clear description of what this skill does]

## When to Use

- Specific trigger condition 1
- Specific trigger condition 2
- Context where this skill is valuable

## Instructions

1. Step-by-step process
2. Expected inputs/outputs
3. Error handling approach

## Examples

```bash
# Example usage
/command or natural language trigger
```

## Best Practices

- Guideline 1
- Guideline 2
```

### Creating Skills

**Method 1: Using init_skill.py**

```bash
# Initialize from template
python scripts/init_skill.py my-new-skill --path skills/

# Creates:
# skills/my-new-skill/
#   ├── SKILL.md (with TODO placeholders)
#   ├── scripts/ (example script)
#   ├── references/ (example reference)
#   └── assets/ (example asset)
```

**Method 2: Manual Creation**

```bash
mkdir -p .claude/skills/my-skill
cd .claude/skills/my-skill
touch SKILL.md
# Edit SKILL.md with proper frontmatter and content
```

**Method 3: Using Meta-Agent**

```bash
# Natural language skill creation
"Create a skill that analyzes code complexity and suggests refactoring"
# Claude Code delegates to meta-agent, which generates the skill file
```

### Skill Development Workflow

```mermaid
graph LR
    A[Define Purpose] --> B[Write SKILL.md]
    B --> C[Add Scripts/Resources]
    C --> D[Test with Claude]
    D --> E{Works?}
    E -->|No| F[Refine Instructions]
    F --> D
    E -->|Yes| G[Package & Deploy]
    G --> H[Monitor Usage]
    H --> I[Iterate Based on Feedback]
```

### Skill Best Practices

1. **Description is Critical**
   - Must clearly state WHEN to use the skill
   - Include trigger keywords Claude will recognize
   - Be specific about the context and task type

2. **Instructions Should Be**
   - Step-by-step and unambiguous
   - Include error handling guidance
   - Provide example usage
   - Define success criteria

3. **Tool Restrictions**
   - Use `allowed-tools` to limit what the skill can do
   - Enhances security and predictability
   - Example: `["Read", "Grep", "Glob"]` for read-only analysis

4. **Bundled Resources**
   - Keep scripts executable and well-documented
   - Reference files should be comprehensive
   - Assets should be self-contained

### Skill Categories & Examples

**1. Code Analysis Skills**
```markdown
---
name: security-auditor
description: Use proactively when reviewing code for security vulnerabilities, especially authentication, input validation, and data handling
---
```

**2. Workflow Automation Skills**
```markdown
---
name: test-runner
description: Automatically run tests and fix failures after code changes
allowed-tools: ["Bash", "Read", "Edit"]
---
```

**3. Documentation Skills**
```markdown
---
name: api-documenter
description: Generate comprehensive API documentation from code
allowed-tools: ["Read", "Write", "Grep"]
---
```

**4. Creative Skills**
```markdown
---
name: algorithmic-art
description: Generate p5.js-based interactive generative art
allowed-tools: ["Write", "Bash"]
---
```

### Validation & Packaging

```bash
# Validate skill structure
python scripts/quick_validate.py path/to/my-skill

# Package into distributable zip
python scripts/package_skill.py path/to/my-skill
# Output: my-skill.zip

# Custom output directory
python scripts/package_skill.py path/to/my-skill ./dist
# Output: dist/my-skill.zip
```

### Skill Installation & Management

**Global Skills:**
```bash
# Place in global directory
cp -r my-skill ~/.claude/skills/
```

**Project Skills:**
```bash
# Place in project directory
cp -r my-skill .claude/skills/
# Commit to git for team sharing
git add .claude/skills/my-skill
git commit -m "Add custom analysis skill"
```

**Using Skills:**
```bash
# Automatic (model-invoked)
"I need to analyze the security of this authentication code"
# Claude automatically invokes security-auditor skill

# Manual trigger via Skill tool
"Use the security-auditor skill on src/auth.js"
```

---

## Agents & Task Tool

### Agent Fundamentals

**Definition**: Agents are specialized Claude instances that run in isolated contexts to perform specific tasks. They enable parallel execution and task delegation.

**Types of Agents:**

1. **Built-in Subagents**
   - `Explore`: Fast codebase exploration (Haiku 4.5)
   - `Plan`: Complex task planning with structured execution
   - General-purpose: Multi-step task execution

2. **Custom Agents** (in `.claude/agents/`)
   - Project-specific specialists
   - Domain experts
   - Workflow orchestrators

3. **Plugin Agents**
   - Marketplace-provided agents
   - Community-contributed specialists

### Agent Configuration Structure

```markdown
---
name: agent-name
description: When to use this agent (critical for automatic delegation)
tools: Tool1, Tool2, Tool3    # Optional - inherits all if omitted
color: Cyan                   # Visual identifier in terminal
model: opus                   # Optional: haiku | sonnet | opus
---

# Purpose
You are a [role definition].

## Instructions
1. Step-by-step approach
2. What to analyze/create/fix
3. How to report results

## Response Format
- Specific format for reporting back to primary agent
- Include relevant data points
- Provide actionable insights
```

### Task Tool Usage

**Invoking Subagents:**

```python
# Python example using Task tool conceptually
# (Actual usage is through natural language or skill invocation)

# Single agent delegation
"Investigate what files implement the authentication feature using Task"

# Parallel agent execution
"Launch multiple agents to analyze security, performance, and maintainability"

# Sequential workflow
"First use code-analyzer to find issues, then optimizer to fix them"
```

**Agent Communication Patterns:**

```
Primary Agent
    │
    ├─> Task → Security Agent ──┐
    │                           │
    ├─> Task → Performance Agent ┤
    │                           │
    └─> Task → Maintainability ──┘
                │
                ▼
        Aggregated Results
                │
                ▼
        Primary Agent (synthesizes)
                │
                ▼
            User Output
```

### Creating Custom Agents

**Method 1: Manual Creation**

```bash
mkdir -p .claude/agents
cat > .claude/agents/test-runner.md << 'EOF'
---
name: test-runner
description: Use proactively to run tests and fix failures after code changes
tools: Bash, Read, Edit
color: Green
model: sonnet
---

You are a test automation expert. When you see code changes:

1. Identify affected test files
2. Run relevant test suite
3. Analyze failures
4. Fix issues while preserving test intent
5. Re-run to verify

## Test Frameworks
- Detect framework (pytest, jest, go test, etc.)
- Use appropriate commands
- Parse output correctly

## Reporting
- List test results
- Explain failures
- Document fixes applied
EOF
```

**Method 2: Using Meta-Agent**

```bash
"Build a new sub-agent that specializes in database query optimization"
# Meta-agent generates properly formatted agent file
```

### Agent Orchestration Patterns

**1. Sequential Execution**
```bash
# Chain of responsibility
"Use the explorer agent to map dependencies,
then the analyzer agent to find bottlenecks,
finally the optimizer agent to implement fixes"
```

**2. Parallel Execution**
```bash
# Concurrent analysis
"Launch security, performance, and accessibility agents in parallel
to review this component"
```

**3. Hierarchical Delegation**
```bash
# Manager pattern
"Have the architect agent design the system,
which will delegate to frontend and backend agents"
```

### Agent Best Practices

1. **Clear Role Definition**
   - Narrow, specific expertise
   - Well-defined input/output contract
   - Explicit success criteria

2. **Tool Restrictions**
   - Limit tools to what's needed
   - Enhances security and predictability
   - Example: Read-only agents shouldn't have Write access

3. **Communication Protocol**
   - Standardized response format
   - Include metadata (confidence, sources)
   - Provide actionable recommendations

4. **Error Handling**
   - Graceful degradation
   - Clear error messages
   - Suggested remediation steps

### Built-in Agent Capabilities

**Explore Agent:**
- Fast codebase navigation
- Pattern matching across files
- Minimal context usage
- Automatically triggered for open-ended searches

**Plan Agent:**
- Break down complex features into phases
- Uses Sonnet for planning, Haiku for execution
- Interactive question tool for clarification
- Structured implementation strategy

**Task Agent:**
- Complex search and investigation
- External information gathering
- Multi-step analysis
- Autonomous problem-solving

### Agent Selection Matrix

| Task Type | Recommended Agent | Why |
|-----------|------------------|-----|
| "Find files implementing X" | Explore | Fast, context-efficient |
| "How to implement Y" | Plan | Structured breakdown |
| "Research latest trends in Z" | Task | External data gathering |
| "Fix this bug" | Custom debugger | Specialized workflow |
| "Review security" | Custom security-auditor | Domain expertise |

---

## Custom Commands (Slash Commands)

### Fundamentals

**Definition**: Slash commands are user-initiated shortcuts that execute predefined prompts. They're essentially saved prompts accessible via `/command` syntax.

**Key Characteristics:**
- User-triggered (not model-invoked)
- Can accept arguments
- Support both project and personal scopes
- Simple Markdown files

### Command Structure

```markdown
---
allowed-tools: Bash(git:*), Read, Write
argument-hint: [optional-args]
description: Brief description shown in autocomplete
model: claude-3-5-haiku-20241022  # Optional: specific model
---

# Command Prompt

Main instructions for Claude to follow when this command is triggered.

## Inputs
- $ARGUMENTS: All arguments passed to command
- $1, $2, $3: Positional arguments

## Process
1. Step-by-step instructions
2. What to analyze/create
3. How to format output

## Output Format
- Specific format requirements
- File locations
- Reporting structure
```

### Command Locations

**Project Commands** (`.claude/commands/`):
- Shared via git
- Team-wide availability
- Project-specific workflows

**Personal Commands** (`~/.claude/commands/`):
- Local to your machine
- All projects
- Personal productivity tools

### Creating Commands

**Simple Command:**
```bash
# Create optimize command
echo "Analyze this code for performance issues and suggest optimizations" \
  > .claude/commands/optimize.md
```

**Command with Arguments:**
```bash
cat > .claude/commands/explain.md << 'EOF'
---
argument-hint: [file-path]
description: Explain code functionality in detail
---

# Code Explanation

Explain the code in $ARGUMENTS with:
1. High-level purpose
2. Key functions/classes
3. Dependencies
4. Usage examples
5. Potential improvements
EOF
```

**Command with Tool Restrictions:**
```bash
cat > .claude/commands/commit.md << 'EOF'
---
allowed-tools: Bash(git:*)
argument-hint: [message]
description: Create a git commit
---

# Git Commit

Create a commit with message: $ARGUMENTS

## Process
1. Run `git status` to see changes
2. Run `git add` for relevant files
3. Run `git commit` with message
4. Include co-author: "Co-Authored-By: Claude <noreply@anthropic.com>"
EOF
```

### Command Examples by Category

**1. Code Review Commands:**
```markdown
---
name: /review
description: Comprehensive code review with quality checks
---

Review this code for:
- Correctness and bugs
- Performance issues
- Security vulnerabilities
- Best practices violations
- Documentation quality

Provide prioritized feedback with specific examples.
```

**2. Documentation Commands:**
```markdown
---
name: /doc-api
allowed-tools: Read, Write
---

Generate API documentation for $ARGUMENTS:
1. Extract endpoints/functions
2. Document parameters and returns
3. Provide usage examples
4. Generate OpenAPI spec if applicable
```

**3. Testing Commands:**
```markdown
---
name: /test-gen
allowed-tools: Read, Write, Bash
---

Generate comprehensive tests for $ARGUMENTS:
1. Read the source file
2. Identify testable functions
3. Create test file with:
   - Unit tests
   - Edge cases
   - Integration tests
4. Run tests to verify they work
```

**4. Refactoring Commands:**
```markdown
---
name: /refactor
allowed-tools: Read, Edit, Bash
---

Safely refactor $ARGUMENTS:
1. Run existing tests
2. Apply SOLID principles
3. Improve readability
4. Reduce duplication
5. Re-run tests to ensure no breakage
```

**5. Project Setup Commands:**
```markdown
---
name: /setup-api
allowed-tools: Write, Bash
---

Set up a new API project with:
- Framework: $1 (express/fastapi/etc)
- Database: $2 (postgresql/mongodb/etc)
- Authentication: JWT
- Testing framework
- Docker configuration
- CI/CD pipeline
```

### Command Invocation

**Basic Usage:**
```bash
/optimize src/utils.js
/explain components/Header.tsx
/commit "Add user authentication feature"
```

**With Multiple Arguments:**
```bash
/setup-api express postgresql
/compare-files old.js new.js
```

**Chaining Commands:**
```bash
# Commands execute in sequence
/test-gen src/auth.js
# Wait for completion
/review src/auth.js
```

### Command Best Practices

1. **Clear Purpose**
   - One command = one responsibility
   - Descriptive name
   - Helpful argument hints

2. **Tool Safety**
   - Restrict tools to minimum needed
   - Be explicit about file operations
   - Use glob patterns for tool restrictions

3. **Documentation**
   - Include usage examples
   - Document expected arguments
   - Explain output format

4. **Error Handling**
   - Anticipate missing files
   - Validate argument counts
   - Provide helpful error messages

5. **Composability**
   - Design commands to work together
   - Output in useful formats
   - Support piping/chaining patterns

### Command Organization

```
.claude/commands/
├── git/
│   ├── commit.md
│   ├── pr-create.md
│   └── rebase.md
├── testing/
│   ├── test-gen.md
│   └── test-fix.md
├── docs/
│   ├── api-doc.md
│   └── readme.md
└── refactor/
    ├── optimize.md
    └── simplify.md
```

---

## Hooks System

### Fundamentals

**Definition**: Hooks are shell commands that execute at specific points in Claude Code's lifecycle, enabling automation, validation, and workflow customization.

**Key Characteristics:**
- Event-driven execution
- Can modify behavior (block operations)
- Support multiple hooks per event
- Execute sequentially within an event

### Hook Types & Trigger Points

| Hook Type | Trigger Point | Common Uses |
|-----------|---------------|-------------|
| **UserPromptSubmit** | User submits a prompt | Validation, context injection, logging |
| **PreToolUse** | Before tool execution | Validation, security checks, command modification |
| **PostToolUse** | After tool completion | Formatting, linting, cleanup |
| **Stop** | Agent finishes responding | Notifications, completion verification |
| **SessionStart** | New session begins | Environment setup, context loading |
| **SessionEnd** | Session terminates | Cleanup, archival |
| **Notification** | Claude awaits user input | Alerts, reminders |

### Hook Configuration

**settings.json Structure:**
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/user_prompt_submit.py --log-only"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/validate_bash.py"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/format_code.py"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/stop.py"
          }
        ]
      }
    ]
  }
}
```

### Hook Input/Output Protocol

**Input (JSON via stdin):**
```json
{
  "session": {
    "id": "session-uuid",
    "created_at": "2025-01-23T10:00:00Z"
  },
  "prompt": "User's prompt text",
  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf /",
    "description": "Delete everything"
  },
  "tool_response": {
    "success": true,
    "output": "Command output"
  }
}
```

**Output (JSON to stdout):**
```json
{
  "decision": "block",
  "reason": "Dangerous command detected",
  "context": "Additional context to add",
  "suppressOutput": false
}
```

**Exit Codes:**
- `0`: Success, continue
- `2`: Block operation, show error to Claude
- Other: Error, stop execution

### Hook Implementation Examples

**1. UserPromptSubmit: Logging & Validation**

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["python-dotenv"]
# ///

import json
import sys
from pathlib import Path
from datetime import datetime

# Read input
input_data = json.load(sys.stdin)
session_id = input_data.get('session', {}).get('id', 'unknown')
prompt = input_data.get('prompt', '')

# Log to file
log_dir = Path("logs")
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / f'{session_id}_prompts.json'

log_entry = {
    "timestamp": datetime.utcnow().isoformat() + 'Z',
    "session_id": session_id,
    "prompt": prompt
}

# Append to log
logs = []
if log_file.exists():
    with open(log_file, 'r') as f:
        logs = json.load(f)
logs.append(log_entry)

with open(log_file, 'w') as f:
    json.dump(logs, f, indent=2)

# Validate (optional)
if "rm -rf /" in prompt.lower():
    print("BLOCKED: Dangerous system deletion command detected", file=sys.stderr)
    sys.exit(2)

sys.exit(0)
```

**2. PreToolUse: Command Validation**

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

import json
import sys
import re

def is_dangerous_rm_command(command):
    """Detect dangerous rm -rf variations."""
    normalized = ' '.join(command.lower().split())
    patterns = [
        r'\brm\s+.*-[a-z]*r[a-z]*f',
        r'\brm\s+.*-[a-z]*f[a-z]*r',
        r'\brm\s+--recursive\s+--force',
    ]
    for pattern in patterns:
        if re.search(pattern, normalized):
            return True
    return False

# Read input
input_data = json.load(sys.stdin)
tool_name = input_data.get('tool_name', '')
tool_input = input_data.get('tool_input', {})

# Block dangerous commands
if tool_name == 'Bash':
    command = tool_input.get('command', '')
    if is_dangerous_rm_command(command):
        print("BLOCKED: Dangerous rm command detected", file=sys.stderr)
        print(f"Command: {command}", file=sys.stderr)
        sys.exit(2)

# Block .env file access
if tool_name in ['Read', 'Edit', 'Write']:
    file_path = tool_input.get('file_path', '')
    if '.env' in file_path and not file_path.endswith('.env.sample'):
        print("BLOCKED: Access to .env files prohibited", file=sys.stderr)
        sys.exit(2)

sys.exit(0)
```

**3. PostToolUse: Code Formatting**

```python
#!/usr/bin/env python3
import json
import sys
import subprocess
import os

# Read input
input_data = json.load(sys.stdin)
tool_name = input_data.get('tool_name', '')
file_path = input_data.get('tool_input', {}).get('file_path', '')

# Format based on file type
if tool_name in ['Edit', 'MultiEdit', 'Write'] and file_path:
    if file_path.endswith('.py'):
        # Format Python with black
        subprocess.run(['black', file_path], check=False)
    elif file_path.endswith(('.js', '.ts', '.tsx', '.jsx')):
        # Format JS/TS with prettier
        subprocess.run(['npx', 'prettier', '--write', file_path], check=False)
    elif file_path.endswith('.go'):
        # Format Go
        subprocess.run(['gofmt', '-w', file_path], check=False)

sys.exit(0)
```

**4. Stop: Completion Notification**

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///

import json
import sys
import subprocess

# Read input
input_data = json.load(sys.stdin)
stop_hook_active = input_data.get('stop_hook_active', False)

# Prevent infinite loops
if stop_hook_active:
    sys.exit(0)

# Desktop notification (macOS)
subprocess.run([
    'osascript', '-e',
    'display notification "Claude Code has finished" with title "Task Complete"'
])

sys.exit(0)
```

### Hook Patterns & Use Cases

**1. Security & Compliance**
- Block dangerous commands
- Prevent secret exposure
- Enforce coding standards
- Audit trail logging

**2. Workflow Automation**
- Auto-format on save
- Run tests after changes
- Update documentation
- Generate commit messages

**3. Context Enhancement**
- Inject project metadata
- Add environment info
- Include recent changes
- Load relevant documentation

**4. Quality Assurance**
- Lint code automatically
- Run static analysis
- Check test coverage
- Validate API contracts

**5. Integration & Deployment**
- Trigger CI/CD pipelines
- Update issue trackers
- Notify team channels
- Archive conversation logs

### Hook Best Practices

1. **Performance**
   - Keep hooks fast (< 1 second)
   - Use async operations where possible
   - Cache expensive computations
   - Avoid unnecessary file I/O

2. **Reliability**
   - Handle errors gracefully
   - Provide clear error messages
   - Log for debugging
   - Test thoroughly

3. **Security**
   - Validate all inputs
   - Sanitize file paths
   - Use subprocess safely
   - Limit hook permissions

4. **Maintainability**
   - Use uv single-file scripts
   - Document dependencies
   - Include usage examples
   - Version control hooks

5. **User Experience**
   - Suppress output when appropriate
   - Provide actionable feedback
   - Don't block unnecessarily
   - Make blocking reasons clear

### Advanced Hook Techniques

**Conditional Execution:**
```python
# Only run in production branches
git_branch = subprocess.check_output(['git', 'branch', '--show-current']).decode().strip()
if git_branch in ['main', 'production']:
    # Run strict checks
    pass
```

**Hook Composition:**
```json
{
  "PreToolUse": [
    {
      "matcher": "Bash",
      "hooks": [
        {"type": "command", "command": "hook1.py"},
        {"type": "command", "command": "hook2.py"},
        {"type": "command", "command": "hook3.py"}
      ]
    }
  ]
}
```

**Context Injection:**
```python
# Add project context to prompt
print(f"Project: {os.getenv('PROJECT_NAME', 'Unknown')}")
print(f"Branch: {get_git_branch()}")
print(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
print("---")  # Separator before user prompt
```

---

## MCP Integration

### Fundamentals

**Definition**: Model Context Protocol (MCP) is an open-source standard for connecting AI assistants to external tools, databases, and services.

**Key Characteristics:**
- Standardized protocol
- Tool & resource discovery
- Bidirectional communication
- Transport flexibility (stdio, HTTP, SSE)

### MCP Server Architecture

```
┌──────────────────┐
│   Claude Code    │
│                  │
│  ┌────────────┐  │
│  │ MCP Client │  │
│  └──────┬─────┘  │
└─────────┼────────┘
          │ JSON-RPC 2.0
          │
    ┌─────▼──────┐
    │ MCP Server │
    │            │
    │ ┌────────┐ │
    │ │ Tools  │ │
    │ ├────────┤ │
    │ │Resources│ │
    │ ├────────┤ │
    │ │Prompts │ │
    │ └────────┘ │
    └──────┬─────┘
           │
    ┌──────▼──────┐
    │ External    │
    │ Service API │
    └─────────────┘
```

### MCP Configuration

**settings.json Structure:**
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-github"],
      "oauth": {
        "clientId": "your-client-id",
        "clientSecret": "your-client-secret",
        "scopes": ["repo", "issues"]
      }
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/path/to/allowed/files"
      ]
    },
    "database": {
      "command": "npx",
      "args": ["-y", "postgresql-mcp@latest"],
      "env": {
        "DATABASE_URL": "postgresql://user:pass@localhost:5432/db",
        "MAX_CONNECTIONS": "10",
        "CONNECTION_TIMEOUT": "30000"
      }
    }
  }
}
```

### MCP Server Types

**1. API Integration Servers**
```json
{
  "github": {
    "command": "npx",
    "args": ["-y", "github-mcp@latest"],
    "env": {
      "GITHUB_TOKEN": "ghp_your_token",
      "GITHUB_API_URL": "https://api.github.com",
      "RATE_LIMIT_REQUESTS": "5000"
    }
  },
  "stripe": {
    "command": "npx",
    "args": ["-y", "stripe-mcp@latest"],
    "env": {
      "STRIPE_SECRET_KEY": "sk_test_your_key",
      "STRIPE_WEBHOOK_SECRET": "whsec_your_secret",
      "STRIPE_API_VERSION": "2023-10-16"
    }
  }
}
```

**2. Database Servers**
```json
{
  "postgresql": {
    "command": "npx",
    "args": ["-y", "postgresql-mcp@latest"],
    "env": {
      "DATABASE_URL": "postgresql://localhost:5432/db",
      "ENABLE_SSL": "true"
    }
  },
  "redis": {
    "command": "npx",
    "args": ["-y", "redis-mcp@latest"],
    "env": {
      "REDIS_URL": "redis://localhost:6379"
    }
  }
}
```

**3. File System Servers**
```json
{
  "filesystem": {
    "command": "npx",
    "args": [
      "-y",
      "filesystem-mcp@latest"
    ],
    "env": {
      "ALLOWED_PATHS": "/home/user/projects,/tmp",
      "MAX_FILE_SIZE": "10485760",
      "ALLOWED_EXTENSIONS": ".js,.ts,.json,.md,.txt"
    }
  }
}
```

**4. Custom MCP Servers**
```typescript
// TypeScript MCP Server Example
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new Server(
  { name: "weather-server", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

// Define tool with Zod validation
const GetWeatherInput = z.object({
  location: z.string().describe("City name"),
  units: z.enum(["imperial", "metric"]).default("imperial")
});

// Register tool
server.registerTool({
  name: "get_weather",
  description: "Get current weather for a location",
  inputSchema: {
    type: "object",
    properties: {
      location: { type: "string" },
      units: { type: "string", enum: ["imperial", "metric"] }
    },
    required: ["location"]
  },
  annotations: {
    readOnlyHint: true,
    openWorldHint: true
  }
}, async (args) => {
  const { location, units } = GetWeatherInput.parse(args);
  // Fetch weather data
  const response = await fetch(
    `https://api.weather.com/v1/weather?q=${location}&units=${units}`
  );
  return {
    content: [{ type: "text", text: JSON.stringify(await response.json()) }]
  };
});

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
```

### MCP Tool Patterns

**1. Tool Definition**
```typescript
{
  name: "tool_name",
  description: "What this tool does",
  inputSchema: {
    type: "object",
    properties: {
      param1: { type: "string", description: "Parameter description" },
      param2: { type: "number", minimum: 1, maximum: 100 }
    },
    required: ["param1"]
  },
  annotations: {
    title: "Human-readable title",
    readOnlyHint: true,      // Doesn't modify state
    destructiveHint: false,   // Not destructive
    idempotentHint: true,     // Same result on repeated calls
    openWorldHint: false      // Doesn't interact with external entities
  }
}
```

**2. Resource Definition**
```typescript
{
  uri: "resource://schema/users",
  name: "Users Schema",
  description: "Database schema for users table",
  mimeType: "application/json"
}
```

**3. Prompt Templates**
```typescript
{
  name: "analyze_code",
  description: "Analyze code for issues",
  arguments: [
    {
      name: "file_path",
      description: "Path to file to analyze",
      required: true
    }
  ]
}
```

### MCP Management Commands

```bash
# Add MCP server via CLI
claude mcp add

# List configured servers
claude mcp list

# Enable/disable via @-mention
@github help

# Debug MCP issues
claude --mcp-debug

# Serve MCP servers for testing
claude mcp serve
```

### MCP Best Practices

**1. Security**
- Trust MCP servers before installing
- Be cautious with servers that fetch untrusted content
- Use environment variables for secrets
- Implement rate limiting
- Validate all inputs with JSON Schema

**2. Performance**
- Keep tool operations fast
- Implement caching where appropriate
- Use pagination for large result sets
- Batch related operations
- Monitor resource usage

**3. Error Handling**
```typescript
try {
  const result = await performOperation();
  return {
    content: [{ type: "text", text: JSON.stringify(result) }]
  };
} catch (error) {
  return {
    isError: true,
    content: [{ type: "text", text: `Error: ${error.message}` }]
  };
}
```

**4. Tool Design**
- Use clear, descriptive names
- Include service prefix (e.g., `github_create_issue`)
- Be action-oriented (verbs)
- Provide comprehensive descriptions
- Document all parameters

**5. Testing & Validation**
```bash
# Validate JSON Schema
python scripts/quick_validate.py server/

# Test with evaluation harness
python scripts/evaluation.py server-eval.xml

# Integration tests
pytest tests/integration/
```

### Popular MCP Servers

**Official Servers:**
- `@anthropic-ai/mcp-server-github`: GitHub integration
- `@modelcontextprotocol/server-filesystem`: File system access
- `@modelcontextprotocol/server-sqlite`: SQLite databases
- `@anthropic-ai/mcp-server-brave-search`: Web search

**Community Servers:**
- PostgreSQL, MySQL, MongoDB: Database access
- Slack, Discord: Team communication
- Jira, Linear: Project management
- AWS, Google Cloud: Cloud services

### MCP Development Workflow

```mermaid
graph TD
    A[Define Tool Requirements] --> B[Create MCP Server]
    B --> C[Implement Tools/Resources]
    C --> D[Add JSON Schema Validation]
    D --> E[Test Locally]
    E --> F{Tests Pass?}
    F -->|No| C
    F -->|Yes| G[Add to Claude Config]
    G --> H[Test with Claude Code]
    H --> I{Works Correctly?}
    I -->|No| J[Debug with --mcp-debug]
    J --> C
    I -->|Yes| K[Document & Deploy]
```

---

## Integration & Orchestration

### When to Use Each Feature

```
Decision Tree:

User wants to...
├─ Execute a saved prompt
│  └─> Use Custom Command (/command)
│
├─ Extend Claude's capabilities permanently
│  └─> Create Skill (model-invoked)
│
├─ Delegate a specialized task
│  └─> Use Agent/Task Tool
│
├─ Automate workflow at lifecycle points
│  └─> Implement Hooks
│
└─ Connect to external services
   └─> Configure MCP Server
```

### Feature Combination Patterns

**1. Skill + MCP Integration**
```markdown
---
name: github-issue-analyzer
description: Analyze GitHub issues and provide insights
allowed-tools: ["mcp__github__*"]
---

# GitHub Issue Analysis

Use GitHub MCP tools to:
1. Fetch recent issues
2. Analyze patterns
3. Suggest prioritization
4. Generate summary report
```

**2. Command + Agent Delegation**
```markdown
---
name: /multi-agent-review
description: Launch multiple review agents in parallel
---

Launch specialized agents for comprehensive review:

1. Security agent: Check for vulnerabilities
2. Performance agent: Identify bottlenecks
3. Accessibility agent: Validate WCAG compliance

Aggregate results and provide unified report.
```

**3. Hook + MCP Automation**
```python
# PostToolUse hook
# After file edits, update project tracking via Linear MCP

import json
import sys

input_data = json.load(sys.stdin)
if input_data.get('tool_name') == 'Edit':
    file_path = input_data.get('tool_input', {}).get('file_path', '')
    # Trigger Linear MCP to update task
    # (Implementation details omitted for brevity)
```

**4. Skill + Custom Command + Hook**
```
Workflow: Automated Code Review

1. Command: /review [file]
   ├─> Invokes code-review skill
   │   ├─> Uses MCP (GitHub) to fetch PR context
   │   └─> Delegates to review agents
   │
2. Hook: PostToolUse
   └─> Auto-commits review comments
       └─> Uses MCP (Linear) to update task status
```

### Multi-Agent Orchestration

**Sequential Pattern:**
```
User Request
    │
    ▼
Primary Agent
    │
    ├─> Agent 1: Explore codebase
    │   └─> Returns: File list
    │       │
    │       ▼
    ├─> Agent 2: Analyze dependencies
    │   └─> Returns: Dependency graph
    │       │
    │       ▼
    └─> Agent 3: Generate report
        └─> Returns: Final analysis
```

**Parallel Pattern:**
```
User Request
    │
    ▼
Primary Agent
    │
    ├─> Agent 1: Security audit ───┐
    │                              │
    ├─> Agent 2: Performance test ─┤
    │                              │
    └─> Agent 3: Code quality ─────┘
                │
                ▼
        Aggregate Results
                │
                ▼
        Synthesized Report
```

**Hierarchical Pattern:**
```
Architect Agent
    │
    ├─> Frontend Team
    │   ├─> React Specialist
    │   ├─> CSS Expert
    │   └─> Accessibility Reviewer
    │
    └─> Backend Team
        ├─> API Designer
        ├─> Database Optimizer
        └─> Security Auditor
```

### Complex Workflow Example

**E-commerce Feature Development:**

```yaml
Workflow: Add Payment Integration

Phase 1: Planning (Plan Agent)
├─ Analyze requirements
├─ Design architecture
└─ Create implementation plan

Phase 2: Development (Parallel Agents)
├─ Backend Agent
│  ├─ Implement payment API endpoints
│  ├─ Add Stripe MCP integration
│  └─ Write unit tests
│
├─ Frontend Agent
│  ├─ Create payment UI components
│  ├─ Integrate with backend API
│  └─ Add form validation
│
└─ Database Agent
   ├─ Design payment tables schema
   ├─ Create migrations
   └─ Add indexes

Phase 3: Quality Assurance (Sequential Agents)
├─ Test Runner Agent: Execute test suite
├─ Security Agent: Audit for vulnerabilities
├─ Performance Agent: Load testing
└─ Code Review Agent: Final review

Phase 4: Deployment (Hooks + MCP)
├─ PreToolUse Hook: Validate deployment target
├─ Deployment Command: /deploy production
├─ PostToolUse Hook: Run smoke tests
└─ MCP (Slack): Notify team of deployment
```

### Context Management Strategies

**1. Progressive Context Loading**
- Start with minimal context
- Load skills/resources on-demand
- Use Explore agent for large codebases
- Cache frequently accessed data

**2. Context Boundaries**
- Isolate agent contexts
- Share only necessary information
- Use MCP for external data
- Clear context between phases

**3. Context Compression**
- Use `/compact` command
- Summarize completed work
- Remove obsolete information
- Maintain only relevant history

---

## Meta-Analysis for Automation

### Identifying Automation Opportunities

**Framework for Analysis:**

```
Project Assessment
    │
    ├─> Project Type
    │   ├─ Web Application
    │   ├─ CLI Tool
    │   ├─ Data Science
    │   ├─ Educational Content
    │   └─ Other
    │
    ├─> Repetitive Tasks
    │   ├─ Code generation patterns
    │   ├─ Testing workflows
    │   ├─ Documentation updates
    │   └─ Deployment procedures
    │
    ├─> Team Workflows
    │   ├─ Code review process
    │   ├─ PR conventions
    │   ├─ Git workflows
    │   └─ Communication patterns
    │
    └─> External Integrations
        ├─ Issue tracking
        ├─ CI/CD systems
        ├─ Databases
        └─ APIs
```

### Project Type Automation Patterns

**1. Web Application Projects**

**Skills:**
- `component-generator`: Generate React/Vue/Angular components
- `api-endpoint-creator`: Scaffold REST/GraphQL endpoints
- `database-migration-helper`: Create and manage migrations
- `accessibility-checker`: WCAG compliance validation

**Commands:**
- `/new-component [name]`: Create component with tests and styles
- `/api-endpoint [resource]`: Generate CRUD endpoint
- `/db-migrate [description]`: Create migration file

**Hooks:**
- PreToolUse: Validate component naming conventions
- PostToolUse: Run linter and formatter
- Stop: Run test suite and report coverage

**MCP:**
- Database servers for query analysis
- GitHub for PR automation
- Vercel/Netlify for deployment

**2. CLI Tool Projects**

**Skills:**
- `cli-command-generator`: Create command structure
- `argument-parser-helper`: Implement argument parsing
- `doc-generator`: Generate man pages and help text

**Commands:**
- `/new-command [name]`: Scaffold command file
- `/add-flag [flag] [description]`: Add command flag
- `/test-cli [command]`: Test CLI behavior

**Hooks:**
- PostToolUse: Update help documentation
- Stop: Build and test binary

**MCP:**
- Filesystem for config management
- Package registries (npm, PyPI, cargo)

**3. Data Science Projects**

**Skills:**
- `notebook-cleaner`: Clean and optimize Jupyter notebooks
- `data-validator`: Validate data schemas
- `visualization-generator`: Create standard plots

**Commands:**
- `/analyze-dataset [file]`: Statistical analysis
- `/create-viz [type] [data]`: Generate visualization
- `/model-eval [model]`: Evaluate model performance

**Hooks:**
- PostToolUse: Re-run notebooks on code changes
- Stop: Generate experiment report

**MCP:**
- Database servers for data access
- MLflow for experiment tracking
- S3/GCS for data storage

**4. Educational Content Projects**

**Skills:**
- `tutorial-generator`: Create step-by-step tutorials
- `exercise-creator`: Generate practice exercises
- `quiz-generator`: Create assessment questions

**Commands:**
- `/new-lesson [topic]`: Scaffold lesson structure
- `/add-exercise [type]`: Create exercise with solution
- `/export-course`: Package course materials

**Hooks:**
- PostToolUse: Validate markdown formatting
- Stop: Generate table of contents

**MCP:**
- GitHub for version control
- LMS APIs for publishing

### Meta-Skill Design Template

```markdown
---
name: meta-automation-builder
description: Analyze project and generate comprehensive automation system
---

# Meta-Automation Builder

Analyze the project and create a complete automation system tailored to its needs.

## Process

### 1. Project Discovery
- Identify project type and tech stack
- Analyze existing workflows
- Find repetitive tasks
- Map external dependencies

### 2. Automation Design
- Recommend skills to create
- Design custom commands
- Plan hook automation points
- Identify MCP integrations

### 3. Implementation
For each recommended automation:
- Generate skill/command/hook files
- Configure MCP servers
- Write documentation
- Create usage examples

### 4. Testing & Validation
- Test each automation
- Verify integrations work
- Validate workflow improvements
- Document limitations

### 5. Delivery
- Package all automations
- Create setup guide
- Provide usage documentation
- Include customization tips

## Output Format

```markdown
# Automation System for [Project Name]

## Project Analysis
- Type: [Web App/CLI/Data Science/etc]
- Tech Stack: [Languages, frameworks]
- Team Size: [Solo/Small/Large]
- Key Pain Points: [List identified issues]

## Recommended Automations

### Skills
1. **skill-name**
   - Purpose: [What it does]
   - Trigger: [When to use]
   - Files: [Where to place]

### Commands
1. **/command-name**
   - Purpose: [What it does]
   - Usage: [Example invocation]
   - Arguments: [Parameter description]

### Hooks
1. **HookType**
   - Trigger: [When it runs]
   - Action: [What it does]
   - Impact: [Expected benefit]

### MCP Integrations
1. **server-name**
   - Purpose: [What service it connects to]
   - Tools: [Available operations]
   - Setup: [Configuration steps]

## Implementation Guide
[Step-by-step setup instructions]

## Usage Examples
[Real-world scenarios with commands]

## Maintenance
[How to update and extend]
```
```

### Automation Assessment Checklist

**Before Automating, Ask:**

1. **Frequency**: How often is this task performed?
   - Daily → High priority for automation
   - Weekly → Medium priority
   - Rarely → May not be worth automating

2. **Complexity**: How complex is the task?
   - Simple repetition → Command or skill
   - Multi-step workflow → Agent + hooks
   - Decision-making required → Skill with clear guidelines

3. **Consistency**: Does the task follow a pattern?
   - Highly consistent → Automate fully
   - Some variation → Parameterize
   - Highly variable → Provide templates

4. **Impact**: What's the benefit of automation?
   - Time saved per execution
   - Error reduction
   - Quality improvement
   - Team consistency

5. **Maintenance**: How stable is the task?
   - Stable process → Safe to automate
   - Evolving → Build flexibility in
   - Experimental → Wait for stabilization

### Automation Architecture Decision Matrix

| Scenario | Best Approach | Why |
|----------|---------------|-----|
| Saved prompt with args | Custom Command | User-triggered, simple |
| Reusable logic Claude should discover | Skill | Model-invoked, context-aware |
| Multi-step specialized task | Agent | Isolated execution, delegation |
| Action at specific lifecycle point | Hook | Event-driven, automation |
| External service integration | MCP | Standardized protocol, discovery |
| Combination of above | Orchestration | Leverage all features together |

---

## Advanced Patterns & Best Practices

### Development Workflow Optimization

**1. Feature Development Pattern**
```
/plan                    # Create implementation plan
  ↓
/feature-dev [feature]   # Architect & implement
  ↓
[Hooks auto-run tests]   # Validate changes
  ↓
/review                  # Code review agent
  ↓
/commit [message]        # Create commit
  ↓
/pr-create               # Generate PR
```

**2. Debugging Workflow**
```
/systematic-debug        # Structured debugging approach
  ↓
[Root cause skill]      # Identify issue
  ↓
[Fix implementation]     # Apply solution
  ↓
[Hooks verify fix]       # Re-run tests
  ↓
/commit-fix              # Document fix
```

**3. Refactoring Workflow**
```
/analyze-debt           # Technical debt analysis
  ↓
/refactor --safe        # Incremental refactoring
  ↓
[Hooks run full suite]  # Ensure no breakage
  ↓
/review-changes         # Verify improvements
```

### Testing Automation

**Skill: test-driven-development**
```markdown
---
name: tdd
description: Implement TDD workflow: red-green-refactor cycle
---

# Test-Driven Development

1. **Red**: Write failing test
2. **Green**: Minimal code to pass
3. **Refactor**: Improve without breaking

Always write test first, watch it fail, then implement.
```

**Hook: Auto-test runner**
```python
# PostToolUse hook
if tool_name in ['Edit', 'Write']:
    file_path = tool_input['file_path']
    if is_source_file(file_path):
        run_relevant_tests(file_path)
```

**Command: /test-fix**
```markdown
Fix failing tests:
1. Run test suite
2. Analyze failures
3. Fix issues preserving test intent
4. Verify all pass
```

### Security & Compliance

**Hook: Security validation**
```python
# PreToolUse: Block dangerous operations
FORBIDDEN_PATTERNS = [
    r'rm\s+-rf\s+/',
    r'eval\s*\(',
    r'exec\s*\(',
    r'\.env[^.sample]'
]
```

**Skill: security-auditor**
```markdown
---
name: security-auditor
description: Comprehensive security audit for web applications
---

Check for:
- SQL injection
- XSS vulnerabilities
- CSRF protection
- Authentication flaws
- Authorization bypasses
- Sensitive data exposure
```

**MCP: Secret scanning**
```json
{
  "trufflehog": {
    "command": "trufflehog",
    "args": ["filesystem", "."]
  }
}
```

### Documentation Automation

**Skill: api-documenter**
```markdown
---
name: api-documenter
description: Generate comprehensive API documentation from code
---

Create documentation including:
- Endpoint descriptions
- Request/response schemas
- Authentication requirements
- Example requests
- Error codes
```

**Hook: Auto-update docs**
```python
# PostToolUse: Update docs when API changes
if is_api_file(file_path):
    regenerate_openapi_spec()
    update_readme()
```

**Command: /doc-sync**
```markdown
Synchronize documentation:
1. Extract API definitions
2. Generate OpenAPI spec
3. Update README
4. Generate client SDKs
```

### Performance Monitoring

**Skill: performance-profiler**
```markdown
---
name: perf-profiler
description: Analyze and optimize performance bottlenecks
allowed-tools: ["Bash", "Read", "Write"]
---

1. Profile application
2. Identify slow operations
3. Suggest optimizations
4. Implement fixes
5. Verify improvements
```

**MCP: Performance tracking**
```json
{
  "datadog": {
    "command": "datadog-mcp",
    "env": {
      "DD_API_KEY": "${DATADOG_API_KEY}",
      "DD_SITE": "datadoghq.com"
    }
  }
}
```

### Continuous Integration

**Hook: Pre-commit validation**
```python
# UserPromptSubmit: Check if committing
if "commit" in prompt.lower():
    # Run pre-commit checks
    run_linter()
    run_tests()
    check_coverage()
```

**Skill: ci-cd-helper**
```markdown
---
name: ci-cd
description: Assist with CI/CD pipeline configuration and debugging
---

Help with:
- Pipeline configuration
- Build script optimization
- Test parallelization
- Deployment automation
- Rollback procedures
```

### Team Collaboration

**Skill: pr-reviewer**
```markdown
---
name: pr-reviewer
description: Comprehensive pull request review
---

Review checklist:
- Code quality
- Test coverage
- Documentation
- Breaking changes
- Performance impact
- Security considerations
```

**Hook: PR automation**
```python
# Stop: After completing feature
if feature_complete():
    create_pr_description()
    assign_reviewers()
    add_labels()
    notify_team()
```

**MCP: Team communication**
```json
{
  "slack": {
    "command": "slack-mcp",
    "env": {
      "SLACK_TOKEN": "${SLACK_BOT_TOKEN}",
      "CHANNEL_ID": "${TEAM_CHANNEL}"
    }
  }
}
```

### Best Practices Summary

**Skills:**
- ✅ Clear, specific descriptions
- ✅ Focused, single-purpose
- ✅ Comprehensive instructions
- ✅ Include usage examples
- ❌ Don't make too generic
- ❌ Don't omit error handling

**Commands:**
- ✅ Descriptive names
- ✅ Clear argument hints
- ✅ Restrict tools appropriately
- ✅ Document expected output
- ❌ Don't create command bloat
- ❌ Don't duplicate skill functionality

**Agents:**
- ✅ Specialized roles
- ✅ Clear delegation criteria
- ✅ Defined response format
- ✅ Appropriate tool access
- ❌ Don't create overlapping agents
- ❌ Don't give unlimited tool access

**Hooks:**
- ✅ Fast execution (< 1s)
- ✅ Clear error messages
- ✅ Proper exit codes
- ✅ Minimal dependencies
- ❌ Don't block unnecessarily
- ❌ Don't create infinite loops

**MCP:**
- ✅ Secure configuration
- ✅ Comprehensive schemas
- ✅ Error handling
- ✅ Rate limiting
- ❌ Don't trust untrusted servers
- ❌ Don't expose secrets

---

## Appendix: Quick Reference

### Feature Comparison

| Feature | Trigger | Scope | State | Use Case |
|---------|---------|-------|-------|----------|
| **Skill** | Model-invoked | Global/Project | Stateless | Reusable capabilities |
| **Command** | User-invoked | Global/Project | Stateless | Saved prompts |
| **Agent** | Delegated | Session | Isolated | Specialized tasks |
| **Hook** | Event-driven | Global/Project | Transient | Automation |
| **MCP** | Tool discovery | Global/Project | Persistent | External integration |

### Common Commands

```bash
# Skills
ls ~/.claude/skills/              # List global skills
ls .claude/skills/                # List project skills

# Commands
ls ~/.claude/commands/            # List global commands
ls .claude/commands/              # List project commands
/command [args]                   # Execute command

# Agents
/agents                           # Open agents interface
ls .claude/agents/                # List custom agents

# MCP
claude mcp add                    # Add MCP server
claude mcp list                   # List servers
claude --mcp-debug                # Debug MCP

# Plugins
/plugin marketplace               # Browse plugins
/plugin install [name]            # Install plugin
/plugin enable [name]             # Enable plugin
```

### File Locations

```
~/.claude/                        # Global Claude Code config
├── settings.json                 # Main configuration
├── commands/                     # Global commands
├── skills/                       # Global skills
└── data/                         # Session data

.claude/                          # Project-specific config
├── settings.json                 # Project settings
├── commands/                     # Project commands
├── skills/                       # Project skills
├── agents/                       # Custom agents
└── hooks/                        # Hook scripts
```

### Environment Variables

```bash
# API Configuration
export ANTHROPIC_API_KEY=sk-ant-...
export OPENAI_API_KEY=sk-...

# Model Selection
export ANTHROPIC_DEFAULT_SONNET_MODEL=claude-sonnet-4-5

# MCP Configuration
export GITHUB_TOKEN=ghp_...
export DATABASE_URL=postgresql://...

# Debug Options
export CLAUDE_CODE_EXIT_AFTER_STOP_DELAY=5000
export CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1
```

### Common Patterns

**1. Initialize Project Automation:**
```bash
mkdir -p .claude/{commands,skills,agents,hooks}
touch .claude/settings.json
# Configure settings.json with hooks and MCP
```

**2. Create Skill:**
```bash
python scripts/init_skill.py my-skill --path .claude/skills/
# Edit .claude/skills/my-skill/SKILL.md
python scripts/package_skill.py .claude/skills/my-skill
```

**3. Add Command:**
```bash
cat > .claude/commands/mycommand.md << 'EOF'
---
description: My custom command
---
# Instructions here
EOF
```

**4. Configure Hook:**
```bash
# Add to .claude/settings.json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit",
      "hooks": [{
        "type": "command",
        "command": "python .claude/hooks/format.py"
      }]
    }]
  }
}
```

**5. Add MCP Server:**
```json
{
  "mcpServers": {
    "my-service": {
      "command": "npx",
      "args": ["-y", "my-mcp-server"],
      "env": {
        "API_KEY": "${MY_API_KEY}"
      }
    }
  }
}
```

---

## Conclusion

This knowledge base provides the foundation for building comprehensive automation systems for any project type. The meta-skill should:

1. **Analyze** the project context
2. **Identify** automation opportunities
3. **Design** appropriate solutions using skills, commands, agents, hooks, and MCP
4. **Generate** all necessary files and configurations
5. **Document** usage and maintenance procedures

By understanding these core concepts and patterns, you can create intelligent automation systems tailored to specific project needs, dramatically improving development velocity and code quality.

---

**Version:** 1.0
**Last Updated:** 2025-01-23
**Next Steps:** Use this knowledge to build the meta-skill for automation system generation
