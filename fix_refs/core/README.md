# fix_refs/core - Orchestration Layer

## Project Overview

The `core/` module is the orchestration layer for the fix_refs library. It contains the main entry points that coordinate all transformation bots in a deterministic pipeline.

### Main Modules

| File | Purpose |
|------|---------|
| `fix_page.py` | Main `fix_one_page()` function - the pipeline orchestrator |
| `settings.py` | Loads per-language settings from JSON file or remote API |

### Technologies

- Python 3.10+ with type hints
- `functools.lru_cache` for settings caching
- `wikitextparser` (indirectly, via bots)

---

## Architecture & Code Quality Review

### Code Organization

The module has a clean two-file structure: one for the pipeline, one for configuration. This is a good separation of concerns.

### Design Patterns

- **Pipeline pattern**: `fix_one_page()` applies 10 sequential transformation steps
- **Facade pattern**: `DoChangesToText1()` wraps settings loading + pipeline invocation
- **Cache-aside pattern**: `load_settings()` uses `lru_cache` to avoid repeated file/API reads

### Pipeline Steps (in order)

1. Redirect detection (skip if redirect)
2. Infobox expansion
3. Mini fixes (whitespace, section titles, ref tag spacing)
4. Missing ref expansion (from MDWiki source)
5. Duplicate ref removal
6. Dot moving (if enabled)
7. Add English language parameter (if enabled)
8. Language-specific fixes
9. Category addition (if enabled)
10. Post-fix mini fixes

### Maintainability

The pipeline is easy to read and modify. Adding a new step is straightforward - just add a function call in sequence.

### Readability

Good docstrings with Args/Returns. The `expand_infobox_if_needed()` helper extracts conditional logic cleanly.

---

## Strengths

1. **Clear pipeline sequence** - Every transformation step is visible and ordered
2. **Safety fallback** - Returns original text if pipeline produces empty output (`fix_page.py:81-82`)
3. **Settings caching** - `lru_cache` on `load_settings()` prevents repeated API/file reads
4. **Dual entry points** - `fix_one_page()` for direct use, `DoChangesToText1()` for settings-aware use

---

## Weaknesses

### Critical Bug: `or True` Always True

```python
# core/__init__.py:14
expand = bool(int(lang_default.get("expend", 1))) or True
```

The `or True` makes this expression **always `True`**, regardless of the language setting. This means the `expend` configuration value is completely ignored. This is almost certainly a bug - the intent was likely:

```python
expand = bool(int(lang_default.get("expend", 1)))
```

### Naming Issues

1. **`DoChangesToText1()`** - PascalCase function name violates PEP 8 conventions. Should be `do_changes_to_text()` or similar.
2. **`expend_infobox`** parameter - "expend" is a misspelling of "expand". Appears in function signatures throughout.
3. **`expand_infobox_if_needed()`** uses "expand" while the parameter is "expend" - inconsistent within the same file.

### Missing Type Hints

- `expand_infobox_if_needed()` lacks type annotations on parameters
- `DoChangesToText1()` has `mdwiki_revid: int|str` which is unusual - should the caller normalize this?

### Docstring Mismatch

`fix_page.py:42` docstring says `infobox:` but the parameter is `expend_infobox`. The docstring is outdated.

---

## Critical Issues

1. **`or True` bug** makes `expand` always True, ignoring configuration
2. **`DoChangesToText1()` accepts `int|str`** for `mdwiki_revid` without normalization - callers passing strings could cause downstream issues

---

## Areas That Need Attention

- Fix the `or True` bug in `core/__init__.py:14`
- Rename `DoChangesToText1()` to follow Python naming conventions
- Fix "expend" typo to "expand" in all parameter names
- Add missing type hints to `expand_infobox_if_needed()`
- Update docstring in `fix_page.py` to match actual parameter names

---

## Improvement Plan

### Quick Wins

1. Remove `or True` from the expand setting
2. Fix the "expend" -> "expand" typo
3. Add type hints to `expand_infobox_if_needed()`

### Medium-term

1. Rename `DoChangesToText1()` to a PEP 8 compliant name
2. Normalize `mdwiki_revid` to always be `int`
3. Consider making the pipeline steps configurable (list of callables)

---

## Comprehensive Review

| Metric | Score | Notes |
|--------|-------|-------|
| **Overall Rating** | 7/10 | Clean orchestration, but the `or True` bug is significant |
| **Production Readiness** | Moderate | Pipeline works but config is partially broken |
| **Technical Debt** | Low-Medium | Naming issues and one logic bug |
| **Risk Assessment** | Medium | `or True` silently overrides configuration |
| **Maintainability** | 8/10 | Clear, linear pipeline is easy to modify |
