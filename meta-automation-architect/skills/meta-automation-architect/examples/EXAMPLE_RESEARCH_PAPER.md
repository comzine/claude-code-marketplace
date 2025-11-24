# Example: Research Paper with Presentation and Documentation

This example shows what the meta-automation-architect generates for a research project that combines **LaTeX** (paper), **HTML** (presentation), and **Markdown** (documentation).

## Project Context

- **Type**: Academic Writing (primary) + Research (secondary)
- **Content**:
  - LaTeX research paper (25 pages, 8 chapters, 45 references)
  - HTML presentation slides (30 slides)
  - Markdown documentation and notes (50+ files)
- **Pain Points**: Broken cross-references, unused citations, broken links, inconsistent formatting
- **Priority**: Citation validation and link checking

## Project Structure

```
research-paper/
├── paper/
│   ├── main.tex                 # Main LaTeX document
│   ├── chapters/
│   │   ├── 01_introduction.tex
│   │   ├── 02_related_work.tex
│   │   ├── 03_methodology.tex
│   │   ├── 04_results.tex
│   │   ├── 05_discussion.tex
│   │   └── 06_conclusion.tex
│   ├── figures/
│   │   ├── figure1.pdf
│   │   ├── figure2.pdf
│   │   └── ... (15 figures)
│   ├── tables/
│   │   ├── table1.tex
│   │   └── ... (5 tables)
│   ├── references.bib           # Bibliography (45 entries)
│   └── custom.sty               # Custom LaTeX style
├── presentation/
│   ├── index.html               # Main presentation
│   ├── slides/
│   │   ├── 01_intro.html
│   │   ├── 02_methods.html
│   │   ├── 03_results.html
│   │   └── ... (30 slides)
│   ├── assets/
│   │   ├── figures/
│   │   ├── css/
│   │   └── js/
│   └── notes/
│       └── speaker_notes.md
├── notes/
│   ├── literature_review.md
│   ├── methodology_notes.md
│   ├── experiment_logs.md
│   ├── analysis/
│   │   ├── [[statistical_tests]].md
│   │   └── [[data_processing]].md
│   └── ideas/
│       └── future_work.md
└── README.md
```

## User Conversation

```
User: "Help me automate my research paper project"

Meta-Skill: Analyzing project...
- Detected: Academic Writing (68% confidence)
  - Found 25 .tex files
  - Found 1 .bib file with 45 entries
  - Found 30 HTML slides
  - Found 50+ interconnected markdown files
- Secondary: Research (32% confidence)
  - Research methodology documentation
  - Experiment logs and analysis

Meta-Skill: What are your main pain points?
Options:
- Broken LaTeX references (RECOMMENDED: Manual checking takes 30 min)
- Unused bibliography entries (RECOMMENDED: 12 unused entries detected)
- Broken HTML/Markdown links (RECOMMENDED: 8 broken links found)
- Inconsistent formatting

User: [Selects: Broken references, Unused citations, Broken links]

Meta-Skill: Automation opportunities identified:
- Validate LaTeX cross-references: Saves 30 min/compile
- Clean bibliography: Saves 20 min/review
- Check all links: Saves 30 min/validation
- Total potential savings: 80+ hours over project lifecycle

Meta-Skill: Generating automation system...
Session ID: research-paper-abc123
```

## Generated Automation System

### 1. Custom Subagents (8)

#### Universal Agents
- **structure-analyzer** - Reviews document organization across all formats
- **workflow-analyzer** - Analyzes compilation and publishing workflow

#### Academic Writing Domain Agents
- **latex-structure-analyzer** - LaTeX document structure and cross-references
- **citation-analyzer** - Bibliography validation and citation usage
- **html-structure-analyzer** - Presentation hierarchy and semantics
- **link-validator** - All links across HTML and Markdown
- **cross-reference-analyzer** - Cross-references across all document types
- **formatting-analyzer** - Formatting consistency

### 2. Custom Skills (4)

**`latex-validator`** - Comprehensive LaTeX validation

