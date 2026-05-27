# fix_refs/lang_bots - Language-Specific Processing

## Project Overview

The `lang_bots/` module contains language-specific transformation bots for processing Wikipedia translations. Each bot handles locale-specific formatting, template translations, and reference conventions for a target Wikipedia language edition.

### Supported Languages

| Language | Module | Complexity | Key Operations |
|----------|--------|------------|----------------|
| Spanish (es) | `es/` subpackage | High | Template name translation, parameter mapping, month translation, ref reorganization, section insertion |
| Portuguese (pt) | `pt_bot.py` | Medium | Month translation, ref spacing |
| Bulgarian (bg) | `bg_bot.py` | Medium | Translation template insertion, category cleanup |
| Armenian (hy) | `hy_bot.py` | Medium | Ref-punctuation spacing, word-ref spacing |
| Polish (pl) | `pl_bot.py` | Low | Medical infobox parameter insertion |
| Swahili (sw) | `sw_bot.py` | Low | Section title correction |

### Technologies

- **wikitextparser** - AST-based wikitext manipulation (Spanish, Polish, Portuguese)
- **re** - Regular expressions (all bots)
- **datetime** - Date formatting (Spanish section bot)

---

## Architecture & Code Quality Review

### Code Organization

The module uses a dispatcher pattern via `apply_language_fixes()` in `__init__.py`. Each language has its own module. The Spanish subpackage (`es/`) is the most complex, decomposed into:
- `es_bot.py` - Template transformation logic
- `es_data.py` - Template/parameter name mappings
- `es_helpers.py` - Shared helper functions
- `es_refs.py` - Reference reorganization
- `es_section_bot.py` - Section/template insertion

### Design Patterns

- **Dispatcher pattern** via `apply_language_fixes()` for language routing
- **Data-driven transformation** - Spanish bot uses lookup tables (`REFS_TEMPS`, `ARGS_TO`) for template/parameter mapping
- **Pure functions** - Each bot function takes text and returns transformed text

### Maintainability

The per-language isolation makes it easy to modify one language without affecting others. The Spanish subpackage is well-decomposed.

### Readability

Mixed. The Spanish subpackage has good documentation. Some other bots (like `remove_space.py`) have debug `print()` statements and minimal documentation.

---

## Strengths

1. **Clean language isolation** - Each language is independent, easy to add new languages
2. **Data-driven Spanish bot** - Template mappings are in a separate data file, not hardcoded in logic
3. **Well-decomposed Spanish module** - Separation of data, helpers, refs, and section processing
4. **Defensive checks** - Most bots check for existing templates before inserting new ones
5. **Dispatcher is simple** - `apply_language_fixes()` is easy to understand and extend

---

## Weaknesses

### Code Duplication

1. **`start_end()`** is defined identically in `pt_bot.py:10-12` and `es_helpers.py:23-25`
2. **`remove_short_refs()`** is defined identically in `es_refs.py:75-86` and `es_helpers.py:10-19`
3. **`str_ends_with()` / `str_starts_with()`** are duplicated in `hy_bot.py` (already exist in `bots/refs_utils.py`)
4. **Month translation** logic is nearly identical between `pt_bot.py` and `es_helpers.py`

### Debug Prints in Production Code

`remove_space.py` has bare `print()` statements:

```python
# lines 28, 36, 51, 58, 65
print(f"count(matches)={len(matches)}")
print(f"count(new_parts)={len(new_parts)}")
print(f"charter={charter}")
print(f"count(last_ref)={len(last_ref_matches)}")
print("endswith")
```

These should use `echo_debug()` or be removed entirely.

### Dispatcher Bug

`lang_bots/__init__.py:14-31`:
```python
if lang == "pl":
    text = pl_fixes(text)

if lang == "pt":     # <-- should be elif
    text = pt_fixes(text)

elif lang == "bg":
    ...
```

The first `if` for Polish is standalone, then the chain switches to `if`/`elif`. This means if `lang == "pl"`, the function runs `pl_fixes()` and then checks `if lang == "pt"` (which is False), then skips all `elif` branches. The behavior is correct, but the inconsistent control flow is confusing and fragile.

---

## Critical Issues

1. **Debug prints in production** (`remove_space.py`) - `print()` statements will output to stdout in production, potentially polluting logs
2. **Dispatcher control flow** (`__init__.py`) - Mixing standalone `if` with `if`/`elif` chain is error-prone

---

## Areas That Need Attention

- Remove or gate `print()` statements in `remove_space.py`
- Consolidate duplicated functions (`start_end`, `remove_short_refs`, `str_ends_with`)
- Fix the dispatcher control flow to use consistent `if`/`elif`
- Add docstrings to `remove_space.py` module
- Add tests for edge cases in each language bot

---

## Improvement Plan

### Quick Wins

1. Replace `print()` with `echo_debug()` in `remove_space.py`
2. Fix dispatcher to use consistent `if`/`elif` pattern
3. Remove duplicated `str_ends_with`/`str_starts_with` from `hy_bot.py`

### Medium-term

1. Extract shared helpers (`start_end`, `remove_short_refs`, month translation) into a common module
2. Add validation for language codes in the dispatcher
3. Add comprehensive test coverage for each language bot

### Long-term

1. Implement a plugin registry for language bots (dynamic discovery)
2. Add configuration-driven bot selection (which transformations to apply per language)

---

## Comprehensive Review

| Metric | Score | Notes |
|--------|-------|-------|
| **Overall Rating** | 7/10 | Good language isolation, but has debug prints and duplication |
| **Production Readiness** | Moderate | Works but has debug output in production code |
| **Technical Debt** | Medium | Duplicated functions, debug prints, inconsistent control flow |
| **Risk Assessment** | Low-Medium | Debug prints could expose internal state; dispatcher is fragile |
| **Maintainability** | 7/10 | Per-language isolation is good; duplication adds friction |
