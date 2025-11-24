# Example: Educational Course Automation

This example shows what the meta-automation-architect generates for an online programming course project.

## Project Context

- **Type**: Educational (primary) + Programming (secondary)
- **Content**: "Learn Python Programming" online course
- **Structure**: 12 modules, 48 lessons, exercises and quizzes
- **Pain Points**: Incomplete assessments, inconsistent formatting, manual progress tracking
- **Priority**: Assessment coverage and content consistency

## User Conversation

```
User: "Set up automation for my Python programming course"

Meta-Skill: Analyzing project...
- Detected: Educational (72% confidence)
  - Found lessons/ directory with 48 markdown files
  - Found quizzes/ with 8 assessment files
  - Found exercises/ with 32 exercise files
  - Sequential numbering detected (01_intro.md, 02_variables.md)
- Secondary: Programming (28% confidence)
  - Found Python code examples in lessons
  - Found exercise solutions in .py files

Meta-Skill: What are your main pain points?
Options:
- Incomplete assessment coverage (RECOMMENDED: 8 quizzes for 48 lessons = 17% coverage)
- Inconsistent lesson formatting
- Manual progress tracking
- Missing prerequisites validation

User: [Selects: Incomplete assessment coverage, Inconsistent formatting]

Meta-Skill: How many agents should we create?
- Few (2-3): Basic analysis
- Moderate (4-6): Multi-domain coverage (RECOMMENDED)
- Many (7+): Comprehensive automation

User: [Selects: Moderate]

Meta-Skill: Generating automation system...
Session ID: ed-course-abc123
```

## Project Structure

```
python-course/
├── modules/
│   ├── 01-introduction/
│   │   ├── 01_what-is-python.md
│   │   ├── 02_setup-environment.md
│   │   ├── 03_first-program.md
│   │   └── 04_variables.md
│   ├── 02-data-types/
│   └── ... (10 more modules)
├── quizzes/
│   ├── module-01-quiz.md
│   └── ... (7 more quizzes)
├── exercises/
│   ├── 01_hello_world.py
│   ├── 02_variables_practice.py
│   └── ... (30 more exercises)
├── solutions/
│   └── ... (exercise solutions)
├── syllabus.md
└── README.md
```

## Generated Automation System

### 1. Custom Subagents (6)

All agents created in `.claude/agents/`:

#### Universal Analysis Agents

**structure-analyzer.md**
- Analyzes course directory organization
- Checks module/lesson hierarchy
- Validates naming conventions
- Ensures consistent structure

**workflow-analyzer.md**
- Identifies repetitive content creation patterns
- Finds bottlenecks in course development
- Maps content creation workflow
- Suggests automation opportunities

#### Educational Domain Agents

**learning-path-analyzer.md**
- Maps lesson dependencies and prerequisites
- Analyzes difficulty progression curve
- Validates learning objective coverage
- Checks skill development sequence

**assessment-analyzer.md**
- Maps quizzes to modules (found only 17% coverage!)
- Analyzes quiz difficulty distribution
- Checks learning objective alignment
- Reviews question quality and variety

#### Implementation Agents

**skill-generator.md**
- Creates custom skills for course automation
- Generated: `quiz-generator`, `lesson-formatter`, `prerequisite-validator`

**command-generator.md**
- Creates commands for common workflows
- Generated: `/generate-quiz`, `/check-progression`, `/export-course`

### 2. Custom Skills (3)

**`.claude/skills/quiz-generator/SKILL.md`**
```markdown
---
name: quiz-generator
description: Automatically generates quiz questions from lesson content
allowed-tools: ["Read", "Write", "Grep", "Glob"]
---

# Quiz Generator

Automatically generates comprehensive quiz questions from lesson content.

## When This Activates

- User requests "generate quiz for module X"
- User says "create assessment for lessons"
- User asks "add quiz questions"

## Process

1. **Read Lesson Content**
   - Parse lesson markdown files
   - Extract key concepts and terms
   - Identify code examples
   - Note learning objectives

2. **Generate Question Types**
   - Multiple choice (concept understanding)
   - Fill-in-the-blank (terminology)
   - Code completion (practical skills)
   - True/false (misconception checking)
   - Short answer (deeper understanding)

3. **Create Quiz File**
   - Standard format with frontmatter
   - Varied question types
   - Progressive difficulty
   - Aligned with learning objectives

4. **Validate Quality**
   - Check question clarity
   - Ensure correct answers
   - Verify difficulty appropriateness
   - Test completeness

## Example

**Input Lesson** (02_variables.md):
```markdown
# Variables in Python

