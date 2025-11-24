# Example: Project Management Automation

This example shows what the meta-automation-architect generates for a software delivery project management workspace.

## Project Context

- **Type**: Project Management (primary) + Programming (secondary)
- **Project**: Q1 2025 Mobile App Development
- **Team**: 8 people (2 devs, 2 designers, 1 PM, 1 QA, 2 stakeholders)
- **Duration**: 3 months (12 sprints)
- **Pain Points**: Manual status reporting, resource over-allocation, missing risk tracking
- **Priority**: Automated reporting and resource management

## Project Structure

```
mobile-app-project/
├── project-plan.md
├── roadmap.md
├── sprints/
│   ├── sprint-01/
│   │   ├── planning.md
│   │   ├── tasks.md
│   │   ├── retrospective.md
│   │   └── burndown-chart.png
│   ├── sprint-02/
│   └── ... (12 sprints)
├── resources/
│   ├── team-capacity.md
│   ├── allocation.xlsx
│   └── skills-matrix.md
├── risks/
│   ├── risk-register.md
│   └── mitigation-plans.md
├── milestones/
│   ├── m1-design-complete.md
│   ├── m2-mvp-ready.md
│   └── m3-launch-ready.md
└── reports/
    ├── weekly-status/
    └── monthly-summary/
```

## User Conversation

```
User: "Set up automation for my mobile app project management"

Meta-Skill: Analyzing project...
- Detected: Project Management (78% confidence)
  - Found sprints/ directory with 12 sprint folders
  - Found project-plan.md and roadmap.md
  - Found resources/allocation.xlsx
  - Found risks/risk-register.md
- Secondary: Programming (22% confidence)
  - References to code deliverables

Meta-Skill: What are your main pain points?
Options:
- Manual status reporting (RECOMMENDED: 12 weekly reports expected, only 3 exist)
- Resource over-allocation (RECOMMENDED: Excel shows conflicts)
- Missing risk tracking
- Timeline validation

User: [Selects: Manual status reporting, Resource over-allocation]

Meta-Skill: Generating automation system...
Session ID: pm-mobile-app-xyz789
```

## Generated Automation System

### 1. Custom Subagents (6)

#### Universal Agents
- **structure-analyzer** - Project organization and folder hierarchy
- **workflow-analyzer** - Sprint and delivery processes

#### Project Management Domain Agents
- **timeline-analyzer** - Sprint schedules, dependencies, critical paths
- **resource-analyzer** - Team allocation, capacity, conflicts
- **risk-analyzer** - Risk identification and mitigation coverage

#### Implementation Agent
- **command-generator** - Created 3 PM-specific commands

### 2. Custom Skills (3)

**`status-reporter`** - Auto-generates weekly status reports from sprint data
- Reads sprint tasks, completion status, blockers
- Generates formatted report with metrics
- Saves time: **45 min/week** (9 hours over 12 sprints)

**`resource-optimizer`** - Identifies and resolves allocation conflicts
- Parses resource allocation data
- Detects over/under allocation
- Suggests rebalancing
- Saves time: **30 min/sprint** (6 hours total)

**`risk-tracker`** - Maintains risk register and tracks mitigation
- Monitors risks from register
- Tracks mitigation progress
- Alerts on new risks
- Saves time: **20 min/week** (4 hours total)

### 3. Custom Commands (3)

**`/sprint-report`**
```bash
/sprint-report                # Current sprint
/sprint-report sprint-05      # Specific sprint
/sprint-report --all          # All sprints summary
```

Generates comprehensive sprint report:
- Completed tasks vs. planned
- Velocity and burndown
- Blockers and risks
- Team capacity utilization
- Next sprint forecast

**`/resource-check`**
```bash
/resource-check               # Check current allocation
/resource-check --week 5      # Specific week
/resource-check --conflicts   # Show only conflicts
```

Analyzes resource allocation:
- Capacity vs. assigned work
- Over-allocated team members
- Under-utilized resources
- Skill match for tasks
- Rebalancing suggestions

**`/timeline-validate`**
```bash
/timeline-validate            # Validate full timeline
/timeline-validate --critical # Show critical path
/timeline-validate --risks    # Timeline risks
```

Validates project timeline:
- Dependency validation
- Critical path analysis
- Buffer analysis
- Risk to deadlines
- Suggested adjustments

### 4. Hooks (2)

**`update_progress.py`** (PostToolUse)
- Triggers when task markdown files are updated
- Extracts completion status
- Updates sprint progress automatically
- Regenerates burndown chart

**`resource_validation.py`** (PreToolUse)
- Triggers when allocation files are modified
- Validates no over-allocation
- Blocks if conflicts detected
- Suggests fixes before allowing change

### 5. Documentation

**Impact Assessment:**

**Time Savings:**
- Weekly status reports: 45 min/week × 12 weeks = **9 hours**
- Resource planning: 30 min/sprint × 12 sprints = **6 hours**
- Risk tracking: 20 min/week × 12 weeks = **4 hours**
- Timeline validation: 1 hour/month × 3 months = **3 hours**
- **Total: 22 hours saved**

