# fix_refs - MediaWiki Reference Fixer

## Project Overview

`fix_refs` is a Python library for parsing, normalizing, and fixing references (citations) in MediaWiki wikitext. It was built for WikiProjectMed's Translation Dashboard to process Wikipedia article translations from MDWiki into multiple target languages.

### Main Modules and Components

| Module       | Purpose                                                                                                 |
| ------------ | ------------------------------------------------------------------------------------------------------- |
| `core/`      | Entry points (`fix_one_page`, `DoChangesToText1`) and settings loader                                   |
| `bots/`      | Individual transformation functions: ref expansion, deduplication, dot-moving, image fixing, mini-fixes |
| `lang_bots/` | Language-specific processing for Bulgarian, Spanish, Armenian, Polish, Portuguese, Swahili              |
| `parsers/`   | Low-level wikitext parsers for `<ref>` tags and category links                                          |
| `infobox/`   | Infobox template expansion and formatting                                                               |
| `mdwiki/`    | MDWiki category integration via Wikidata API                                                            |
| `utils/`     | HTTP client and debug utilities                                                                         |
| `resources/` | Local JSON data files and cached revisions                                                              |

### Technologies and Dependencies

-   **Python 3.10+** with type hints
-   **wikitextparser** - MediaWiki wikitext parsing
-   **requests** - HTTP client for API calls
-   **python-dotenv** - Environment variable loading
-   **hatchling** - Build system
-   **pytest** - Testing framework
-   **ruff/black/isort** - Code formatting and linting
-   **mypy** - Static type checking

---

## Architecture & Code Quality Review

### Code Organization

The project follows a layered architecture:

```
fix_page.py (orchestration)
    ├── bots/ (transformations)
    │   ├── mini_fixes.py
    │   ├── fix_missing_refs.py
    │   ├── remove_duplicate_refs.py
    │   ├── move_dots.py
    │   └── ...
    ├── lang_bots/ (language-specific)
    │   ├── es/ (Spanish - most complex)
    │   ├── bg_bot.py
    │   ├── hy_bot.py
    │   └── ...
    ├── parsers/ (low-level parsing)
    ├── infobox/ (template expansion)
    └── utils/ (HTTP, debug)
```

**Pipeline pattern**: `fix_one_page()` applies transformations in a deterministic order, making the processing flow clear and predictable.

### Design Patterns

-   **Pipeline pattern** in `fix_one_page()` for sequential transformations
-   **Strategy pattern** for language-specific bots dispatched via `apply_language_fixes()`
-   **Dataclass** (`Citation`) for structured reference representation
-   **LRU caching** for settings and image existence checks
-   **Facade pattern** with `fix_one_page()` as the unified entry point

### Maintainability

-   Each bot module is self-contained with a single responsibility
-   Language bots are isolated per language, making it easy to add new languages
-   The Spanish module (`es/`) is well-decomposed into data, helpers, refs, and section processing

### Readability

-   Functions generally have docstrings with Args/Returns sections
-   Module-level docstrings describe purpose
-   Variable names are generally descriptive (though some legacy short names remain)

### Scalability Considerations

-   LRU caches on settings and image checks reduce repeated API calls
-   Processing is stateless per page, enabling parallel batch processing
-   Local file fallbacks for API calls support offline development

---

## Strengths

1. **Clear pipeline architecture** - The `fix_one_page()` function provides a clean, auditable processing sequence
2. **Good modular decomposition** - Each bot has a focused responsibility
3. **Language extensibility** - Adding a new language only requires creating a new bot module and registering it in `lang_bots/__init__.py`
4. **Robust error handling** in HTTP utilities - Graceful fallbacks on API failures
5. **Defensive image checking** - Returns `True` on API failure to avoid removing valid images
6. **Comprehensive test suite** - Tests organized to mirror source structure
7. **Modern Python tooling** - pyproject.toml, ruff, black, mypy, isort all configured
8. **Citation dataclass** - Clean abstraction over wikitextparser's tag objects
9. **Fallback strategy** - Local JSON files as fallback when server is unavailable

---

## Weaknesses

### Code Duplication

1. **`str_ends_with` / `str_starts_with`** are duplicated in `refs_utils.py` and `hy_bot.py` - these are trivial wrappers around built-in `str.endswith()` / `str.startswith()`
2. **`start_end()`** function is duplicated in `pt_bot.py` and `es_helpers.py`
3. **`remove_short_refs()`** is duplicated in `es_refs.py` and `es_helpers.py`
4. **Month translation logic** is nearly identical between `fix_pt_months_in_refs()` and `fix_es_months_in_refs()`

### Poor Organization

1. **`refs_utils.py`** contains only trivial string helper functions (`str_ends_with`, `str_starts_with`) that add no value over built-in methods
2. **`remove_space.py`** in `lang_bots/` contains `print()` debug statements left in production code
3. The `es/` submodule uses inconsistent relative import depths (`...utils.debug` vs `..bots.months`)

### Code Quality Issues

1. **`apply_language_fixes()`** uses `if`/`elif` chain but starts with `if lang == "pl"` then switches to `elif` - the first condition should be `if` or all should be `elif`
2. **`DoChangesToText1()`** naming violates Python conventions (PascalCase for a function)
3. **`expend_infobox`** is a misspelling - should be `expand_infobox` (appears in function names and parameter names throughout)
4. **`expand = ... or True`** in `core/__init__.py` line 14 - the `or True` makes the setting always `True`, rendering the configuration useless
5. **Mixed use of `@dataclass` and `__init__`** in `Citation` class - the `@dataclass` decorator is imported but the class defines its own `__init__`, making the decorator pointless
6. **`remove_space.py`** has bare `print()` calls (lines 28, 36, 51, 58, 65) that should use the debug utilities