**Example:**
```
Running LaTeX validation...

✅ Document Structure
  - 6 chapters found
  - Proper hierarchy: chapter → section → subsection
  - TOC depth: 2 levels

⚠️  Cross-References
  - 23/25 \\ref commands valid
  - 2 broken references:
    * Line 145: \\ref{fig:missing} - target not found
    * Line 289: \\ref{sec:old-name} - outdated reference

✅ Figures/Tables
  - 15/15 figures referenced
  - 5/5 tables referenced
  - All captions present

⚠️  Bibliography
  - 45 entries in references.bib
  - 33 cited in text
  - 12 unused entries:
    * [Smith2020] - Never cited
    * [Jones2019] - Never cited
    * ...

📊 Compilation Status
  - pdflatex: ✅ Success
  - bibtex: ✅ Success
  - Output: main.pdf (2.3 MB)

💡 Recommendations:
  1. Fix 2 broken \\ref references
  2. Remove 12 unused bibliography entries (saves 20% .bib size)
  3. Consider adding \\label for Section 4.2 (referenced but not labeled)
```

**`link-checker`** - Validates all links in HTML and Markdown

**Example:**
```
Checking links across project...

📁 HTML Presentation (30 slides)
  ✅ Internal links: 45/45 valid
  ✅ External links: 12/12 valid
  ✅ Asset references: 28/28 valid

📁 Markdown Notes (52 files)
  ✅ Wiki-style [[links]]: 67/75 valid
  ⚠️  Broken wiki links (8):
    * notes/analysis/stats.md → [[missing_page]]
    * notes/ideas/future.md → [[old-experiment]]
    * ...
  ✅ External links: 34/35 valid
  ⚠️  1 broken external link:
    * http://oldwebsite.com/data → 404 Not Found

📊 Summary
  - Total links checked: 185
  - Valid: 177 (95.7%)
  - Broken: 8 (4.3%)
  - Orphaned pages: 2 (no incoming links)

💡 Recommendations:
  1. Fix 8 broken wiki links
  2. Update 1 broken external link
  3. Consider linking to orphaned pages
  4. Estimated fix time: 15 minutes
```

**`cross-reference-checker`** - Validates references across all formats

**Example:**
```
Analyzing cross-references...

📄 LaTeX Paper
  - \\ref commands: 25 (23 valid, 2 broken)
  - \\cite commands: 33 (all valid)
  - Figure refs: 15 (all valid)
  - Table refs: 5 (all valid)

🖥️ HTML Presentation
  - Internal anchor links: 45 (all valid)
  - Figure references: 12 (all valid)
  - Paper references: 8 links to LaTeX sections

📝 Markdown Notes
  - Internal [[links]]: 75 (67 valid, 8 broken)
  - Cross-format refs: 5 links to paper sections

🔗 Cross-Format Consistency
  ✅ Methodology: Consistent between paper and presentation
  ✅ Results: Figures match in paper and slides
  ⚠️  Discussion section in paper not reflected in presentation
  💡 Consider adding discussion slide

📊 Overall Reference Health: 96.2%
```

**`bibliography-manager`** - Manages .bib entries and citations

**Example:**
```
Analyzing bibliography...

📚 references.bib
  - Total entries: 45
  - Used in paper: 33 (73%)
  - Unused: 12 (27%)

🔍 Citation Analysis
  - Most cited: [Smith2020] (8 times)
  - Least cited: [Wang2021] (1 time)
  - Average citations: 2.4 per entry

⚠️  Issues Found
  1. Unused entries (12):
     * [Smith2020] - Never cited (can be removed)
     * [Jones2019] - Never cited (can be removed)
     * ...

  2. Missing fields (3):
     * [Brown2021] - Missing 'pages' field
     * [Davis2022] - Missing 'doi' field
     * [Wilson2020] - Inconsistent author format

  3. Duplicate entries (2):
     * [Lee2019] and [Lee2019b] - Same paper
     * [Miller2020] and [Miller2020a] - Same paper

💡 Recommendations:
  1. Remove 12 unused entries → 27% smaller .bib file
  2. Merge 2 duplicate entries
  3. Complete missing fields for better citations
  4. Run: /clean-bibliography to apply fixes
```

