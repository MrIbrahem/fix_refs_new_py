# fix_refs/mdwiki - MDWiki Integration

## Project Overview

The `mdwiki/` module handles integration with MDWiki (mdwiki.toolforge.org), specifically managing category assignment for translated articles. It fetches category information from Wikidata and adds appropriate translation attribution categories to processed pages.

### Main Modules

| File | Purpose |
|------|---------|
| `category.py` | Fetches MDWiki categories from Wikidata API and adds them to translated pages |

### Key Functions

| Function | Purpose |
|----------|---------|
| `add_translated_from_mdwiki()` | Main entry point - adds MDWiki category to text if not present |
| `get_mdwiki_category()` | Gets the appropriate category name for a language |
| `get_cats()` | Fetches category data from Wikidata with local file fallback |
| `load_from_local_file()` | Loads categories from local JSON file |

### Technologies

- **requests** (via `utils/http.py`) - Wikidata API calls
- **json** - Data parsing
- **re** - Category pattern matching

---

## Architecture & Code Quality Review

### Code Organization

Single-file module with clear function hierarchy. Each function has a specific responsibility.

### Design Patterns

- **Fallback pattern** - API call with local file fallback
- **Guard clause** - Early returns for skipped languages
- **Idempotent insertion** - Checks for existing category before adding

### Maintainability

Good. The fallback strategy ensures the module works offline. The skip list makes it easy to exclude languages.

### Readability

Clear function names and docstrings. The logic is straightforward.

---

## Strengths

1. **Robust fallback strategy** - Tries Wikidata API first, falls back to local JSON file
2. **Idempotent operations** - Checks for existing category before adding, safe to call multiple times
3. **Skip list for languages** - Excludes languages that don't need the category (e.g., Italian, English, Bulgarian)
4. **Good error handling** - Catches JSON decode errors and IO errors gracefully

---

## Weaknesses

1. **Hardcoded skip lists** - `skip_langs` appears in both `get_mdwiki_category()` (line 63) and `add_translated_from_mdwiki()` (line 86) with different values:
   ```python
   # get_mdwiki_category()
   skip_langs = ["it", "en"]

   # add_translated_from_mdwiki()
   skip_langs = ["it", "en", "bg"]
   ```
   The inconsistency means `get_mdwiki_category("bg")` returns a category, but `add_translated_from_mdwiki()` skips Bulgarian entirely.

2. **Import inside function** - `import re` on line 83 is inside `add_translated_from_mdwiki()` instead of at module level.

3. **No caching** - `get_cats()` makes an API call every time (no `lru_cache` like settings.py uses).

---

## Critical Issues

1. **Inconsistent skip lists** - `get_mdwiki_category()` skips `["it", "en"]` but `add_translated_from_mdwiki()` skips `["it", "en", "bg"]`. This means the category fetching logic and the category addition logic have different views of which languages should be processed.

---

## Areas That Need Attention

- Consolidate skip lists into a single constant
- Move `import re` to module level
- Add caching to `get_cats()` to avoid repeated API calls
- Add tests for the fallback behavior
- Document the Wikidata API endpoint and expected response format

---

## Improvement Plan

### Quick Wins

1. Consolidate skip lists into a module-level constant
2. Move `import re` to module top
3. Add `@lru_cache` to `get_cats()`

### Medium-term

1. Add tests for API fallback behavior
2. Document the Wikidata API integration
3. Add configurable skip list

### Long-term

1. Support additional category sources beyond Wikidata
2. Add category validation (verify category exists on target wiki)

---

## Comprehensive Review

| Metric | Score | Notes |
|--------|-------|-------|
| **Overall Rating** | 7/10 | Clean and functional, but inconsistent skip lists |
| **Production Readiness** | Good | Works reliably with fallback |
| **Technical Debt** | Low | Minor issues with skip list inconsistency |
| **Risk Assessment** | Low | Fallback ensures availability |
| **Maintainability** | 8/10 | Simple, focused module |
