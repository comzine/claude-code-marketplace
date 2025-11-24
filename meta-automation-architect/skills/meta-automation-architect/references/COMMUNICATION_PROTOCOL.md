# Agent Communication Protocol (ACP)

The Agent Communication Protocol enables parallel subagents with isolated contexts to coordinate and share information through a structured file-based system.

## Core Principles

1. **Asynchronous** - Agents don't block each other
2. **Discoverable** - Any agent can read any report
3. **Persistent** - Survives agent crashes and restarts
4. **Transparent** - Complete event log for debugging
5. **Atomic** - File operations are append-only or replace-whole
6. **Orchestratable** - Coordinator manages dependencies

## Directory Structure

```
.claude/agents/context/{session-id}/
  ├── coordination.json       # Status tracking and dependencies
  ├── messages.jsonl          # Append-only event log
  ├── reports/               # Standardized agent outputs
  │   ├── {agent-name}.json
  │   └── ...
  └── data/                  # Shared data artifacts
      ├── {artifact-name}.json
      └── ...
```

### Session ID

Each automation generation gets a unique session ID (UUID):

```bash
SESSION_ID=$(uuidgen | tr '[:upper:]' '[:lower:]')
export CLAUDE_SESSION_ID="${SESSION_ID}"
```

All agents receive this session ID and use it to locate the context directory.

## Communication Components

### 1. Coordination File (`coordination.json`)

Central status tracking for all agents.

**Structure:**

```json
{
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "started_at": "2025-01-23T10:00:00Z",
  "project_type": "web_app",
  "project_path": "/path/to/project",
  "agents": {
    "security-analyzer": {
      "status": "completed",
      "started_at": "2025-01-23T10:00:00Z",
      "completed_at": "2025-01-23T10:05:00Z",
      "report_path": "reports/security-analyzer.json",
      "dependencies": [],
      "progress": "Analysis complete"
    },
    "performance-analyzer": {
      "status": "in_progress",
      "started_at": "2025-01-23T10:00:00Z",
      "progress": "Analyzing database queries...",
      "dependencies": []
    },
    "skill-generator": {
      "status": "waiting",
      "dependencies": ["security-analyzer", "performance-analyzer", "code-quality-analyzer"],
      "reason": "Waiting for analysis agents to complete"
    }
  }
}
```

**Agent Status Values:**

- `waiting` - Not started, may have dependencies
- `in_progress` - Currently executing
- `completed` - Finished successfully
- `failed` - Encountered error

**Reading Coordination:**

```bash
# Check all agent statuses
jq '.agents' .claude/agents/context/${SESSION_ID}/coordination.json

# Check specific agent
jq '.agents["security-analyzer"]' .claude/agents/context/${SESSION_ID}/coordination.json

# List completed agents
jq '.agents | to_entries | map(select(.value.status == "completed")) | map(.key)' \
  .claude/agents/context/${SESSION_ID}/coordination.json

# List waiting agents with dependencies
jq '.agents | to_entries | map(select(.value.status == "waiting")) | map({name: .key, deps: .value.dependencies})' \
  .claude/agents/context/${SESSION_ID}/coordination.json
```

**Updating Coordination:**

```bash
# Update status to in_progress
cat .claude/agents/context/${SESSION_ID}/coordination.json | \
  jq '.agents["my-agent"] = {
    "status": "in_progress",
    "started_at": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'",
    "progress": "Starting analysis",
    "dependencies": []
  }' > /tmp/coord.json && \
  mv /tmp/coord.json .claude/agents/context/${SESSION_ID}/coordination.json

# Update to completed
cat .claude/agents/context/${SESSION_ID}/coordination.json | \
  jq '.agents["my-agent"].status = "completed" |
      .agents["my-agent"].completed_at = "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'" |
      .agents["my-agent"].report_path = "reports/my-agent.json"' > /tmp/coord.json && \
  mv /tmp/coord.json .claude/agents/context/${SESSION_ID}/coordination.json
```

### 2. Message Bus (`messages.jsonl`)

Append-only log of all events. Each line is a JSON object.

**Event Types:**

- `status` - Progress updates
- `finding` - Discovery of issues or insights
- `error` - Failures or problems
- `data` - Data artifact creation
- `completed` - Agent completion announcement

**Event Format:**

