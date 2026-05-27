# Comprehensive Project Audit Report

**Project:** fix_refs — MediaWiki Reference Fixer
**Version:** 0.1.0 (Beta)
**Audit Date:** 2026-05-27
**Auditor:** Automated Code Audit
**Scope:** Full codebase analysis across all modules, tests, configuration, and infrastructure

---

## Executive Summary

### Overall Purpose

fix_refs is a Python library that parses and fixes references (citations) in MediaWiki wikitext. It was built for WikiProjectMed's Translation Dashboard to process Wikipedia article translations from MDWiki into six target languages (Spanish, Portuguese, Bulgarian, Armenian, Polish, Swahili). The library applies a 10-step transformation pipeline to normalize references, translate templates, fix formatting, and add metadata.

### Main Technologies

| Technology | Role |
|---|---|
| Python 3.10+ | Runtime |
| wikitextparser | AST-based wikitext parsing |
| requests | HTTP client for Wikimedia/Commons/Wikidata APIs |
| python-dotenv | Environment configuration |
| hatchling | Build system |
| pytest | Testing framework |
| ruff / black / isort | Code formatting and linting |
| mypy / pylint | Static analysis |

### General Architecture Overview

The system follows a layered pipeline architecture:

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
| **Overall Code Quality** | 6.5/10 | Functional and well-structured, but has notable bugs, code duplication, and debug artifacts |
| **Maintainability** | 7/10 | Good modular decomposition; duplication and naming issues add friction |
| **Scalability** | 7/10 | Stateless design enables parallel processing; repeated parsing is a bottleneck |
| **Security Posture** | 5/10 | Bare `except Exception`, no URL validation, no input sanitization |
| **Production Readiness** | 6/10 | Core pipeline works; configuration bug and missing error handling are blockers |

### Per-Module Ratings

| Module | Score | Key Concern |
|---|---|---|
| `core/` | 7/10 | `or True` bug ignores configuration |
| `bots/` | 7/10 | Trivial wrapper functions, minor duplication |
| `lang_bots/` | 7/10 | Debug `print()` in production code |
| `lang_bots/es/` | 7.5/10 | Best-structured; minor duplication |
| `parsers/` | 7/10 | Unused `@dataclass`, fragile string parsing |
| `infobox/` | 5.5/10 | Cryptic variable names, missing docs, fragile heuristics |
| `mdwiki/` | 7/10 | Inconsistent skip lists |
| `utils/` | 7/10 | Bare `except Exception`, print-based debugging |
| `resources/` | 5/10 | Cached data in git, no documentation |
| `tests/` | 6.5/10 | Good structure; missing HTTP, config, and integration coverage |

---

## Cross-Project Analysis

### Shared Architectural Patterns

1. **Pipeline pattern** — `fix_one_page()` applies 10 sequential transformations. Consistent and auditable.
2. **Pure function design** — All bots are stateless (text in → text out), enabling easy testing and composition.
3. **Data-driven transformation** — Spanish bot uses lookup tables (`REFS_TEMPS`, `ARGS_TO`) for template/parameter mapping, separating data from logic.
4. **Fallback strategy** — API calls fall back to local JSON files for offline development.
5. **LRU caching** — Used for settings and image existence checks.

### Repeated Weaknesses

| Weakness | Occurrences | Files Affected |
|---|---|---|
| `str_ends_with` / `str_starts_with` trivial wrappers | 2 | `bots/refs_utils.py`, `lang_bots/hy_bot.py` |
| `start_end()` duplication | 2 | `lang_bots/pt_bot.py`, `lang_bots/es/es_helpers.py` |
| `remove_short_refs()` duplication | 2 | `lang_bots/es/es_refs.py`, `lang_bots/es/es_helpers.py` |
| Month translation logic duplication | 2 | `bots/months.py` (via `es_helpers.py` and `pt_bot.py`) |
| Bare `except Exception` | 2+ | `config.py`, `utils/http.py` |
| Debug `print()` in production code | 5 | `lang_bots/remove_space.py` (lines 28, 36, 51, 58, 65) |
| "expend" typo (should be "expand") | 8+ | `expend_refs.py`, `expend_infobox.py`, parameter names throughout |

### Common Technical Debt

