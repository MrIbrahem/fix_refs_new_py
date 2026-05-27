# Project Audit Report — fix_refs

**Project:** fix_refs — MediaWiki Reference Fixer
**Version:** 0.1.0 (Beta)
**Audit Date:** 2026-05-27
**Auditor:** Senior Software Architect (automated)
**Scope:** Full codebase analysis of all Python modules, tests, configuration, and infrastructure
**Test Status:** 407 passed, 2 deselected

---

## Executive Summary

### Overall Purpose

fix_refs is a Python library that parses and fixes references (citations) in MediaWiki wikitext. It serves WikiProjectMed's Translation Dashboard, processing Wikipedia article translations from MDWiki into six target languages: Spanish, Portuguese, Bulgarian, Armenian, Polish, and Swahili.

The main entry point `fix_one_page()` applies a 10-step transformation pipeline: redirect detection, infobox expansion, whitespace cleanup, reference expansion from source, deduplication, dot-moving, language tagging, language-specific fixes, category injection, and post-fix cleanup.

### Main Technologies

| Technology | Role |
|---|---|
| Python 3.10+ | Runtime |
| wikitextparser | AST-based wikitext parsing |
| requests | HTTP client for Wikimedia/Commons/Wikidata APIs |
| python-dotenv | Environment configuration |
| hatchling | Build system |
| pytest | Testing framework (407 tests) |
| ruff / black / isort | Code formatting and linting |
| mypy / pylint | Static analysis |

### General Architecture

```
fix_one_page() orchestrator (core/fix_page.py)
    ├── Infobox expansion (infobox/)
    ├── General bots (bots/) — whitespace, ref expansion, deduplication, dot-moving, image validation
    ├── Language-specific bots (lang_bots/) — template translation, locale formatting
    ├── Low-level parsers (parsers/) — Citation dataclass, category parsing
    ├── External integrations (mdwiki/) — Wikidata category fetching
    └── Utilities (utils/) — HTTP client, debug output
```

Each bot is a stateless pure function: text in, text out. The pipeline is deterministic and serial.

---

## Project Health Assessment

| Dimension | Rating | Summary |
|---|---|---|
| **Overall Code Quality** | 6.5/10 | Functional and well-structured, but has a configuration-ignoring bug, code duplication, and naming issues |
| **Maintainability** | 7/10 | Good modular decomposition; duplication and naming inconsistencies add friction |
| **Scalability** | 6/10 | Stateless design enables parallel processing; repeated `wtp.parse()` calls are a bottleneck |
| **Security Posture** | 7/10 | Proper User-Agent, timeouts, and HTTPS; bare `except Exception` removed; hardcoded localhost remains |
| **Production Readiness** | 6.5/10 | Core pipeline works; configuration bug and missing CI/CD are blockers |

### Per-Module Ratings

| Module | Score | Key Concern |
|---|---|---|
| `core/` | 7/10 | `or True` bug ignores configuration (see Critical Findings) |
| `bots/` | 7/10 | Trivial wrapper functions, `str.replace()` fragility |
| `lang_bots/` | 7/10 | Dispatcher flow fixed; debug prints fixed |
| `lang_bots/es/` | 7.5/10 | Best-structured module; minor duplication remains |
| `parsers/` | 7/10 | Unused `@dataclass`, `get_attributes()` improved but still string-based |
| `infobox/` | 5.5/10 | Cryptic variable names, missing docstrings, fragile template selection heuristic |
| `mdwiki/` | 7/10 | Skip lists consolidated; `import re` moved to module level |
| `utils/` | 7/10 | Bare `except Exception` removed; should adopt `logging` module |
| `resources/` | 5/10 | Cached data in git, no format documentation |
| `tests/` | 6.5/10 | Good structure; missing HTTP, config, and integration coverage |

---

## Cross-Project Analysis

### Shared Architectural Patterns

1. **Pipeline pattern** — `fix_one_page()` applies 10 sequential transformations. Consistent and auditable.
2. **Pure function design** — All bots are stateless (text in, text out), enabling easy testing and composition.
3. **Data-driven transformation** — Spanish bot uses lookup tables (`REFS_TEMPS`, `ARGS_TO`) for template/parameter mapping, separating data from logic.
4. **Fallback strategy** — API calls fall back to local JSON files for offline development.
5. **LRU caching** — Used for settings and image existence checks.
6. **Dispatcher routing** — `apply_language_fixes()` routes to language-specific bots via `if`/`elif` chain (now consistent after fix).