```json
{"timestamp":"2025-01-23T10:00:00Z","from":"security-analyzer","type":"status","message":"Starting security analysis"}
{"timestamp":"2025-01-23T10:02:15Z","from":"security-analyzer","type":"finding","severity":"high","data":{"title":"SQL Injection Risk","location":"src/db/queries.ts:42"}}
{"timestamp":"2025-01-23T10:03:00Z","from":"security-analyzer","type":"data","artifact":"data/vulnerabilities.json","description":"Detailed vulnerability data"}
{"timestamp":"2025-01-23T10:05:00Z","from":"security-analyzer","type":"completed","message":"Analysis complete. Found 5 high-severity issues."}
```

**Writing Events:**

```bash
# Log status update
echo "{\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"from\":\"my-agent\",\"type\":\"status\",\"message\":\"Starting analysis\"}" >> \
  .claude/agents/context/${SESSION_ID}/messages.jsonl

# Log finding
echo "{\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"from\":\"my-agent\",\"type\":\"finding\",\"severity\":\"high\",\"data\":{\"title\":\"Issue found\",\"location\":\"file:line\"}}" >> \
  .claude/agents/context/${SESSION_ID}/messages.jsonl

# Log completion
echo "{\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"from\":\"my-agent\",\"type\":\"completed\",\"message\":\"Analysis complete\"}" >> \
  .claude/agents/context/${SESSION_ID}/messages.jsonl
```

**Reading Events:**

```bash
# Watch live events
tail -f .claude/agents/context/${SESSION_ID}/messages.jsonl | jq

# Get events from specific agent
jq 'select(.from == "security-analyzer")' .claude/agents/context/${SESSION_ID}/messages.jsonl

# Get events by type
jq 'select(.type == "finding")' .claude/agents/context/${SESSION_ID}/messages.jsonl

# Get high-severity findings
jq 'select(.type == "finding" and .severity == "high")' .claude/agents/context/${SESSION_ID}/messages.jsonl

# Count events by type
jq -s 'group_by(.type) | map({type: .[0].type, count: length})' \
  .claude/agents/context/${SESSION_ID}/messages.jsonl

# Timeline of agent activity
jq -s 'sort_by(.timestamp) | .[] | "\(.timestamp) [\(.from)] \(.type): \(.message // .data.title // "no message")"' \
  .claude/agents/context/${SESSION_ID}/messages.jsonl -r
```

### 3. Agent Reports (`reports/{agent-name}.json`)

Standardized output from each agent.

**Standard Report Format:**

```json
{
  "agent_name": "security-analyzer",
  "timestamp": "2025-01-23T10:05:00Z",
  "status": "completed",
  "summary": "Brief 2-3 sentence overview of findings",

  "findings": [
    {
      "type": "issue|recommendation|info",
      "severity": "high|medium|low",
      "title": "Short title",
      "description": "Detailed description of the finding",
      "location": "file:line or component",
      "recommendation": "What to do about it",
      "example": "Code snippet or example (optional)"
    }
  ],

  "metrics": {
    "items_analyzed": 150,
    "issues_found": 5,
    "high_severity": 2,
    "medium_severity": 2,
    "low_severity": 1,
    "time_taken": "2m 34s"
  },

  "data_artifacts": [
    "data/vulnerabilities.json",
    "data/dependency-graph.json"
  ],

  "next_actions": [
    "Fix SQL injection in queries.ts",
    "Update vulnerable dependencies",
    "Add input validation to API routes"
  ],

  "recommendations_for_automation": [
    "Skill: SQL injection checker that runs on code changes",
    "Command: /security-scan for quick manual checks",
    "Hook: Validate queries on PreToolUse for Write operations",
    "MCP: Integrate with security scanning service"
  ]
}
```

**Writing Reports:**

```bash
cat > .claude/agents/context/${SESSION_ID}/reports/my-agent.json << 'EOF'
{
  "agent_name": "my-agent",
  "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'",
  "status": "completed",
  "summary": "Your summary here",
  "findings": [
    {
      "type": "issue",
      "severity": "high",
      "title": "Finding title",
      "description": "Detailed description",
      "location": "src/file.ts:42",
      "recommendation": "How to fix"
    }
  ],
  "metrics": {
    "items_analyzed": 100,
    "issues_found": 3
  },
  "next_actions": ["Action 1", "Action 2"],
  "recommendations_for_automation": ["Suggestion 1", "Suggestion 2"]
}
EOF
```

**Reading Reports:**