**Quality Improvements:**
- **100% sprint coverage** for status reports (up from 25%)
- **Zero resource conflicts** (automated detection)
- **Real-time risk visibility** (vs. monthly reviews)
- **Validated timeline** with critical path analysis

## Example Usage

### Generating Sprint Report

```bash
/sprint-report sprint-05
```

**Output:**
```markdown
# Sprint 05 Report
**Period:** Jan 15-19, 2025
**Team:** Mobile App Team

## Summary
✅ Sprint Goal: Complete user authentication flow - ACHIEVED

## Metrics
- **Planned Story Points:** 34
- **Completed Story Points:** 32 (94%)
- **Velocity:** 32 pts (trending up from 28)
- **Team Capacity:** 160 hours
- **Actual Hours:** 152 hours (95% utilization)

## Completed Tasks (8)
✅ User login UI (8 pts) - @designer1
✅ OAuth integration (13 pts) - @dev1
✅ Session management (5 pts) - @dev2
✅ Login testing (3 pts) - @qa
[... 4 more ...]

## Carried Over (2)
➡️  Password reset flow (5 pts) - blocked by API
➡️  Biometric auth (8 pts) - iOS issue

## Blockers
⚠️  API authentication endpoint delayed → unblocks next sprint
⚠️  iOS biometric API documentation unclear → dev investigating

## Risks
🔴 HIGH: OAuth provider latency affecting UX → mitigation: add loading states
🟡 MEDIUM: Test coverage only 65% → action: dedicated testing time in sprint 06

## Team Notes
- Great collaboration between design and dev
- Need more QA capacity in next sprint
- Consider adding API buffer time

## Next Sprint Preview
Sprint 06 will focus on:
- Complete password reset (carried over)
- User profile management
- Settings screen
- Target: 30-35 story points

---
Auto-generated by meta-automation-architect
```

### Checking Resource Allocation

```bash
/resource-check
```

**Output:**
```
📊 Resource Allocation Analysis

Current Week: Week 6 (Jan 22-26, 2025)

✅ Properly Allocated (5):
- @dev1: 40/40 hours (100%)
- @designer2: 32/40 hours (80%)
- @qa: 40/40 hours (100%)
- @pm: 35/40 hours (88%)
- @stakeholder1: 10/10 hours (100%)

⚠️  Over-Allocated (2):
- @dev2: 52/40 hours (130% - CRITICAL)
  Tasks: Feature A (20h), Feature B (18h), Bug fixes (14h)
  Recommendation: Move Bug fixes to @dev1 (8h available)

- @designer1: 45/40 hours (113%)
  Tasks: UI mockups (25h), Asset creation (20h)
  Recommendation: Defer Asset creation to Week 7

🔵 Under-Utilized (1):
- @stakeholder2: 3/10 hours (30%)
  Opportunity: Review sessions, feedback collection

💡 Optimization Suggestions:
1. Redistribute 14h from @dev2 to @dev1
2. Move Asset creation from @designer1 to Week 7
3. Add review tasks for @stakeholder2

Estimated Rebalancing Time: 10 minutes
After optimization: 100% feasible allocation
```

## Agent Communication

**`reports/timeline-analyzer.json`** (excerpt):
```json
{
  "agent_name": "timeline-analyzer",
  "summary": "Timeline feasible but tight. Critical path includes 4 sprints with zero buffer.",
  "findings": [
    {
      "type": "risk",
      "severity": "high",
      "title": "Zero Buffer on Critical Path",
      "description": "Sprints 4, 7, 9, 11 are on critical path with no schedule buffer",
      "recommendation": "Add 10% buffer to each critical sprint or reduce scope",
      "time_impact": "Any delay in these sprints directly impacts launch date"
    },
    {
      "type": "opportunity",
      "severity": "medium",
      "title": "Parallel Workstreams Possible",
      "description": "Design and backend development can run in parallel in sprints 2-5",
      "recommendation": "Optimize resource allocation to leverage parallelism",
      "time_saved_if_optimized": "2 weeks off critical path"
    }
  ],
  "automation_impact": {
    "time_saved": "3 hours per month in timeline reviews",
    "quality_improvement": "Real-time critical path visibility vs. monthly checks"
  }
}
```

## Result

**PM now has powerful automation:**
- ✅ Weekly status reports generated in 30 seconds (vs. 45 minutes)
- ✅ Resource conflicts detected instantly (vs. discovered in standup)
- ✅ Risk register automatically maintained
- ✅ Timeline validated continuously
- ✅ **22 hours saved** over project duration
- ✅ **Better decision making** with real-time data

**Before vs After:**

**Before (Manual):**
- Weekly status report: 45 min
- Resource planning: 30 min/sprint
- Risk review: 20 min/week
- Timeline validation: 1 hour/month
- **Total: ~3 hours/week**

**After (Automated):**
- Status report: `/sprint-report` → 30 seconds
- Resource check: `/resource-check` → 30 seconds
- Risk tracking: Auto-updated from tasks
- Timeline: Auto-validated on every change
- **Total: ~5 minutes/week**

**Impact: 97% time reduction + higher data quality!**
