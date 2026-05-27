# fix_refs/lang_bots/es - Spanish Language Processing

## Project Overview

The `es/` subpackage handles Spanish-specific wikitext transformations. It is the most complex language bot in the project, with dedicated modules for data, helpers, reference processing, and section management.

### Main Modules

| File | Purpose |
|------|---------|
| `__init__.py` | Entry point - `fix_es_all()` orchestrates all Spanish fixes |
| `es_bot.py` | Template name and parameter translation (English -> Spanish) |
| `es_data.py` | Data tables: `REFS_TEMPS` (template names), `ARGS_TO`/`PARAMS_ES_UP` (parameter names) |
| `es_helpers.py` | Shared helpers: month translation, ref cleanup, template line insertion |
| `es_refs.py` | Reference reorganization: extracts refs and moves them into `{{listaref}}` template |
| `es_section_bot.py` | Inserts `{{Traducido ref MDWiki}}` template for translation attribution |

### Technologies

- **wikitextparser** - AST-based template and reference manipulation
- **re** - Regular expressions for template name/parameter replacement
- **datetime** - Date insertion in translation templates

---

## Architecture & Code Quality Review

### Code Organization

Excellent decomposition for a language bot:
- Data is separated from logic (`es_data.py`)
- Helpers are reusable across modules
- Ref processing is isolated from template translation
- Section insertion is its own concern

### Processing Pipeline

`fix_es_all()` applies:
1. `fix_es()` - Template translation, month translation, ref reorganization
2. `es_section()` - Translation attribution template insertion

`fix_es()` internally applies:
1. Redirect detection
2. `<references />` -> `{{listaref}}` replacement
3. Month translation in refs
4. Template name/parameter translation
5. Reference reorganization into `{{listaref}}`

### Design Patterns

- **Data-driven transformation** - All template/parameter mappings in `es_data.py`
- **Two-phase processing** - First translate templates, then reorganize refs
- **Defensive insertion** - Checks for existing templates before inserting

### Maintainability

Very good. The data/logic separation makes it easy to update Spanish template mappings without touching processing code.

---

## Strengths

1. **Excellent data/logic separation** - `es_data.py` contains all mappings, `es_bot.py` contains only logic
2. **Comprehensive template mapping** - 29 template name translations and 50+ parameter translations
3. **Reference reorganization** - Complex ref extraction and `{{listaref}}` insertion
4. **Defensive checks** - Verifies template doesn't already exist before inserting
5. **Good docstrings** - Functions have clear Args/Returns documentation

---

## Weaknesses

### Code Duplication

1. **`start_end()`** is duplicated with `pt_bot.py`:
   ```python
   # es_helpers.py:23-25 and pt_bot.py:10-12
   def start_end(cite_temp: str) -> bool:
       return cite_temp.startswith("{{") and cite_temp.endswith("}}")
   ```

2. **`remove_short_refs()`** is duplicated in `es_refs.py:75-86` and `es_helpers.py:10-19` - identical implementations

3. **`fix_es_months_in_refs()`** and `fix_pt_months_in_refs()` follow the same pattern

### Inconsistent Relative Imports

```python
# es_bot.py
from ...utils.debug import echo_test      # 3 levels up

# es_helpers.py
from ...bots.months import make_date_new_val_es  # 3 levels up

# es_section_bot.py
# No imports from parent modules
```

The triple-dot relative imports (`...`) are fragile and hard to follow.

### Magic Strings

`es_section_bot.py:32-33` uses hardcoded Spanish strings:
```python
if re.search(r'==\s*Enlaces\s*externos\s*==', text, re.IGNORECASE):
```

These should be constants or configurable.

---

## Critical Issues

1. **`es_refs.py:68`** - `x.string = asas` modifies the tag's string in-place while iterating over tags. This could cause wikitextparser to lose sync with the parsed structure.

2. **`es_bot.py:83`** - `new_text.replace(old_text_template, new_text_str)` uses string replacement which could match substrings of other templates if the template text appears multiple times.

---

## Areas That Need Attention

- Consolidate `remove_short_refs()` into a single shared function
- Extract `start_end()` into a shared utility
- Use constants for hardcoded Spanish strings in `es_section_bot.py`
- Add tests for edge cases in `es_refs.py` (ref extraction/reorganization)
- Consider using wikitextparser's API for template modification instead of string replacement

---

## Improvement Plan

### Quick Wins

1. Remove duplicate `remove_short_refs()` - keep one in `es_helpers.py`
2. Move `start_end()` to a shared location
3. Extract hardcoded strings to constants

### Medium-term

1. Replace string-based template replacement with AST-based operations
2. Add comprehensive tests for ref reorganization edge cases
3. Standardize import style across the subpackage

### Long-term

1. Create a reusable template translation framework that other languages can use
2. Add validation for template mapping completeness

---

## Comprehensive Review

| Metric | Score | Notes |
|--------|-------|-------|
| **Overall Rating** | 7.5/10 | Best-structured language bot, but has duplication and some fragile patterns |
| **Production Readiness** | Good | Handles complex Spanish transformations reliably |
| **Technical Debt** | Low-Medium | Some duplication and magic strings |
| **Risk Assessment** | Low-Medium | String replacement could cause edge-case issues |
| **Maintainability** | 8/10 | Good decomposition, data/logic separation |
