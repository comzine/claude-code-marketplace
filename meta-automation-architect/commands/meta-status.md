---
name: meta-status
description: Show what automation exists in current project and what meta-automation has generated
---

# Automation Status Check

Please check and report on:

## 1. Existing Automation
Use `discover_existing_tools.py` to find:
- Linting tools (ESLint, Pylint, etc.)
- Testing frameworks (Jest, pytest, etc.)
- CI/CD pipelines (.github/workflows, .gitlab-ci.yml, etc.)
- Git hooks (pre-commit, pre-push, etc.)
- Formatters (Prettier, Black, etc.)
- Security scanners
- Documentation generators

## 2. Meta-Automation Generated
Check `.claude/agents/`, `.claude/skills/`, `.claude/commands/` for:
- Custom agents generated
- Custom skills generated
- Custom commands generated
- Hooks installed

## 3. Summary
Provide a clear summary of:
- What automation is already present
- What meta-automation has generated
- Gaps or opportunities for additional automation

Present this information in a clean, organized format.