### Repeated Weaknesses

| Weakness | Occurrences | Files Affected |
|---|---|---|
| `str_ends_with` / `str_starts_with` trivial wrappers | 2 | `bots/refs_utils.py`, `lang_bots/hy_bot.py` |
| `start_end()` duplication | 2 | `lang_bots/pt_bot.py`, `lang_bots/es/es_helpers.py` |
| `remove_short_refs()` duplication | 2 | `lang_bots/es/es_refs.py`, `lang_bots/es/es_helpers.py` |
| Month translation logic duplication | 2 | `bots/months.py` (via `es_helpers.py` and `pt_bot.py`) |
| "expend" typo (should be "expand") | 8+ | `expend_refs.py`, `expend_infobox.py`, parameter names throughout |
| String-based wikitext manipulation | 4+ | `remove_duplicate_refs.py`, `expend_refs.py`, `es_bot.py`, `expend_infobox.py` |

### Common Technical Debt

1. **Naming violations** — `DoChangesToText1()` (PascalCase function), `expend_infobox` (misspelling), inconsistent parameter naming.
2. **String-based wikitext manipulation** — Several bots use `str.replace()` instead of AST-based operations, risking substring corruption.
3. **Missing type annotations** — Multiple functions lack parameter and return type hints (`apply_language_fixes`, `expend_new`, `match_it`, etc.).
4. **Dead code** — Commented-out code in `remove_duplicate_refs.py` and `expend_infobox.py`.
5. **Global mutable state** — `DEBUG` and `TEST_MODE` in `utils/debug.py` are module-level globals.

### Dependency Issues

| Issue | Detail | Status |
|---|---|---|
| `python-dotenv` not in pyproject.toml | Listed in `requirements.txt` and imported in `config.py` but missing from `[project.dependencies]` | **Unfixed** |
| Python version mismatch | Tooling targets `py313` but `requires-python = ">=3.10"` | **Unfixed** |
| License inconsistency | Was MIT in `pyproject.toml` vs GPLv3+ in classifiers | **Fixed** — now `GPL-3.0-or-later` |
| Cached revisions in git | `resources/revisions/` bloats the repository | **Unfixed** |

### Integration Concerns

1. **Wikidata API** — No caching on `get_cats()`, makes HTTP call every time.
2. **Commons API** — Image existence checks are per-image in a loop without batch support or connection pooling.
3. **MDWiki API** — Hardcoded `http://localhost:9001` in `settings.py` could leak into production.
4. **`DoChangesToText1()` type safety** — Accepts `mdwiki_revid: int|str` without normalization.

---

## Critical Findings

### Active Bugs

| # | Issue | Location | Severity | Status |
|---|---|---|---|---|
| 1 | `or True` makes expand setting always `True` | `core/__init__.py:14` | **Critical** | **UNFIXED** — configuration is silently ignored |
| 2 | String replacement can corrupt wikitext | `bots/remove_duplicate_refs.py:55` | **High** | **UNFIXED** — `str.replace()` matches substrings |
| 3 | In-place modification during iteration | `lang_bots/es/es_refs.py:68` | **High** | **UNFIXED** — modifying tag strings while iterating |

### Previously Fixed Issues

| # | Issue | Location | Fix Applied |
|---|---|---|---|
| 1 | Debug `print()` in production code | `lang_bots/remove_space.py` | Replaced with `echo_debug()` |
| 2 | Dispatcher control flow bug | `lang_bots/__init__.py` | Fixed to consistent `if`/`elif` chain |
| 3 | Bare `except Exception` swallows errors | `utils/http.py` | Removed; only specific exceptions caught |
| 4 | `get_attributes()` fragile `>` splitting | `parsers/citations.py` | Rewritten to find first `>` after `<ref` |
| 5 | License inconsistency (MIT vs GPLv3+) | `pyproject.toml` | Changed to `GPL-3.0-or-later` |
| 6 | Inconsistent skip lists | `mdwiki/category.py` | Consolidated to `SKIP_LANGS_CATEGORY` constant |
| 7 | `import re` inside function | `mdwiki/category.py` | Moved to module top |

### Security Vulnerabilities

| # | Vulnerability | Location | Risk | Status |
|---|---|---|---|---|
| 1 | Hardcoded localhost URL | `settings.py:19` | Could be used if `SERVER_NAME` is misconfigured | **Unfixed** |
| 2 | No URL validation on HTTP requests | `utils/http.py` | SSRF risk if URLs come from untrusted sources | **Unfixed** |
| 3 | No JSON schema validation | Multiple `json.load()` calls | Malformed API responses cause silent failures | **Unfixed** |

