# fix_refs/infobox - Infobox Template Expansion

## Project Overview

The `infobox/` module handles the expansion and formatting of MediaWiki infobox templates. It reformats collapsed single-line infobox templates into readable multi-line format with aligned parameters.

### Main Modules

| File                | Purpose                                                             |
| ------------------- | ------------------------------------------------------------------- |
| `expend_infobox.py` | Infobox template expansion, comment formatting, parameter alignment |

### Key Functions

| Function                         | Purpose                                               |
| -------------------------------- | ----------------------------------------------------- |
| `expand_infobox_in_text()`       | Main entry point - expands infobox in wikitext        |
| `expend_new()`                   | Reformats a single template with aligned parameters   |
| `do_comments()`                  | Converts HTML comment section headers to visible text |
| `extract_templates_and_params()` | Extracts all templates and their parameters           |
| `make_section_0()`               | Extracts the section before the first heading         |

### Technologies

-   **wikitextparser** - Template parsing and manipulation
-   **re** - Regular expressions for comment pattern matching

---

## Architecture & Code Quality Review

### Code Organization

Single-file module with focused responsibilities. Functions are ordered logically: helpers first, main function last.

### Design Patterns

-   **Template processing** - Finds the largest template (by length) as the "main" infobox
-   **String manipulation** - Uses wikitextparser for parsing but falls back to string operations

### Maintainability

The module is relatively self-contained. The comment regex pattern is complex but well-defined.

### Readability

Mixed. Variable names like `tempse_by_u`, `PP`, `u`, `y1`, `u1`, `y2`, `u2` are cryptic. The `---` comment markers are used as visual separators but add noise.

---

## Strengths

1. **Handles complex infobox formats** - Can process multi-parameter templates with nested content
2. **Comment section formatting** - Converts HTML comments to visible section headers
3. **Parameter alignment** - Pads parameter names for readable output

---

## Weaknesses

### Naming Issues

1. **`expend_infobox`** - Misspelling of "expand" throughout
2. **`expend_new()`** - Unclear name; should be `format_template()` or `align_template_params()`
3. **Cryptic variable names**:
    ```python
    tempse_by_u = {}  # templates indexed by number
    tempse = {}       # template sizes
    PP = [[y1, u1] for u1, y1 in tempse.items()]  # sorted template sizes
    ```

### Code Smell

1. **`---` comment markers** - Used extensively as visual separators; these are not standard Python practice
2. **`u += 1` counter** - Should use `enumerate()`
3. **Complex template selection logic** - The "find largest template" heuristic is fragile

### Missing Documentation

-   `expend_new()` has no docstring
-   `make_section_0()` has no docstring
-   `extract_templates_and_params()` has no docstring

---

## Critical Issues

1. **Template selection heuristic** (`expend_infobox.py:130-146`) - The code selects the "main" infobox as the template with the most parameters (>4) and the longest text. This heuristic could fail for pages with multiple large templates.

2. **String replacement fragility** (`expend_infobox.py:156`) - `newtext.replace(main_temp_text, new_temp)` could match the template text in unexpected locations (e.g., inside comments or nowiki tags).

---

## Areas That Need Attention

-   Fix "expend" -> "expand" typo in function names
-   Add docstrings to all functions
-   Improve variable naming
-   Add tests for edge cases (multiple infoboxes, nested templates)
-   Consider using wikitextparser's API for template modification instead of string replacement

---

## Improvement Plan

### Quick Wins

1. Fix "expend" typo to "expand"
2. Add docstrings to `expend_new()`, `make_section_0()`, `extract_templates_and_params()`
3. Replace `u += 1` with `enumerate()`

### Medium-term

1. Improve variable naming throughout
2. Add comprehensive tests for infobox expansion
3. Handle edge cases (multiple infoboxes, nested templates)

### Long-term

1. Replace string-based template modification with AST-based operations
2. Make template selection heuristic configurable

---

## Comprehensive Review

| Metric                   | Score    | Notes                                                                  |
| ------------------------ | -------- | ---------------------------------------------------------------------- |
| **Overall Rating**       | 5.5/10   | Functional but has naming issues, missing docs, and fragile heuristics |
| **Production Readiness** | Moderate | Works for common cases but has edge case risks                         |
| **Technical Debt**       | Medium   | Naming, documentation, and fragile string operations                   |
| **Risk Assessment**      | Medium   | Template selection heuristic could misidentify infoboxes               |
| **Maintainability**      | 5/10     | Cryptic names and missing docs make modification risky                 |