Variables are containers for storing data values. In Python, you don't need to declare a variable type.

```python
x = 5
name = "Alice"
```

Variables can change type:
```python
x = 5       # int
x = "text"  # now string
```
```

**Generated Quiz** (module-01-quiz.md):
```markdown
---
module: 1
lessons_covered: [1, 2, 3, 4]
difficulty: beginner
time_estimate: 10 minutes
---

# Module 1 Quiz: Introduction to Python

## Question 1 (Multiple Choice)
What is a variable in Python?
a) A fixed value that cannot change
b) A container for storing data values
c) A type of function
d) A Python keyword

**Answer:** b

## Question 2 (Fill in the Blank)
In Python, you _____ need to declare a variable's type explicitly.
**Answer:** don't / do not

## Question 3 (Code Completion)
Complete this code to create a variable named `age` with value 25:
```python
___ = ___
```
**Answer:** age = 25

## Question 4 (True/False)
A Python variable can change its type during program execution.
**Answer:** True

## Question 5 (Short Answer)
Explain in one sentence why Python is considered "dynamically typed".
**Sample Answer:** Python determines variable types at runtime rather than requiring explicit type declarations.
```

[... full skill implementation ...]
```

**`.claude/skills/lesson-formatter/SKILL.md`**
```markdown
---
name: lesson-formatter
description: Enforces consistent lesson structure and formatting across all course content
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob"]
---

# Lesson Formatter

Automatically formats lessons to maintain consistency across the course.

## Standard Lesson Format

Every lesson should have:

1. **Frontmatter** (metadata)
2. **Title** (# heading)
3. **Learning Objectives** (bullet list)
4. **Prerequisites** (if any)
5. **Content Sections** (## headings)
6. **Code Examples** (with syntax highlighting)
7. **Key Takeaways** (bullet list)
8. **Practice Exercise** (link)
9. **Next Lesson** (link)

## Process

1. **Scan Lesson**
   - Check for required sections
   - Validate frontmatter
   - Verify code block formatting

2. **Add Missing Sections**
   - Generate learning objectives from content
   - Add takeaways summary
   - Create exercise links

3. **Format Consistently**
   - Standardize heading levels
   - Fix code block languages
   - Normalize spacing

4. **Validate Links**
   - Check prerequisite links
   - Verify exercise references
   - Validate next lesson

## Example Transformation

**Before:**
```markdown
# Variables

Let's learn about variables.

x = 5

That's a variable.
```

**After:**
```markdown
---
module: 1
lesson: 4
title: Variables in Python
duration: 15 minutes
difficulty: beginner
prerequisites: [03_first-program]
---

# Variables in Python

## Learning Objectives

By the end of this lesson, you will be able to:
- Define what a variable is in Python
- Create variables with different data types
- Understand Python's dynamic typing
- Follow variable naming conventions

## Prerequisites

- Completed: [First Python Program](03_first-program.md)

## What are Variables?

Variables are containers for storing data values. In Python, you don't need to declare a variable type explicitly.

## Creating Variables

```python
x = 5
name = "Alice"
is_student = True
```

## Dynamic Typing

Python is dynamically typed, meaning variables can change type:

```python
x = 5       # int
x = "text"  # now string (valid in Python!)
```

## Key Takeaways

- Variables store data values
- No type declaration needed
- Can change type during execution
- Use descriptive names

## Practice

Complete [Exercise 02: Variables Practice](../../exercises/02_variables_practice.py)

## Next

Continue to [Data Types](../02-data-types/01_numbers.md)
```

[... full skill implementation ...]
```