1. **Naming violations** — `DoChangesToText1()` (PascalCase function), `expend_infobox` (misspelling), inconsistent parameter naming.
2. **String-based wikitext manipulation** — Several bots use `str.replace()` instead of AST-based operations, risking substring corruption.
3. **Missing type annotations** — Multiple functions lack parameter and return type hints (`apply_language_fixes`, `expend_new`, `match_it`, etc.).
4. **Dead code** — `refs_to_name` populated but never used in `es_refs.py`; commented-out code in `remove_duplicate_refs.py` and `expend_infobox.py`.
5. **Global mutable state** — `DEBUG` and `TEST_MODE` in `utils/debug.py` are module-level globals.

### Dependency Issues

| Issue | Detail |
|---|---|
| License conflict | `pyproject.toml` declares `license = { text = "GPL-3.0-or-later" }` but README says MIT |
| Python version mismatch | Tooling targets `py313` but `requires-python = ">=3.10"` |
| `python-dotenv` not in dependencies | Listed in README but missing from `pyproject.toml` `[project.dependencies]` |
| Cached revisions in git | `resources/revisions/` bloats the repository |

### Integration Concerns

1. **Wikidata API** — No caching on `get_cats()`, makes HTTP call every time.
2. **Commons API** — Image existence checks are per-image in a loop without batch support or connection pooling.
3. **MDWiki API** — Hardcoded `http://localhost:9001` in `settings.py` could leak into production.

---

## Critical Findings

### High-Risk Issues

| # | Issue | Location | Severity | Impact |
|---|---|---|---|---|
| 1 | `or True` makes expand setting always `True` | `core/__init__.py:14` | **Critical** | Configuration is silently ignored; all languages always expand infoboxes regardless of settings |
| 2 | String replacement can corrupt wikitext | `bots/remove_duplicate_refs.py:55`, `bots/expend_refs.py:31` | **High** | `str.replace()` matches substrings; one citation's text could be a substring of another's |
| 3 | In-place modification during iteration | `bots/fix_images.py:129-171`, `lang_bots/es/es_refs.py:68` | **High** | Modifying parsed objects while iterating can cause index shifting and data corruption |
| 4 | Bare `except Exception` swallows errors | `config.py:9`, `utils/http.py:32,58` | **High** | Programming errors (TypeError, AttributeError) are silently caught, hiding bugs |

### Security Vulnerabilities

| # | Vulnerability | Location | Risk |
|---|---|---|---|
| 1 | No URL validation on HTTP requests | `utils/http.py` | SSRF if URLs come from untrusted sources |
| 2 | No JSON schema validation | Multiple files using `json.load()` | Malformed API responses could cause silent failures |
| 3 | Environment variable path injection | `config.py:15` | Path traversal if environment is compromised |
| 4 | Hardcoded localhost URL | `settings.py:19` | Could be used in production if `SERVER_NAME` is misconfigured |

### Performance Bottlenecks

| # | Bottleneck | Location | Impact |
|---|---|---|---|
| 1 | Repeated `wtp.parse()` calls | All bots | Same text parsed N times (once per bot); O(n) full AST constructions |
| 2 | Non-compiled regex patterns | `bots/mini_fixes.py`, multiple files | Patterns compiled on every function call instead of once at module level |
| 3 | String concatenation in loops | `lang_bots/es/es_refs.py:7-21` | Inefficient; should use `str.join()` |
| 4 | Uncached API calls in loops | `bots/fix_images.py` | Per-image HTTP requests without connection pooling |

### Stability Concerns

| # | Concern | Location |
|---|---|---|
| 1 | `Citation.copy_object()` re-parses string representation | `parsers/citations.py` |
| 2 | `Citation.get_attributes()` splits on `>` — breaks if ref content contains `>` | `parsers/citations.py` |
| 3 | Template selection heuristic (largest template = infobox) is fragile | `infobox/expend_infobox.py:130-146` |
| 4 | Inconsistent skip lists in mdwiki module | `mdwiki/category.py` |
| 5 | Dispatcher mixes `if`/`elif` inconsistently | `lang_bots/__init__.py:14-31` |

### Missing Infrastructure