```bash
# Read specific report
cat .claude/agents/context/${SESSION_ID}/reports/security-analyzer.json | jq

# Get summaries from all reports
jq -r '.summary' .claude/agents/context/${SESSION_ID}/reports/*.json

# Get all high-severity findings
jq -s 'map(.findings[]) | map(select(.severity == "high"))' \
  .claude/agents/context/${SESSION_ID}/reports/*.json

# Aggregate metrics
jq -s '{
  total_findings: map(.findings | length) | add,
  high_severity: map(.findings[] | select(.severity == "high")) | length,
  automation_opportunities: map(.recommendations_for_automation) | flatten | length
}' .claude/agents/context/${SESSION_ID}/reports/*.json

# List all data artifacts
jq -s 'map(.data_artifacts) | flatten | unique' \
  .claude/agents/context/${SESSION_ID}/reports/*.json
```

### 4. Data Artifacts (`data/{artifact-name}.json`)

Shared data files for detailed information exchange.

Agents can create data artifacts when:
- Report would be too large
- Other agents need raw data
- Detailed analysis is needed
- Data should be reusable

**Example Artifacts:**

```bash
# Vulnerability details
data/vulnerabilities.json

# Performance profiling results
data/performance-profile.json

# Dependency graph
data/dependency-graph.json

# Test coverage report
data/test-coverage.json

# Code complexity metrics
data/complexity-metrics.json
```

**Creating Artifacts:**

```bash
cat > .claude/agents/context/${SESSION_ID}/data/vulnerabilities.json << 'EOF'
{
  "scan_date": "2025-01-23T10:05:00Z",
  "vulnerabilities": [
    {
      "id": "SQL-001",
      "type": "SQL Injection",
      "severity": "high",
      "file": "src/db/queries.ts",
      "line": 42,
      "code": "db.query(`SELECT * FROM users WHERE id = ${userId}`)",
      "fix": "db.query('SELECT * FROM users WHERE id = ?', [userId])",
      "cwe": "CWE-89",
      "references": ["https://cwe.mitre.org/data/definitions/89.html"]
    }
  ]
}
EOF

# Log artifact creation
echo "{\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"from\":\"security-analyzer\",\"type\":\"data\",\"artifact\":\"data/vulnerabilities.json\",\"description\":\"Detailed vulnerability data\"}" >> \
  .claude/agents/context/${SESSION_ID}/messages.jsonl
```

**Reading Artifacts:**

```bash
# Read artifact
cat .claude/agents/context/${SESSION_ID}/data/vulnerabilities.json | jq

# Find all artifacts
ls .claude/agents/context/${SESSION_ID}/data/

# Check which agents created artifacts
jq 'select(.type == "data") | {from: .from, artifact: .artifact}' \
  .claude/agents/context/${SESSION_ID}/messages.jsonl
```

## Agent Workflows

### Analysis Agent Workflow

```bash
# 1. Check coordination
jq '.agents' .claude/agents/context/${SESSION_ID}/coordination.json

# 2. Read prerequisite reports (if any)
cat .claude/agents/context/${SESSION_ID}/reports/dependency-analyzer.json | jq

# 3. Announce startup
echo "{\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"from\":\"my-analyzer\",\"type\":\"status\",\"message\":\"Starting analysis\"}" >> \
  .claude/agents/context/${SESSION_ID}/messages.jsonl

# 4. Update coordination
# [Update to in_progress as shown above]

# 5. Perform analysis and log progress
echo "{\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"from\":\"my-analyzer\",\"type\":\"status\",\"message\":\"Analyzed 50% of codebase\"}" >> \
  .claude/agents/context/${SESSION_ID}/messages.jsonl

# 6. Write report
# [Create report as shown above]

# 7. Create data artifacts (if needed)
# [Create artifacts as shown above]

# 8. Update coordination to completed
# [Update status as shown above]

# 9. Announce completion
echo "{\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"from\":\"my-analyzer\",\"type\":\"completed\",\"message\":\"Analysis complete. Found X issues.\"}" >> \
  .claude/agents/context/${SESSION_ID}/messages.jsonl
```

### Implementation Agent Workflow