**`.claude/skills/prerequisite-validator/SKILL.md`**
```markdown
---
name: prerequisite-validator
description: Validates that lesson prerequisites form a valid learning path
allowed-tools: ["Read", "Grep", "Glob"]
---

# Prerequisite Validator

Ensures lessons have valid prerequisites and creates a coherent learning path.

## What It Checks

1. **Prerequisite Existence**
   - Referenced lessons exist
   - Paths are correct

2. **No Circular Dependencies**
   - Lesson A → B → A is invalid
   - Detects cycles in prerequisite graph

3. **Logical Progression**
   - Prerequisites come before lesson
   - Difficulty increases appropriately

4. **Completeness**
   - All lessons reachable from start
   - No orphaned lessons

## Process

1. **Parse Prerequisites**
   ```python
   # Extract from frontmatter
   prerequisites: [01_intro, 02_variables]
   ```

2. **Build Dependency Graph**
   ```
   01_intro
     ├─ 02_variables
     │   ├─ 03_data_types
     │   └─ 04_operators
     └─ 05_strings
   ```

3. **Validate**
   - Check cycles
   - Verify order
   - Find orphans

4. **Generate Report**
   - Issues found
   - Suggested fixes
   - Visualization of learning path

## Example Output

```
✅ Prerequisite Validation Complete

📊 Learning Path Statistics:
- Total lessons: 48
- Entry points: 1 (01_what-is-python)
- Maximum depth: 6 levels
- Average prerequisites per lesson: 1.4

❌ Issues Found: 3

1. Circular dependency detected:
   15_functions → 16_scope → 17_recursion → 15_functions

   Recommendation: Remove prerequisite from 17_recursion

2. Orphaned lesson:
   advanced/99_metaprogramming.md
   No lesson links to this. Add to module 12.

3. Missing prerequisite:
   Lesson 23_list_comprehensions uses concepts from 20_loops
   but doesn't list it as prerequisite.

   Recommendation: Add 20_loops to prerequisites

📈 Learning Path Diagram saved to: docs/learning-path.mmd
```

[... full skill implementation ...]
```

### 3. Custom Commands (3)

**`.claude/commands/generate-quiz.md`**
```markdown
---
description: Generate quiz for a module or lesson
allowed-tools: ["Read", "Write", "Grep", "Glob"]
---

# Generate Quiz

Creates comprehensive quiz from lesson content.

## Usage

```bash
/generate-quiz module-01          # Generate quiz for module 1
/generate-quiz 15_functions       # Generate quiz for specific lesson
/generate-quiz --all              # Generate missing quizzes for all modules
```

## What It Does

1. Reads lesson content from specified module/lesson
2. Extracts key concepts and learning objectives
3. Generates varied question types
4. Creates quiz file in standard format
5. Updates quiz index

## Example

```bash
/generate-quiz module-02
```

Output:
```
📝 Generating quiz for Module 02: Data Types...

✅ Analyzed 4 lessons:
   - 05_numbers.md
   - 06_strings.md
   - 07_lists.md
   - 08_dictionaries.md

✅ Generated 15 questions:
   - 6 multiple choice
   - 3 fill-in-blank
   - 4 code completion
   - 2 short answer

✅ Quiz saved to: quizzes/module-02-quiz.md

📊 Estimated completion time: 12 minutes
💡 Difficulty: Beginner

Next: Review and adjust questions in quizzes/module-02-quiz.md
```

[... full command implementation ...]
```

**`.claude/commands/check-progression.md`**
```markdown
---
description: Check learning path and prerequisite validity
allowed-tools: ["Read", "Grep", "Glob"]
---

# Check Progression

Validates course structure and learning path.

## Usage

```bash
/check-progression                    # Full validation
/check-progression --module 3         # Check specific module
/check-progression --visual           # Generate visual diagram
```

## Checks Performed

1. **Structure Validation**
   - All modules present
   - Lessons numbered correctly
   - No gaps in sequence

2. **Prerequisite Validation**
   - No circular dependencies
   - Prerequisites exist
   - Logical progression

3. **Assessment Coverage**
   - Quiz per module
   - Exercises per lesson
   - Coverage percentage

4. **Content Consistency**
   - Standard lesson format
   - Required sections present
   - Code examples formatted

[... full command implementation ...]
```

**`.claude/commands/export-course.md`**
```markdown
---
description: Export course to various formats (PDF, HTML, SCORM)
allowed-tools: ["Read", "Bash", "Write", "Glob"]
---

# Export Course

Exports course content to distributable formats.

## Usage

```bash
/export-course pdf                    # Export to PDF
/export-course html                   # Export to static website
/export-course scorm                  # Export to SCORM package
/export-course --module 3 pdf         # Export specific module
```

[... full command implementation ...]
```