### Performance Bottlenecks

| # | Bottleneck | Location | Impact |
|---|---|---|---|
| 1 | Repeated `wtp.parse()` calls | All bots | Same text parsed up to 6 times per `fix_one_page()` call |
| 2 | Non-compiled regex patterns | `bots/mini_fixes.py`, multiple files | Patterns compiled on every function call |
| 3 | Uncached API calls in loops | `bots/fix_images.py` | Per-image HTTP requests without connection pooling |

### Missing Infrastructure

| Missing Item | Impact |
|---|---|
| No CI/CD pipeline | No automated testing, linting, or deployment |
| No `.github/` configuration | No issue templates, PR workflows, or Actions |
| No `CHANGELOG.md` | No release history tracking |
| No `py.typed` marker | PEP 561 non-compliant |
| No integration tests | Full pipeline behavior untested end-to-end |
| No HTTP mocking in tests | `utils/http.py` and API-dependent code untested |

---

## Strengths

### Strong Engineering Decisions

1. **Pipeline architecture** — The 10-step sequential pipeline in `fix_one_page()` is clear, auditable, and easy to extend. Each step is a single function call with visible parameters.

2. **Pure function design** — All bots are stateless text transformers. This makes them easy to test, compose, and reason about. No hidden state or side effects.

3. **Safety fallback** — `fix_page.py:81-82` returns original text if the pipeline produces empty output, preventing data loss.

4. **Defensive image checking** — `fix_images.py` returns `True` on API failure to avoid removing valid images. Fail-open is the correct default for content preservation.

5. **Settings caching** — `lru_cache(maxsize=1)` on `load_settings()` prevents repeated file/API reads across calls.

### Reusable Components

1. **`Citation` dataclass** — Clean abstraction over wikitextparser's `Tag` object with accessor methods for name, content, attributes, and short/full classification.

2. **Spanish bot data tables** — `es_data.py` contains 29 template name translations and 50+ parameter translations, cleanly separated from processing logic.

3. **HTTP utility** — `utils/http.py` provides a reusable HTTP client with proper User-Agent compliance for Wikimedia APIs, appropriate timeouts, and specific exception handling.

4. **Month translation** — `bots/months.py` handles English-to-Portuguese/Spanish date conversion with multiple format patterns.

### Well-Structured Modules

1. **`lang_bots/es/`** — The Spanish subpackage is the best-structured module: data/logic separation, focused sub-modules (data, helpers, refs, section), and clear entry points.

2. **`parsers/`** — Clean two-file structure with the `Citation` class providing a stable API over wikitextparser internals.

3. **`mdwiki/`** — Simple, focused module with robust fallback strategy (API with local file fallback).

### Good Development Practices

1. **Modern tooling** — `pyproject.toml`, hatchling, ruff, black, mypy, isort all configured with consistent 120-char line length.
2. **Test structure mirrors source** — Tests organized to match source tree, making it intuitive to find and add tests.
3. **External test data** — Complex test inputs stored in files, not inline.
4. **407 passing tests** — Comprehensive test suite runs in under 1 second.

---

## Improvement Roadmap

### Immediate Fixes (1-2 days)

| # | Fix | File | Effort |
|---|---|---|---|
| 1 | **Remove `or True` from expand setting** | `core/__init__.py:14` | 5 min |
| 2 | Remove trivial wrapper functions (`str_ends_with`, `str_starts_with`) | `bots/refs_utils.py`, `lang_bots/hy_bot.py` | 30 min |
| 3 | Add `python-dotenv` to `pyproject.toml` dependencies | `pyproject.toml` | 5 min |
| 4 | Rename `DoChangesToText1()` to PEP 8 compliant name | `core/__init__.py` + callers | 30 min |
| 5 | Remove unused `@dataclass` from `Citation` | `parsers/citations.py` | 10 min |

### Short-Term Improvements (1-2 weeks)

| # | Improvement | Scope | Effort |
|---|---|---|---|
| 1 | Consolidate duplicated functions (`start_end`, `remove_short_refs`, month translation) | `lang_bots/` | 2 hours |
| 2 | Fix "expend" to "expand" typo throughout codebase | All files | 1 hour |
| 3 | Replace `str.replace()` with AST-based operations for ref manipulation | `remove_duplicate_refs.py`, `expend_refs.py` | 4 hours |
| 4 | Add missing type annotations to key functions | Multiple files | 4 hours |
| 5 | Add `logging` module integration replacing `echo_debug()`/`echo_test()` | `utils/debug.py` | 2 hours |
| 6 | Add `.gitignore` for `resources/revisions/` | Root | 5 min |
| 7 | Remove dead code and commented-out code | Multiple files | 1 hour |

