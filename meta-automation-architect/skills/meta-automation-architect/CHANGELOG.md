# Changelog

## [2.0.0] - 2025-11-23 - Major Architecture Overhaul

### 🚀 Major Changes

**Agent-Based Detection (vs Python Pattern Matching)**
- Replaced 727-line `detect_project.py` Python script with intelligent `project-analyzer` agent
- Agent reads key files, understands context, and asks clarifying questions
- More accurate, context-aware project understanding

**Interactive Workflow**
- Added mode selection: Quick (⚡ $0.03, 10 min) → Focused (🔧 $0.10, 20 min) → Comprehensive (🏗️ $0.15, 30 min)
- No more guessing - system asks questions with recommendations
- Simple mode first for new users

**Template-Based Generation**
- Replaced Python string building with `.template` files using `{{variable}}` syntax
- Easier to customize and maintain
- Cleaner separation of structure from logic

**Tool Discovery**
- Automatically detects existing automation (linting, testing, CI/CD, git hooks, etc.)
- Prevents duplication and integration conflicts
- Recommends: fill gaps, enhance existing, or create independent

**Cost Transparency**
- Shows token estimates, time estimates, and costs BEFORE execution
- No surprises - users see exactly what they're getting

### 🎯 New Features

**User Preference Learning** (`scripts/user_preferences.py`)
- Tracks mode preferences, agent usage, satisfaction ratings
- Provides personalized recommendations based on history
- Calculates ROI: actual time saved / setup time

**Metrics Tracking** (`scripts/metrics_tracker.py`)
- Records ACTUAL time saved (not just estimates)
- Tracks effectiveness: which automation is actually used
- Proves value with real data

**Rollback Capability** (`scripts/rollback_manager.py`)
- Creates automatic backups before making changes
- Manifest-based tracking of all changes
- One-command rollback to pre-automation state

**Configuration Reuse** (`scripts/agent_reuse.py`)
- Saves successful automation configurations
- Finds similar projects using similarity matching
- Recommends reuse to save 5-10 minutes

### 📁 New Scripts

- `scripts/collect_project_metrics.py` - Simple metrics collection (150 lines vs 586)
- `scripts/template_renderer.py` - Template rendering engine
- `scripts/discover_existing_tools.py` - Existing automation detection
- `scripts/cost_estimator.py` - Cost/time estimation
- `scripts/user_preferences.py` - User learning and recommendations
- `scripts/metrics_tracker.py` - Real usage tracking
- `scripts/rollback_manager.py` - Backup and restore
- `scripts/agent_reuse.py` - Configuration reuse

### 📝 New Templates

- `templates/agent-base.md.template` - Base template for agents
- `templates/skill-base.md.template` - Base template for skills
- `templates/command-base.md.template` - Base template for commands
- `templates/project-analyzer.md` - Intelligent project analyzer agent

### 🗑️ Removed

**Obsolete Code:**
- ❌ `scripts/detect_project.py` (727 lines) - Replaced by agent-based detection

**Test Data:**
- ❌ `.claude/meta-automation/` directories with test runs

**Obsolete Documentation:**
- ❌ `IMPROVEMENT_ROADMAP.md`
- ❌ `PHASE1_IMPLEMENTATION.md`
- ❌ `PHASE2_IMPLEMENTATION.md`
- ❌ `PHASE3_IMPLEMENTATION.md`
- ❌ `IMPLEMENTATION_COMPLETE.md`
- ❌ `UNIVERSAL_UPGRADE.md`
- ❌ `DOCUMENT_FORMATS_EXPANSION.md`

**Old Templates:**
- ❌ `templates/example-skill-template.md`
- ❌ `templates/example-command-template.md`
- ❌ `templates/example-hook-template.py`

### 📊 Impact

- **Lines Removed:** ~3,500 lines
- **Files Removed:** ~18 files
- **Code Quality:** Production-ready, maintainable structure
- **User Experience:** Interactive, transparent, learns from usage
- **Efficiency:** Simple mode first, progressive enhancement

### 🔄 Migration Notes

**Breaking Changes:**
- `detect_project.py` removed - use `project-analyzer` agent instead
- Old template format `{variable}` replaced with `{{variable}}`

**New Workflow:**
1. Skill asks: Quick, Focused, or Comprehensive?
2. Collects project metrics
3. Launches project-analyzer agent
4. Agent analyzes and asks questions
5. Discovers existing tools
6. Shows cost/time estimates
7. Generates automation
8. Tracks usage and learns

---

## [1.0.0] - Initial Release

- Universal project detection (8 project types)
- 37 specialized agents
- Skill, command, and hook generation
- Coordinator architecture
- Communication protocol