### 3. Custom Commands (4)

**`/validate-latex`**
```bash
/validate-latex                  # Full validation
/validate-latex --refs-only      # Only check references
/validate-latex --fix            # Auto-fix common issues
```

**`/check-links`**
```bash
/check-links                     # Check all links
/check-links presentation/       # Only HTML slides
/check-links notes/              # Only Markdown notes
/check-links --external          # Include external links
```

**`/clean-bibliography`**
```bash
/clean-bibliography              # Interactive cleanup
/clean-bibliography --remove-unused  # Auto-remove unused entries
/clean-bibliography --fix-format     # Fix formatting issues
```

**`/build-paper`**
```bash
/build-paper                     # Compile LaTeX to PDF
/build-paper --watch             # Auto-compile on changes
/build-paper --validate          # Validate before building
```

### 4. Hooks (3)

**`validate_on_save.py`** (PreToolUse)
- Triggers when .tex or .bib files are saved
- Runs quick validation checks
- Alerts if new issues introduced

**`update_references.py`** (PostToolUse)
- Triggers after editing .tex files
- Updates cross-reference index
- Checks for new broken references

**`link_check_on_md_save.py`** (PostToolUse)
- Triggers when .md files are saved
- Validates wiki-style [[links]]
- Alerts if broken links created

### 5. Impact

**Time Savings:**
- Manual LaTeX validation: 30 min/compile → **2 minutes** automated (93% reduction)
- Bibliography cleanup: 45 min/cleanup → **5 minutes** automated (89% reduction)
- Link checking: 30 min/check → **1 minute** automated (97% reduction)
- Cross-reference validation: 20 min/review → **2 minutes** automated (90% reduction)
- **Total: 125 min → 10 min** (92% time reduction per validation cycle)

Over typical paper lifecycle (50 validation cycles):
- Manual: **104 hours**
- Automated: **8 hours**
- **Savings: 96 hours (92%)**

**Quality Improvements:**
- Cross-reference accuracy: Manual checking → **100% validated** automatically
- Bibliography: 12 unused entries → **0 unused** (27% smaller .bib)
- Link health: 92% valid → **100% valid** (8 broken links fixed)
- Compilation success rate: 80% → **100%** (catches issues before compile)

**Concrete Fixes Applied:**
- Fixed 2 broken LaTeX \\ref references
- Removed 12 unused bibliography entries
- Fixed 8 broken Markdown wiki links
- Updated 1 broken external link
- Merged 2 duplicate .bib entries
- Completed 3 missing bibliography fields

## Example Results

### Before Automation

**LaTeX Compilation:**
```
! LaTeX Error: Reference `fig:missing' on page 12 undefined.
! LaTeX Error: Reference `sec:old-name' on page 23 undefined.

Warning: Citation 'Smith2020' unused
Warning: Citation 'Jones2019' unused
... (10 more unused citations)

Output: main.pdf generated with warnings
```

**Manual Link Checking:**
```
Manually clicking through 185 links...
Found broken link after 15 minutes
Found another after 20 minutes
Gave up after 30 minutes, unsure if all checked
```

**Bibliography Management:**
```
45 entries in .bib file
Manually grep for each to see if cited
Takes 45 minutes to identify 12 unused entries
Not sure about duplicates or format issues
```

### After Automation

**`/validate-latex` Output:**
```
✅ Running comprehensive LaTeX validation...

📊 Results (completed in 2 minutes):
  ✅ Document structure: Valid
  ⚠️  Cross-references: 2 issues found
  ✅ Bibliography: All citations valid
  ⚠️  Unused entries: 12 found
  ✅ Compilation: Success

🔧 Auto-fix available:
  Run: /validate-latex --fix
```

**`/check-links` Output:**
```
✅ Link validation complete (1 minute):
  - 185 total links
  - 177 valid (95.7%)
  - 8 broken (4.3%)

📋 Detailed report: reports/link-validator.json
💡 Run: /check-links --fix to auto-fix wiki links
```

