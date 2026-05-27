# fix_refs/resources - Data Files

## Project Overview

The `resources/` directory contains static data files and cached revision data used by the fix_refs library at runtime.

### Contents

| Path | Purpose |
|------|---------|
| `language_settings.json` | Per-language configuration (move_dots, expend, add_en_lang) |
| `revisions/` | Cached MDWiki revision wikitext files |
| `revisions/1469242/` | Example cached revision |

### Technologies

- **JSON** - Configuration data format
- **Plain text** - Cached wikitext files

---

## Architecture & Code Quality Review

### Design

The resources directory serves as a local cache and fallback data source. When the MDWiki API is unavailable, the library reads from these files instead.

### File Organization

- `language_settings.json` - Loaded by `core/settings.py`
- `revisions/{id}/wikitext.txt` - Loaded by `bots/fix_missing_refs.py` for reference expansion

---

## Strengths

1. **Offline support** - Enables development and testing without API access
2. **Standard paths** - Uses environment variables (`RESOURCES_PATH`, `REVISIONS_PATH`) for configurability

---

## Weaknesses

1. **No documentation** - No README explaining the file format or how to update the data
2. **Committed cache data** - Revision files in `revisions/` are cached data that probably shouldn't be in version control
3. **No validation** - No schema or validation for `language_settings.json`

---

## Critical Issues

1. **Cached revisions in git** - The `revisions/` directory contains cached wikitext that will bloat the repository over time. Consider `.gitignore` or external storage.

---

## Areas That Need Attention

- Add `.gitignore` for `revisions/` directory or move to external storage
- Document the JSON schema for `language_settings.json`
- Add a script to update/download revision data

---

## Improvement Plan

### Quick Wins

1. Add `revisions/` to `.gitignore`
2. Document the `language_settings.json` format

### Medium-term

1. Create a script to download/cache revision data
2. Add JSON schema validation

---

## Comprehensive Review

| Metric | Score | Notes |
|--------|-------|-------|
| **Overall Rating** | 5/10 | Functional but lacks documentation and has cache in VCS |
| **Production Readiness** | Good | Works as designed |
| **Technical Debt** | Low | Cache data in git |
| **Risk Assessment** | Low | Fallback data is supplementary |
| **Maintainability** | 6/10 | Needs documentation |
