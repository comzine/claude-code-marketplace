---
name: meta-metrics
description: Show ROI, time saved, and effectiveness metrics for meta-automation
---

# Meta-Automation Metrics Report

Please generate a comprehensive metrics report showing the value of automation.

## Instructions

1. **Load metrics** from `.claude/meta-automation/metrics/` if they exist
2. **Calculate ROI** using the metrics_tracker.py script
3. **Show effectiveness** - which automation is actually used vs generated

## Report Should Include

### Time Metrics
- Setup time spent
- Estimated time savings
- Actual time savings (tracked)
- Accuracy (actual vs estimated)
- Net gain in hours

### ROI Metrics
- Return on investment ratio
- Break-even status
- Cost spent vs value gained

### Usage Metrics
- Skills/commands generated
- Skills/commands actually used
- Most frequently used automation
- Unused automation (candidates for removal)

### Value Delivered
- Issues prevented
- Quality improvements
- User satisfaction ratings

If no metrics exist yet, explain how to start tracking metrics using the meta-automation-architect system.

Present this as a clear, actionable report with specific numbers.