| Missing Item | Impact |
|---|---|
| No CI/CD pipeline | No automated testing, linting, or deployment |
| No `.github/` configuration | No issue templates, PR workflows, or Actions |
| No `CHANGELOG.md` | No release history tracking |
| No `py.typed` marker | PEP 561 non-compliant; type checkers won't use inline types |
| No `conftest.py` in subdirectories | No shared test fixtures |
| No integration tests | Full pipeline behavior is untested end-to-end |
| No HTTP mocking in tests | `utils/http.py` and all API-dependent code is untested |

---

## Strengths

### Strong Engineering Decisions

1. **Pipeline architecture** — The 10-step sequential pipeline in `fix_one_page()` is clear, auditable, and easy to extend. Each step is visible and ordered.
2. **Pure function design** — All bots are stateless text transformers. This makes them easy to test, compose, and reason about.
3. **Safety fallback** — `fix_page.py:81-82` returns original text if the pipeline produces empty output, preventing data loss.
4. **Defensive image checking** — `fix_images.py` returns `True` on API failure to avoid removing valid images. Fail-open is the correct default for content preservation.
5. **Settings caching** — `lru_cache` on `load_settings()` prevents repeated file/API reads.

### Reusable Components

1. **`Citation` dataclass** — Clean abstraction over wikitextparser's `Tag` object with accessor methods for name, content, attributes, and short/full classification.
2. **Spanish bot data tables** — `es_data.py` contains 29 template name translations and 50+ parameter translations, cleanly separated from logic.
3. **HTTP utility** — `utils/http.py` provides a reusable HTTP client with proper User-Agent compliance for Wikimedia APIs.
4. **Language dispatcher** — `apply_language_fixes()` provides a simple, extensible routing mechanism for language-specific processing.

### Well-Structured Modules

1. **`lang_bots/es/`** — The Spanish subpackage is the best-structured module: data/logic separation, focused sub-modules (data, helpers, refs, section), and clear entry points.
2. **`parsers/`** — Clean two-file structure with the `Citation` class providing a stable API over wikitextparser internals.
3. **`mdwiki/`** — Simple, focused module with robust fallback strategy (API → local file).

### Good Development Practices

1. **Modern tooling** — pyproject.toml, hatchling, ruff, black, mypy, isort all configured.
2. **Test structure mirrors source** — Tests are organized to match the source tree, making it intuitive to find and add tests.
3. **External test data** — Complex test inputs are stored in files, not inline.
4. **120-character line length** — Consistently applied across all tooling.

---

## Improvement Roadmap

### Immediate Fixes (1-2 days)

| # | Fix | File | Effort |
|---|---|---|---|
| 1 | Remove `or True` from expand setting | `core/__init__.py:14` | 5 min |
| 2 | Replace `print()` with `echo_debug()` | `lang_bots/remove_space.py` | 15 min |
| 3 | Fix dispatcher to use consistent `if`/`elif` | `lang_bots/__init__.py:14-31` | 10 min |
| 4 | Remove trivial wrapper functions (`str_ends_with`, `str_starts_with`) | `bots/refs_utils.py`, `lang_bots/hy_bot.py` | 30 min |
| 5 | Fix license inconsistency (MIT vs GPLv3+) | `pyproject.toml` | 5 min |
| 6 | Add `python-dotenv` to dependencies | `pyproject.toml` | 5 min |
| 7 | Remove `@dataclass` from `Citation` class | `parsers/citations.py` | 10 min |
| 8 | Fix `get_attributes()` to use `self.ref.attrs` | `parsers/citations.py` | 15 min |

### Short-Term Improvements (1-2 weeks)

| # | Improvement | Scope | Effort |
|---|---|---|---|
| 1 | Consolidate duplicated functions (`start_end`, `remove_short_refs`, month translation) | `lang_bots/` | 2 hours |
| 2 | Fix "expend" → "expand" typo throughout codebase | All files | 1 hour |
| 3 | Rename `DoChangesToText1()` to PEP 8 compliant name | `core/fix_page.py` + callers | 30 min |
| 4 | Replace `str.replace()` with AST-based operations for ref manipulation | `bots/remove_duplicate_refs.py`, `bots/expend_refs.py` | 4 hours |
| 5 | Add missing type annotations to key functions | Multiple files | 4 hours |
| 6 | Replace bare `except Exception` with specific exception types | `config.py`, `utils/http.py` | 1 hour |
| 7 | Add `logging` module integration | `utils/debug.py` | 2 hours |
| 8 | Add `.gitignore` for `resources/revisions/` | Root | 5 min |
| 9 | Consolidate inconsistent skip lists into constants | `mdwiki/category.py` | 30 min |
| 10 | Remove dead code and commented-out code | Multiple files | 1 hour |