### Technical Debt

1. The `Citation.copy_object()` method re-parses the string representation to create a copy - a workaround for wikitextparser's limitations
2. Several functions accept `Any` types where specific types would be safer
3. `find_mdwiki_revid()` uses string concatenation for file paths instead of `pathlib`
4. Inconsistent parameter naming: `expend_infobox` vs `expand` vs `expend`

---

## Critical Issues

### Potential Bugs

1. **`expand = bool(int(...)) or True`** (`core/__init__.py:14`) - This expression always evaluates to `True`, meaning the `expend` language setting is completely ignored. This is likely a bug.

2. **`apply_language_fixes()` logic error** (`lang_bots/__init__.py:14-31`) - The first condition uses `if` but subsequent ones use `elif`. If `lang == "pl"`, the function runs `pl_fixes()` but then skips all `elif` branches. However, if `lang != "pl"`, the first `if` fails and the `elif` chain starts. This means `pl_fixes()` runs correctly, but the control flow is misleading and fragile.

3. **String replacement race condition** (`remove_duplicate_refs.py:55`) - Using `str.replace()` to swap citation text can fail if one citation's text is a substring of another's.

4. **`es_refs.py:68`** - `x.string = asas` modifies the parsed object's string directly, which may cause index shifting issues in subsequent iterations.

### Performance Bottlenecks

1. **Repeated `wtp.parse()` calls** - The same text is parsed multiple times across different bots (mini_fixes, remove_duplicate_refs, add_lang_en, etc.). Each parse creates a full AST.
2. **`remove_missing_infobox_images()`** makes HTTP requests in a loop without connection pooling or batch API calls.

### Unsafe Practices

1. **`settings.py:19`** - Hardcoded `http://localhost:9001` URL for development - could accidentally be used in production if `SERVER_NAME` is misconfigured
2. **Bare `except Exception`** in `config.py:9` and `http.py:32` swallows all errors silently

---

## Areas That Need Attention

### Missing Files

-   No `__init__.py` in `lang_bots/es/` subdirectories (though it exists at the es level)
-   No `py.typed` marker file for PEP 561 compliance
-   No `.github/` CI/CD configuration
-   No `CHANGELOG.md`

### Missing Documentation

-   No API documentation beyond docstrings
-   No architecture decision records
-   No contribution guidelines
-   No documentation for the processing pipeline order and its rationale

### Lack of Tests

-   No tests for `utils/http.py` (HTTP client)
-   No tests for `utils/debug.py`
-   No tests for `config.py`
-   No tests for `settings.py`
-   No integration tests that verify the full pipeline end-to-end
-   No property-based tests for regex-heavy functions

### Outdated Dependencies

-   `wikitextparser>=0.55.0` - check for latest version compatibility
-   Python target version in tooling config (`py313`) vs `requires-python` (`>=3.10`) mismatch

### Configuration Issues

-   `pyproject.toml` declares `license = { text = "MIT" }` but classifiers say `GPLv3+` - contradictory licensing
-   `target-version = "py313"` in ruff config but `requires-python = ">=3.10"` in project metadata

---

## Improvement Plan

### Quick Wins (1-2 days)

1. **Fix the `or True` bug** in `core/__init__.py:14` - change to `expand = bool(int(lang_default.get("expend", 1)))`
2. **Remove duplicate utility functions** - delete `str_ends_with`/`str_starts_with` wrappers, use built-ins directly
3. **Replace `print()` with `echo_debug()`** in `remove_space.py`
4. **Fix `apply_language_fixes()` control flow** - use consistent `if`/`elif` pattern
5. **Fix license inconsistency** in pyproject.toml (MIT vs GPLv3+)
6. **Fix `expend` typo** - rename to `expand` throughout

### Medium-term Improvements (1-2 weeks)

1. **Consolidate duplicate code** in `es_helpers.py` and `es_refs.py` (shared `remove_short_refs`, `start_end`)
2. **Extract month translation** into a shared utility with language-specific mappings
3. **Add integration tests** for the full `fix_one_page()` pipeline
4. **Add HTTP utility tests** with mocked responses
5. **Implement wikitext parse caching** to avoid re-parsing the same text
6. **Add `py.typed` marker** for PEP 561
7. **Standardize error handling** - use logging module instead of debug flags

### Long-term Refactoring (1-2 months)

1. **Replace string-based ref manipulation** with AST-based operations throughout
2. **Add batch API calls** for Commons image existence checking
3. **Implement plugin architecture** for language bots to support dynamic registration
4. **Add type stubs** for wikitextparser
5. **Create CI/CD pipeline** with automated testing, linting, and publishing
6. **Add property-based testing** (hypothesis) for regex transformations

---

## Comprehensive Review

| Metric                   | Score      | Notes                                                                                       |
| ------------------------ | ---------- | ------------------------------------------------------------------------------------------- |
| **Overall Rating**       | 6.5/10     | Functional and well-structured, but has notable bugs and code duplication                   |
| **Production Readiness** | Moderate   | Core pipeline works but has the `or True` bug and missing error handling                    |
| **Technical Debt**       | Medium     | Duplicate code, inconsistent naming, debug prints in production code                        |
| **Risk Assessment**      | Medium-Low | The `or True` bug silently ignores configuration; string replacement could corrupt wikitext |
| **Maintainability**      | 7/10       | Good modular structure, but duplicated code and inconsistent patterns add friction          |
| **Test Coverage**        | 6/10       | Good test structure, but missing coverage for HTTP, config, and integration scenarios       |
| **Code Quality**         | 6/10       | Generally clean, but debug prints, trivial wrappers, and naming issues detract              |