**`/clean-bibliography` Output:**
```
✅ Bibliography analysis complete (5 minutes):
  - Removed 12 unused entries
  - Merged 2 duplicates
  - Fixed 3 incomplete entries
  - New size: 33 entries (73% of original)

💾 Backup: references.bib.backup
✅ Updated: references.bib
```

## Agent Communication

**`reports/latex-structure-analyzer.json`** (excerpt):
```json
{
  "agent_name": "latex-structure-analyzer",
  "summary": "Paper structure is sound. Found 2 broken cross-references and compilation warnings.",
  "findings": [
    {
      "type": "broken_reference",
      "severity": "high",
      "location": "chapters/03_methodology.tex:145",
      "description": "\\ref{fig:missing} references non-existent label",
      "recommendation": "Add \\label{fig:missing} to appropriate figure or fix reference"
    },
    {
      "type": "unused_bibliography",
      "severity": "medium",
      "description": "12 bibliography entries never cited in text",
      "entries": ["Smith2020", "Jones2019", ...],
      "recommendation": "Remove unused entries or add citations where appropriate"
    }
  ],
  "metrics": {
    "total_chapters": 6,
    "total_sections": 24,
    "total_references": 25,
    "valid_references": 23,
    "broken_references": 2,
    "bibliography_entries": 45,
    "cited_entries": 33,
    "unused_entries": 12
  },
  "automation_impact": {
    "time_saved": "30 min/validation (manual checking)",
    "quality_improvement": "100% reference validation vs. manual spot-checking"
  }
}
```

**`reports/link-validator.json`** (excerpt):
```json
{
  "agent_name": "link-validator",
  "summary": "Found 8 broken links across HTML and Markdown. 95.7% link health.",
  "findings": [
    {
      "type": "broken_wiki_link",
      "severity": "medium",
      "location": "notes/analysis/stats.md:23",
      "description": "[[missing_page]] does not exist",
      "recommendation": "Create missing_page.md or update link to correct page"
    },
    {
      "type": "broken_external_link",
      "severity": "high",
      "location": "notes/literature_review.md:156",
      "description": "http://oldwebsite.com/data returns 404",
      "recommendation": "Update to current URL or mark as archived"
    }
  ],
  "metrics": {
    "total_links": 185,
    "valid_links": 177,
    "broken_links": 8,
    "link_health_percentage": 95.7,
    "html_links": 57,
    "markdown_wiki_links": 75,
    "markdown_external_links": 35,
    "orphaned_pages": 2
  },
  "automation_impact": {
    "time_saved": "30 min/check (manual link clicking)",
    "quality_improvement": "100% coverage vs. ~60% manual coverage"
  }
}
```

## Result

Researcher now has:
- ✅ **100% validated cross-references** - No more broken \\ref in paper
- ✅ **Clean bibliography** - 27% smaller, no unused entries
- ✅ **All links validated** - 8 broken links fixed, 100% health
- ✅ **Consistent formatting** - Across LaTeX, HTML, and Markdown
- ✅ **Fast compilation** - Issues caught before build
- ✅ **96 hours saved** over project lifecycle (92% reduction)

**Before vs After:**

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Cross-reference validation | Manual, 30 min | 2 min automated | 93% faster |
| Bibliography unused entries | 12 (27%) | 0 (0%) | 100% clean |
| Link health | 92% (manual partial check) | 100% (full automated) | +8% |
| Validation coverage | ~60% (time limited) | 100% (comprehensive) | +40% |
| Time per validation cycle | 125 min | 10 min | 92% reduction |
| Time over project (50 cycles) | 104 hours | 8 hours | 96 hours saved |

**Ongoing Benefits:**
- Every save triggers validation
- New issues caught immediately
- No broken references in final paper
- Bibliography stays clean
- All links remain valid
- Compilation always succeeds

**Publication Quality:**
- Zero broken cross-references in submitted paper
- Professional bibliography (no unused entries)
- All presentation links work during defense
- Documentation fully interconnected
- Reviewers praise technical quality