### Medium-Term Improvements (1-2 months)

| # | Improvement | Scope | Effort |
|---|---|---|---|
| 1 | Add integration tests for full `fix_one_page()` pipeline | `tests/` | 1 week |
| 2 | Add HTTP tests with mocked responses | `tests/` | 3 days |
| 3 | Implement wikitext parse caching (parse once, pass to bots) | `core/fix_page.py` | 1 week |
| 4 | Pre-compile regex patterns at module level | Multiple bot files | 2 days |
| 5 | Use `requests.Session` for connection pooling | `utils/http.py` | 1 day |
| 6 | Add batch Commons API calls for image checking | `bots/fix_images.py` | 1 week |
| 7 | Create CI/CD pipeline (GitHub Actions) | `.github/` | 2 days |
| 8 | Add `py.typed` marker for PEP 561 | Root | 5 min |
| 9 | Standardize error handling strategy (return empty vs raise vs fallback) | All modules | 3 days |
| 10 | Use `Literal` type for language codes | `core/fix_page.py` | 1 day |

### Security Hardening Priorities

| # | Priority | Action |
|---|---|---|
| 1 | Add URL validation to `get_url()` / `get_url_json()` — restrict to known Wikimedia domains |
| 2 | Replace bare `except Exception` with specific exception types + logging |
| 3 | Add JSON schema validation for external API responses |
| 4 | Sanitize environment variable paths in `config.py` |
| 5 | Remove hardcoded `localhost` URL from `settings.py` |
| 6 | Add timeout configuration (currently hardcoded at 5s) |

### DevOps and Testing Recommendations

| # | Recommendation | Priority |
|---|---|---|
| 1 | Set up GitHub Actions with pytest + ruff + mypy | High |
| 2 | Add coverage thresholds (target: 80%+) | High |
| 3 | Add pre-commit hooks for formatting and linting | Medium |
| 4 | Add property-based tests (hypothesis) for regex transformations | Medium |
| 5 | Add performance benchmarks for batch processing | Low |
| 6 | Create API documentation with Sphinx | Low |
| 7 | Add issue and PR templates | Low |

---

## Final Evaluation

### Scoring

| Metric | Score | Notes |
|---|---|---|
| **Overall Project Score** | **6.5 / 10** | Functional and well-architected at the module level, but has critical bugs, missing infrastructure, and notable code duplication |
| **Risk Level** | **Medium** | The `or True` bug silently overrides configuration; string replacement could corrupt wikitext; bare exceptions hide errors |
| **Technical Debt Level** | **Medium** | Duplicate code, inconsistent naming, debug prints in production, missing type annotations |
| **Estimated Production Readiness** | **70%** | Core pipeline works for common cases; configuration bug, missing error handling, and lack of CI/CD are blockers |

### Summary Verdict

fix_refs is a **functional and well-designed library** with a clear pipeline architecture and good modular decomposition. The pure-function bot design and data-driven Spanish processing are strong engineering choices. However, it has **several critical bugs** (the `or True` configuration override, string replacement fragility) and **significant gaps in infrastructure** (no CI/CD, no integration tests, no HTTP mocking). The codebase shows signs of organic growth — duplication has accumulated, naming conventions have drifted, and debug artifacts remain in production code.

### Recommended Next Steps

1. **Fix the `or True` bug immediately** — this is a 5-minute fix with high impact
2. **Remove debug `print()` statements** from `remove_space.py`
3. **Set up CI/CD** with GitHub Actions (pytest + ruff + mypy)
4. **Add integration tests** for the full pipeline
5. **Consolidate duplicated code** across `lang_bots/`
6. **Address the security findings** in `utils/http.py`

With these fixes, the project would move from **6.5/10 to approximately 8/10** and be suitable for production deployment in WikiProjectMed's Translation Dashboard.

---

*End of Report*