### 4. Hooks (1)

**`.claude/hooks/validate_lesson_format.py`**
```python
#!/usr/bin/env python3
"""
Lesson Format Validation Hook
Type: PostToolUse
Validates lesson format after editing
"""

import sys
import json
import re
from pathlib import Path

def main():
    context = json.load(sys.stdin)
    tool = context.get('tool')
    params = context.get('parameters', {})

    # Only trigger on Write/Edit to lesson files
    if tool not in ['Write', 'Edit']:
        sys.exit(0)

    file_path = params.get('file_path', '')
    if '/lessons/' not in file_path or not file_path.endswith('.md'):
        sys.exit(0)

    print(f"📋 Validating lesson format: {Path(file_path).name}", file=sys.stderr)

    try:
        with open(file_path) as f:
            content = f.read()

        issues = []

        # Check frontmatter
        if not content.startswith('---'):
            issues.append("Missing frontmatter")

        # Check required sections
        required_sections = [
            '# ',  # Title
            '## Learning Objectives',
            '## Key Takeaways'
        ]

        for section in required_sections:
            if section not in content:
                issues.append(f"Missing section: {section}")

        # Check code blocks have language
        code_blocks = re.findall(r'```(\w*)', content)
        if any(lang == '' for lang in code_blocks):
            issues.append("Code blocks missing language specification")

        # Check for exercise link
        if '../../exercises/' not in content and '/exercises/' not in content:
            issues.append("Missing practice exercise link")

        if issues:
            print(f"⚠️  Format issues found:", file=sys.stderr)
            for issue in issues:
                print(f"   - {issue}", file=sys.stderr)
            print(f"\n💡 Tip: Use the lesson-formatter skill to auto-fix", file=sys.stderr)
        else:
            print(f"✅ Lesson format valid", file=sys.stderr)

    except Exception as e:
        print(f"❌ Validation error: {e}", file=sys.stderr)

    sys.exit(0)

if __name__ == '__main__':
    main()
```

### 5. Settings Configuration

**`.claude/settings.json`** (updated)
```json
{
  "hooks": {
    "PostToolUse": {
      "commands": [".claude/hooks/validate_lesson_format.py"]
    }
  }
}
```

### 6. Documentation

**`.claude/AUTOMATION_README.md`**
```markdown
# Automation System for Python Programming Course

## Generated On
2025-01-23

## Session ID
ed-course-abc123

## What Was Created

### Analysis Phase

- **structure-analyzer**: Course well-organized, but inconsistent lesson numbering in module 5
- **workflow-analyzer**: Identified repetitive quiz creation as major time sink
- **learning-path-analyzer**: Clear progression, but module 8 prerequisites need clarification
- **assessment-analyzer**: LOW COVERAGE - Only 17% (8 quizzes for 48 lessons)

### Generated Artifacts

#### Custom Agents (6)
- **structure-analyzer**: Analyzes course organization
- **workflow-analyzer**: Identifies automation opportunities
- **learning-path-analyzer**: Validates learning progression
- **assessment-analyzer**: Checks quiz coverage
- **skill-generator**: Created 3 custom skills
- **command-generator**: Created 3 slash commands

#### Skills (3)
- **quiz-generator**: Auto-generates quiz questions from lessons (SAVES 20 MIN/QUIZ!)
- **lesson-formatter**: Enforces consistent lesson structure
- **prerequisite-validator**: Validates learning path dependencies

#### Commands (3)
- **/generate-quiz**: Create quiz for module/lesson
- **/check-progression**: Validate course structure
- **/export-course**: Export to PDF/HTML/SCORM

#### Hooks (1)
- **PostToolUse**: Validates lesson format on save

## Impact Assessment

### Time Savings
- Quiz generation: 20 min/quiz × 40 missing quizzes = **13.3 hours saved**
- Lesson formatting: 5 min/lesson × 48 lessons = **4 hours saved**
- Prerequisite validation: 30 min/module × 12 modules = **6 hours saved**
- **Total: ~23 hours saved** + ongoing maintenance