```bash
# 1. Wait for analysis agents
while true; do
  COMPLETED=$(jq -r '.agents | to_entries | map(select(.key | endswith("analyzer")) and .value.status == "completed") | length' \
    .claude/agents/context/${SESSION_ID}/coordination.json)
  TOTAL=$(jq -r '.agents | to_entries | map(select(.key | endswith("analyzer")) | length' \
    .claude/agents/context/${SESSION_ID}/coordination.json)
  if [ "$COMPLETED" -eq "$TOTAL" ]; then
    break
  fi
  sleep 2
done

# 2. Read all analysis reports
for report in .claude/agents/context/${SESSION_ID}/reports/*-analyzer.json; do
  cat "$report" | jq '.summary, .recommendations_for_automation'
done

# 3. Synthesize findings and make decisions
# [Aggregate recommendations, prioritize, decide what to generate]

# 4. Generate artifacts (skills, commands, hooks)
# [Create actual files in .claude/skills/, .claude/commands/, etc.]

# 5. Write report
# [Document what was generated and why]

# 6. Update coordination
# [Mark as completed]
```

### Coordinator Agent Workflow

```bash
# 1. Launch analysis agents in parallel
echo "Launching analysis agents: security, performance, quality, dependency, documentation"

# 2. Monitor progress
watch -n 2 'cat .claude/agents/context/${SESSION_ID}/coordination.json | jq ".agents"'

# 3. Wait for all analysis agents to complete
while true; do
  COMPLETED=$(jq -r '.agents | to_entries | map(select(.key | endswith("analyzer")) and .value.status == "completed") | length' \
    .claude/agents/context/${SESSION_ID}/coordination.json)
  TOTAL=$(jq -r '.agents | to_entries | map(select(.key | endswith("analyzer")) | length' \
    .claude/agents/context/${SESSION_ID}/coordination.json)
  if [ "$COMPLETED" -eq "$TOTAL" ]; then
    break
  fi
  sleep 5
done

# 4. Synthesize all findings
jq -s '{
  total_findings: map(.findings | length) | add,
  high_severity: map(.findings[] | select(.severity == "high")) | length,
  automation_suggestions: map(.recommendations_for_automation) | flatten
}' .claude/agents/context/${SESSION_ID}/reports/*-analyzer.json

# 5. Make decisions on what to generate
# [Based on synthesis, decide which skills/commands/hooks/MCP to create]

# 6. Launch implementation agents in parallel
echo "Launching implementation agents: skill-gen, command-gen, hook-gen, mcp-config"

# 7. Monitor implementation
# [Similar monitoring loop]

# 8. Launch validation agents sequentially
echo "Launching integration-tester"
# [Wait for completion]
echo "Launching documentation-validator"

# 9. Generate final documentation
# [Create AUTOMATION_README.md, QUICK_REFERENCE.md]

# 10. Report to user
# [Summarize what was created and how to use it]
```

## Error Handling

### Detecting Failures

```bash
# Check for failed agents
jq '.agents | to_entries | map(select(.value.status == "failed"))' \
  .claude/agents/context/${SESSION_ID}/coordination.json

# Find error events
jq 'select(.type == "error")' .claude/agents/context/${SESSION_ID}/messages.jsonl
```

### Recovery Strategies

1. **Retry Agent** - Re-run the failed agent
2. **Continue Without** - Proceed if agent was non-critical
3. **Manual Intervention** - Fix issue and resume
4. **Partial Results** - Check if agent wrote partial report

### Logging Errors

```bash
# Log error with details
echo "{\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"from\":\"my-agent\",\"type\":\"error\",\"message\":\"Failed to analyze X\",\"error\":\"Error details here\"}" >> \
  .claude/agents/context/${SESSION_ID}/messages.jsonl

# Update coordination
cat .claude/agents/context/${SESSION_ID}/coordination.json | \
  jq '.agents["my-agent"].status = "failed" |
      .agents["my-agent"].error = "Error details"' > /tmp/coord.json && \
  mv /tmp/coord.json .claude/agents/context/${SESSION_ID}/coordination.json
```

## Best Practices

### For Agents

1. **Check dependencies first** - Read coordination before starting
2. **Log frequently** - Write to message bus for transparency
3. **Standardize reports** - Follow the exact JSON format
4. **Be atomic** - Complete write-then-move for files
5. **Handle errors gracefully** - Log errors, update status
6. **Provide actionable output** - Clear recommendations
7. **Suggest automation** - Think about reusable patterns

### For Coordinators

