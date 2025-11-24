---
name: meta-rollback
description: Rollback/undo automation changes made by meta-automation-architect
---

# Rollback Meta-Automation Changes

You want to undo automation changes. Let me help you safely rollback.

## Instructions

1. **Check for backups** in `.claude/meta-automation/backups/`
2. **Show what would be rolled back** using `rollback_manager.py`
3. **Ask for confirmation** before actually rolling back
4. **Execute rollback** if confirmed

## Steps

### 1. Preview Rollback
Use the RollbackManager to preview:
- Files that will be restored to previous versions
- Files that will be deleted (created by automation)
- Total changes that will be undone

### 2. Confirm with User
Show the preview and ask: "Do you want to proceed with this rollback? [y/n]"

### 3. Execute if Confirmed
If yes:
- Restore backed-up files
- Delete created files
- Update manifest to mark rollback as complete
- Show summary of what was rolled back

### 4. Verify
After rollback:
- Check that files were restored correctly
- Confirm no automation artifacts remain
- Show final status

## Safety Notes
- Rollback can only be done ONCE per backup
- Make sure to commit any important work before rollback
- Cannot rollback if changes have been modified since automation

Please walk me through this process step by step.