### Medium-Term Improvements (1-2 months)

| # | Improvement | Scope | Effort |
|---|---|---|---|
| 1 | Add integration tests for full `fix_one_page()` pipeline | `tests/` | 1 week |
| 2 | Add HTTP tests with mocked responses | `tests/` | 3 days |
| 3 | Implement wikitext parse caching (parse once, pass AST to all bots) | `core/fix_page.py` | 1 week |
| 4 | Pre-compile regex patterns at module level | Multiple bot files | 2 days |
| 5 | Use `requests.Session` for connection pooling | `utils/http.py` | 1 day |
| 6 | Add batch Commons API calls for image checking | `bots/fix_images.py` | 1 week |
| 7 | Create CI/CD pipeline (GitHub Actions) | `.github/` | 2 days |
| 8 | Add `py.typed` marker for PEP 561 | Root | 5 min |

### Security Hardening Priorities

| # | Priority | Action |
|---|---|---|
| 1 | Remove hardcoded `localhost` URL from `settings.py` | Replace with environment-only configuration |
| 2 | Add URL validation to `get_url()`/`get_url_json()` | Restrict to known Wikimedia domains |
| 3 | Add JSON schema validation for external API responses | Prevent malformed data from propagating |
| 4 | Add timeout configuration | Currently hardcoded at 5s; make configurable |

### DevOps and Testing Recommendations

| # | Recommendation | Priority |
|---|---|---|
| 1 | Set up GitHub Actions with `pytest` + `ruff check` + `mypy` | High |
| 2 | Add coverage thresholds (target: 80%+) | High |
| 3 | Add pre-commit hooks for formatting and linting | Medium |
| 4 | Add property-based tests (hypothesis) for regex transformations | Medium |
| 5 | Add performance benchmarks for batch processing | Low |
| 6 | Add `CHANGELOG.md` and semantic versioning | Low |

---

## Final Evaluation

### Scoring

| Metric | Score | Notes |
|---|---|---|
| **Overall Project Score** | **6.5/10** | Functional and well-architected at module level, but has a critical configuration bug, notable code duplication, and missing infrastructure |
| **Risk Level** | **Medium** | The `or True` bug silently overrides configuration; string replacement could corrupt wikitext on edge cases |
| **Technical Debt Level** | **Medium** | Duplicate code, inconsistent naming, missing type annotations |
| **Estimated Production Readiness** | **70%** | Core pipeline works for common cases; configuration bug and lack of CI/CD are blockers |
| **Maintainability** | **7/10** | Strong modular isolation; duplication and naming add friction |
| **Test Coverage** | **6/10** | 407 tests with good structure; missing HTTP, config, settings, and integration tests |

### Summary Verdict

fix_refs is a **functional and well-designed library** with a clear pipeline architecture and good modular decomposition. The pure-function bot design and data-driven Spanish processing are strong engineering choices. The codebase shows signs of organic growth — duplication has accumulated, naming conventions have drifted, and a configuration bug has persisted.

Several critical issues from the initial audit have been **fixed**: debug print statements replaced with `echo_debug()`, dispatcher control flow corrected, bare `except Exception` removed, license inconsistency resolved, and inconsistent skip lists consolidated.

The **highest-priority remaining issue** is the `or True` bug at `core/__init__.py:14` which silently ignores the `expend` configuration setting. This is a one-line fix with high impact.

### Recommended Next Steps (Priority Order)

1. **Fix the `or True` bug** — Remove `or True` from `core/__init__.py:14`. One character, high impact.
2. **Add `python-dotenv` to pyproject.toml** — Prevents `pip install` failures.
3. **Set up CI/CD** — Even a minimal `pytest` + `ruff check` GitHub Actions workflow prevents regressions.
4. **Consolidate duplicate functions** — Start with `start_end()` and `remove_short_refs()`.
5. **Add integration tests** — Verify the full pipeline with realistic multi-language inputs.
6. **Address `str.replace()` fragility** — Audit all wikitext string replacements for substring collision risk.

With these fixes, the project would move from **6.5/10 to approximately 8/10** and be suitable for reliable production deployment.

---

*End of Report*
