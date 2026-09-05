# fix_refs/tests - Test Suite

## Project Overview

The `tests/` directory contains the pytest-based test suite for the fix_refs library. Tests are organized to mirror the source code structure, with subdirectories for each module.

### Test Structure

| Directory                     | Tests For                  | Test Files                                                                                                      |
| ----------------------------- | -------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `core/`                       | `fix_page.py` pipeline     | `test_fix_refs.py`, `test_fix_page.py`, `test_fix_page_files.py`, `test_index.py`                               |
| `bots/mini_fixes/`            | `mini_fixes.py`            | `test_bots_mini_fixes.py`, `test_mini_fixes.py`                                                                 |
| `bots/fix_missing_refs/`      | `fix_missing_refs.py`      | `test_missing_refs.py`                                                                                          |
| `bots/remove_duplicate_refs/` | `remove_duplicate_refs.py` | `test_bots_remove_duplicate_refs.py`                                                                            |
| `bots/move_dots/`             | `move_dots.py`             | `test_move_dots.py`                                                                                             |
| `bots/add_lang_en_bot/`       | `add_lang_en_bot.py`       | `test_bots_add_lang_en.py`                                                                                      |
| `bots/expend_refs/`           | `expend_refs.py`           | `test_bots_expend_refs.py`                                                                                      |
| `bots/months/`                | `months.py`                | `test_months.py`                                                                                                |
| `bots/fix_images/`            | `fix_images.py`            | `test_fix_images.py`                                                                                            |
| `infobox/`                    | `expend_infobox.py`        | `test_do_comments.py`, `test_infobox2.py`, `test_infobox_expend_infobox.py`, `test_infobox_expend_infobox_2.py` |
| `lang_bots/es/`               | Spanish bots               | `test_lang_bots_es.py`, `test_lang_bots_es_additional.py`, `test_lang_bots_es_section.py`, `test_mv_es_refs.py` |
| `lang_bots/bg_bot/`           | Bulgarian bot              | `test_bulgarian_bot.py`, `test_lang_bots_bg.py`                                                                 |
| `lang_bots/hy_bots/`          | Armenian bot               | `test_armenian_bot.py`, `test_lang_bots_hy.py`, `test_remove_spaces_between_ref_and_punctuation.py`             |
| `lang_bots/pl_bots/`          | Polish bot                 | `test_pl_bot.py`, `test_polish_bot.py`                                                                          |
| `lang_bots/pt_bots/`          | Portuguese bot             | `test_lang_bots_pt.py`, `test_pt_months_new_value.py`                                                           |
| `lang_bots/sw_bot/`           | Swahili bot                | `test_lang_bots_sw.py`, `test_swahili_bot.py`                                                                   |
| `lang_bots/remove_space/`     | `remove_space.py`          | `test_files.py`, `test_remove_space.py`, `test_remove_space_part_2.py`                                          |
| `parsers/`                    | Parsers                    | `test_citations.py`, `test_category.py`, `test_parsers_citations.py`, `test_parsers_category.py`                |
| `mdwiki/`                     | MDWiki integration         | `test_category_network.py`, `test_mdwiki_category.py`                                                           |

### Technologies

-   **pytest** - Test framework
-   **pytest-cov** - Coverage reporting
-   Test data files in `texts/` subdirectories

---

## Architecture & Code Quality Review

### Code Organization

Tests mirror the source structure, making it easy to find tests for any module. Test data files are stored in `texts/` subdirectories alongside test files.

### Design Patterns

-   **Class-based test organization** - Tests grouped into classes by functionality
-   **Fixture-based setup** - `conftest.py` adds project root to `sys.path`
-   **Data-driven tests** - Test data loaded from external files

### Maintainability

Good structure. The mirroring convention makes it intuitive to find and add tests.

### Readability

Test names are descriptive. Assertions use clear comparisons.

---

## Strengths

1. **Comprehensive structure** - Tests mirror source code organization
2. **Class-based grouping** - Related tests are grouped logically
3. **External test data** - Complex test inputs stored in files, not inline
4. **Good naming conventions** - Test files follow `test_*.py` pattern consistently

---

## Weaknesses

### Missing Test Coverage

No tests exist for:

-   `utils/http.py` - HTTP client (mocking needed)
-   `utils/debug.py` - Debug utilities
-   `config.py` - Configuration/path setup
-   `core/settings.py` - Settings loading
-   `mdwiki/category.py` network behavior (only local file tests)

### Test Configuration Issues

1. **`conftest.py`** modifies `sys.path` directly instead of using pytest's built-in path management or `pip install -e .`
2. **No `conftest.py` in subdirectories** - No shared fixtures for common test patterns

### Test Data Management

-   Test data files in `texts/` directories are not documented
-   No clear naming convention for test data files
-   Some test directories have `texts/` while others don't

### Duplicate Test Files

Some modules have multiple test files that could be consolidated:

-   `test_bots_mini_fixes.py` and `test_mini_fixes.py`
-   `test_citations.py` and `test_parsers_citations.py`
-   `test_category.py` and `test_parsers_category.py`

---

## Critical Issues

1. **No HTTP mocking** - `utils/http.py` is untested. API-dependent features (image checking, settings loading) have no test coverage.
2. **No integration tests** - No end-to-end tests that verify the full `fix_one_page()` pipeline with realistic inputs.

---

## Areas That Need Attention

-   Add tests for `utils/http.py` with mocked responses
-   Add tests for `core/settings.py`
-   Add integration tests for the full pipeline
-   Consolidate duplicate test files
-   Add fixtures for common test patterns (e.g., creating Citation objects)
-   Document test data files

---

## Improvement Plan

### Quick Wins

1. Add basic tests for `utils/debug.py`
2. Consolidate duplicate test files
3. Add docstrings to test classes

### Medium-term

1. Add HTTP tests with `pytest-mock` or `responses` library
2. Add integration tests for the full pipeline
3. Create shared fixtures in subdirectory `conftest.py` files
4. Add tests for `core/settings.py`

### Long-term

1. Add property-based tests for regex transformations (hypothesis)
2. Add performance benchmarks for batch processing
3. Set up CI with coverage thresholds

---

## Comprehensive Review

| Metric                   | Score    | Notes                                                                 |
| ------------------------ | -------- | --------------------------------------------------------------------- |
| **Overall Rating**       | 6.5/10   | Good structure but missing coverage for HTTP, config, and integration |
| **Production Readiness** | Moderate | Core transformations tested, but gaps in utility coverage             |
| **Technical Debt**       | Medium   | Duplicate test files, missing coverage                                |
| **Risk Assessment**      | Medium   | Untested HTTP and settings code could have hidden bugs                |
| **Maintainability**      | 7/10     | Good mirroring convention, but some consolidation needed              |