### Quality Improvements
- **100% quiz coverage** (up from 17%)
- **Consistent lesson format** across all content
- **Valid learning path** with no circular dependencies
- **Professional export formats** (PDF, HTML, SCORM)

## Quick Start

1. Generate missing quizzes:
   ```bash
   /generate-quiz --all
   ```

2. Validate course structure:
   ```bash
   /check-progression --visual
   ```

3. Format all lessons:
   ```bash
   "Format all lessons in the course"
   # lesson-formatter skill auto-invokes
   ```

4. Create new lesson (format validated automatically):
   ```bash
   # Edit any lesson file
   # Hook validates format on save
   ```

## Course Statistics

- **48 Lessons** across 12 modules
- **8 Quizzes** → Will be 48 quizzes (100% coverage)
- **32 Exercises** with solutions
- **Learning Path Depth:** 6 levels
- **Estimated Course Duration:** 24 hours

## Customization

All generated automation can be customized:
- Edit skills in `.claude/skills/`
- Modify commands in `.claude/commands/`
- Adjust hooks in `.claude/hooks/`

## Session Data

All agent communication is logged in:
`.claude/agents/context/ed-course-abc123/`

Review this directory to understand what automation decisions were made and why.
```

## Agent Communication Example

**`coordination.json`**
```json
{
  "session_id": "ed-course-abc123",
  "started_at": "2025-01-23T14:00:00Z",
  "project_type": "educational",
  "secondary_types": ["programming"],
  "agents": {
    "structure-analyzer": {
      "status": "completed",
      "completed_at": "2025-01-23T14:03:00Z",
      "report_path": "reports/structure-analyzer.json"
    },
    "learning-path-analyzer": {
      "status": "completed",
      "completed_at": "2025-01-23T14:05:00Z",
      "report_path": "reports/learning-path-analyzer.json"
    },
    "assessment-analyzer": {
      "status": "completed",
      "completed_at": "2025-01-23T14:06:00Z",
      "report_path": "reports/assessment-analyzer.json"
    }
  }
}
```

**`reports/assessment-analyzer.json`** (excerpt)
```json
{
  "agent_name": "assessment-analyzer",
  "summary": "CRITICAL: Only 17% assessment coverage. 40 modules lack quizzes.",
  "findings": [
    {
      "type": "gap",
      "severity": "critical",
      "title": "Insufficient Quiz Coverage",
      "description": "Only 8 quizzes for 48 lessons (17% coverage). Industry standard is 80-100%.",
      "location": "quizzes/",
      "recommendation": "Generate quizzes for all modules using automated question extraction",
      "time_saved_if_automated": "20 minutes per quiz × 40 quizzes = 13.3 hours"
    }
  ],
  "recommendations_for_automation": [
    "Skill: quiz-generator - Auto-generate from lesson content",
    "Command: /generate-quiz --all - Batch generate missing quizzes",
    "Hook: Suggest quiz creation when module is complete"
  ],
  "automation_impact": {
    "time_saved": "13.3 hours",
    "quality_improvement": "83% increase in coverage (17% → 100%)"
  }
}
```

## Result

Course creator now has powerful automation:
- ✅ Can generate 40 missing quizzes in minutes (vs. 13+ hours manually)
- ✅ All lessons formatted consistently
- ✅ Learning path validated with no circular dependencies
- ✅ Hook prevents incorrectly formatted lessons
- ✅ Can export to professional formats (PDF, SCORM)
- ✅ **23+ hours saved** in course development and maintenance

## Before vs After

**Before:**
```
# Manual workflow
- Write lesson → 30 min
- Format manually → 5 min
- Create quiz → 20 min
- Validate prerequisites → 5 min
- Total: 60 min per lesson × 48 = 48 hours
```

**After:**
```
# Automated workflow
- Write lesson → 30 min
- Auto-formatted on save → 0 min
- Generate quiz → 1 min (/generate-quiz)
- Auto-validated → 0 min
- Total: 31 min per lesson × 48 = 24.8 hours

SAVINGS: 23+ hours (48% reduction!)
```

**Quality Improvement:**
- Quiz coverage: 17% → 100% (+83%)
- Format consistency: 60% → 100% (+40%)
- Valid learning paths: 90% → 100% (+10%)
