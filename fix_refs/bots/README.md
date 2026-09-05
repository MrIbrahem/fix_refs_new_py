# fix_refs/bots - Transformation Bots

## Project Overview

The `bots/` module contains individual transformation functions that operate on wikitext. Each bot performs a specific, focused transformation such as fixing references, moving punctuation, translating months, or validating images.

### Main Modules

| File                       | Purpose                                                                                       | Lines                                    |
| -------------------------- | --------------------------------------------------------------------------------------------- | ---------------------------------------- | --- |
| `mini_fixes.py`            | Whitespace cleanup, section title translation, ref tag spacing, interwiki link simplification | 127                                      |
| `fix_missing_refs.py`      | Expands short refs (`<ref name="x"/>`) from MDWiki source text                                | 111                                      |
| `remove_duplicate_refs.py` | Deduplicates references with identical content                                                | 67                                       |
| `move_dots.py`             | Moves punctuation after refs to before refs (language-specific)                               | 32                                       |
| `add_lang_en_bot.py`       | Adds `                                                                                        | language=en` to English source citations | 61  |
| `expend_refs.py`           | Reference expansion utilities for short-to-full citation conversion                           | 64                                       |
| `fix_images.py`            | Validates images against Wikimedia Commons API, removes missing ones                          | 256                                      |
| `months.py`                | Translates English month names to Portuguese/Spanish                                          | 100                                      |
| `refs_utils.py`            | String utility wrappers                                                                       | 92                                       |
| `redirect.py`              | Redirect page detection                                                                       | 32                                       |

### Technologies

-   **wikitextparser** - Used in most bots for AST-based wikitext manipulation
-   **re** - Regular expressions for pattern matching
-   **requests** (via `utils/http.py`) - For Commons API calls in `fix_images.py`

---

## Architecture & Code Quality Review

### Code Organization

Each bot file has a single responsibility. The module-level docstrings describe purpose clearly. Functions are generally small and focused.

### Design Patterns

-   **Pure functions** - Most bots are stateless functions that take text in and return text out
-   **Decorator pattern** - `@lru_cache` for image existence caching
-   **Separation of concerns** - Each file handles one transformation type

### Maintainability

Good - each bot is independent and can be modified or extended without affecting others. The pure-function approach makes testing straightforward.

### Readability

Mixed. Most functions have good docstrings, but some (like `expend_new` in infobox) use terse variable names (`str_`, `tempse_by_u`, `PP`).

---

## Strengths

1. **Pure function design** - All bots are stateless, taking text and returning transformed text
2. **Single responsibility** - Each file handles one transformation type
3. **Defensive image checking** (`fix_images.py`) - Returns `True` on API failure to avoid removing valid images
4. **LRU caching** on image checks prevents redundant API calls
5. **Good test coverage** - Each bot has corresponding test files

---

## Weaknesses

### Code Duplication

1. **`str_ends_with()` / `str_starts_with()`** in `refs_utils.py` are trivial wrappers around `str.endswith()` / `str.startswith()` - they add zero value
2. **`refs_expand()` and `refs_expand_work()`** in `expend_refs.py` do nearly the same thing with different input formats
3. **`start_end()`** helper is duplicated between `pt_bot.py` and `es_helpers.py`

### Trivial Utility Functions

`refs_utils.py` contains functions that don't justify their existence:

```python
def str_ends_with(string: str, end_string: str) -> bool:
    return string.endswith(end_string)

def str_starts_with(text: str, start: str) -> bool:
    return text.startswith(start)
```

These are just wrappers around Python built-ins and should be replaced with direct calls.

### Inconsistent Error Handling

-   `fix_images.py` has thorough error handling with fallbacks
-   `fix_missing_refs.py` silently returns empty strings on errors
-   `mini_fixes.py` has no error handling at all

---

## Critical Issues

1. **`refs_utils.py:remove_start_end_quotes()`** - Complex quote normalization logic with multiple edge cases. The partial-quote handling (lines 76-87) is fragile and could produce incorrect results for strings with mixed quote types.

2. **`remove_duplicate_refs.py:55`** - `str.replace()` for citation swapping could match substrings of other citations, causing corruption.

3. **`fix_images.py:129-171`** - `remove_missing_infobox_images()` modifies template arguments in-place while iterating, which could cause issues with wikitextparser's internal state.

---

## Areas That Need Attention

-   Remove trivial wrapper functions from `refs_utils.py`
-   Consolidate `refs_expand()` and `refs_expand_work()` into one function
-   Add error handling to `mini_fixes.py`
-   Add tests for `refs_utils.py` edge cases (quote normalization)
-   Consider batch API calls in `fix_images.py` for Commons checks

---

## Improvement Plan

### Quick Wins

1. Delete `str_ends_with`/`str_starts_with` from `refs_utils.py`, use built-ins
2. Remove `refs_expand_work()` or merge it with `refs_expand()`
3. Remove duplicate `start_end()` function

### Medium-term

1. Add input validation to transformation functions
2. Implement batch Commons API checking in `fix_images.py`
3. Add comprehensive tests for `refs_utils.py` quote handling

### Long-term

1. Create a bot registry/plugin system for dynamic bot loading
2. Add metrics collection for transformation success rates

---

## Comprehensive Review

| Metric                   | Score      | Notes                                                             |
| ------------------------ | ---------- | ----------------------------------------------------------------- |
| **Overall Rating**       | 7/10       | Good functional decomposition, but some dead code and duplication |
| **Production Readiness** | Good       | Core transformations are reliable                                 |
| **Technical Debt**       | Low-Medium | Trivial wrappers and minor duplication                            |
| **Risk Assessment**      | Low        | Pure functions are easy to test and verify                        |
| **Maintainability**      | 7/10       | Independent modules, but some code smell                          |