1. **Launch in parallel when possible** - Maximize concurrency
2. **Respect dependencies** - Don't start agents before prerequisites
3. **Monitor actively** - Check coordination periodically
4. **Synthesize thoroughly** - Read all reports before decisions
5. **Validate results** - Test generated automation
6. **Document completely** - Explain what was created and why

### For File Operations

1. **Append-only for logs** - Use `>>` for messages.jsonl
2. **Replace-whole for state** - Use write-to-temp-then-move for coordination.json
3. **Unique names** - Avoid conflicts in data artifacts
4. **JSON formatting** - Always use valid JSON
5. **Timestamps** - ISO 8601 format (UTC)

## Example Session

Full example of 3 agents communicating:

```bash
# Session starts
SESSION_ID="abc123"
mkdir -p ".claude/agents/context/${SESSION_ID}"/{reports,data}

# Agent 1: Security Analyzer starts
echo "{\"timestamp\":\"2025-01-23T10:00:00Z\",\"from\":\"security\",\"type\":\"status\",\"message\":\"Starting\"}" >> \
  .claude/agents/context/${SESSION_ID}/messages.jsonl

# Agent 2: Performance Analyzer starts (parallel)
echo "{\"timestamp\":\"2025-01-23T10:00:01Z\",\"from\":\"performance\",\"type\":\"status\",\"message\":\"Starting\"}" >> \
  .claude/agents/context/${SESSION_ID}/messages.jsonl

# Security finds issue
echo "{\"timestamp\":\"2025-01-23T10:02:00Z\",\"from\":\"security\",\"type\":\"finding\",\"severity\":\"high\",\"data\":{\"title\":\"SQL Injection\"}}" >> \
  .claude/agents/context/${SESSION_ID}/messages.jsonl

# Security completes
echo "{\"timestamp\":\"2025-01-23T10:05:00Z\",\"from\":\"security\",\"type\":\"completed\",\"message\":\"Found 5 issues\"}" >> \
  .claude/agents/context/${SESSION_ID}/messages.jsonl
# Creates report: reports/security.json

# Performance completes
echo "{\"timestamp\":\"2025-01-23T10:06:00Z\",\"from\":\"performance\",\"type\":\"completed\",\"message\":\"Found 3 bottlenecks\"}" >> \
  .claude/agents/context/${SESSION_ID}/messages.jsonl
# Creates report: reports/performance.json

# Coordinator reads both reports
cat .claude/agents/context/${SESSION_ID}/reports/security.json | jq .summary
cat .claude/agents/context/${SESSION_ID}/reports/performance.json | jq .summary

# Coordinator launches implementation agent
echo "{\"timestamp\":\"2025-01-23T10:07:00Z\",\"from\":\"coordinator\",\"type\":\"status\",\"message\":\"Launching skill generator\"}" >> \
  .claude/agents/context/${SESSION_ID}/messages.jsonl

# Skill generator reads analysis reports
jq -s 'map(.recommendations_for_automation) | flatten' \
  .claude/agents/context/${SESSION_ID}/reports/*.json

# Skill generator creates artifacts
# [Generates skills based on recommendations]

# Complete
echo "{\"timestamp\":\"2025-01-23T10:10:00Z\",\"from\":\"coordinator\",\"type\":\"completed\",\"message\":\"Automation system ready\"}" >> \
  .claude/agents/context/${SESSION_ID}/messages.jsonl
```

## Protocol Guarantees

### What ACP Guarantees

✅ **Visibility** - All agents can see all reports
✅ **Ordering** - Events have timestamps
✅ **Persistence** - Survives crashes
✅ **Transparency** - Complete audit trail
✅ **Atomicity** - No partial writes (when using temp files)

### What ACP Does NOT Guarantee

❌ **Real-time coordination** - File-based, not instant
❌ **Locking** - No distributed locks (use temp files + move)
❌ **Transactions** - No multi-file atomicity
❌ **Ordering of concurrent writes** - Append-only log doesn't guarantee order

## Summary

The Agent Communication Protocol provides a simple, robust way for parallel subagents to:

1. **Coordinate** - Via coordination.json
2. **Communicate findings** - Via standardized reports
3. **Share data** - Via data artifacts
4. **Maintain transparency** - Via message bus
5. **Enable orchestration** - Via dependency tracking

All communication is file-based, making it:
- Easy to implement
- Easy to debug
- Easy to monitor
- Reliable and persistent
- Language-agnostic

This protocol enables the meta-skill to generate sophisticated multi-agent automation systems that work reliably in parallel.
