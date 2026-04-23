# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

fix_refs is a Python library for parsing and fixing references in MediaWiki wikitext. It's used by WikiProjectMed's translation dashboard to process Wikipedia article translations.

## Development Commands

```bash
# Install in development mode
pip install -e ".[dev]"

# Run all tests
pytest

# Run tests with coverage
pytest --cov=fix_refs --cov-report=html

# Run a specific test file
pytest tests/core/test_fix_refs.py

# Run a specific test
pytest tests/core/test_fix_refs.py::TestFixRefs::test_hy_language_simple

# Type checking
mypy fix_refs/

# Linting
pylint fix_refs/

# Format with black/ruff (line-length: 120)
black fix_refs/
ruff format fix_refs/
```

## Architecture

The codebase has four main modules under `fix_refs/`:

### core/
Entry point and orchestration layer:
- `fix_page.py` - Main `fix_one_page()` function that orchestrates all fixes in a pipeline
- `settings.py` - Loads language-specific settings from JSON file or API server

### bots/
Individual transformation functions that operate on wikitext:
- `mini_fixes.py` - General fixes: section title translation, whitespace cleanup, interwiki link simplification
- `fix_missing_refs.py` - Expands short refs (`<ref name="x"/>`) from MDWiki source text
- `remove_duplicate_refs.py` - Deduplicates references with identical names
- `move_dots.py` - Moves punctuation after refs to before refs (language-specific)
- `add_lang_en_bot.py` - Adds `|language=en` to English source citations
- `fix_images.py` - Fixes image syntax and retrieves metadata from Commons API

### lang_bots/
Language-specific processing modules. Each module handles fixes specific to a Wikipedia language edition:
- `bg_bot.py` - Bulgarian
- `es/` - Spanish (has submodules for data, helpers, refs, section processing)
- `hy_bot.py` - Armenian
- `pl_bot.py` - Polish
- `pt_bot.py` - Portuguese
- `sw_bot.py` - Swahili

### parsers/
Low-level parsers using `wikitextparser` library:
- `citations.py` - Parses `<ref>` tags into `Citation` dataclass objects
- `category.py` - Parses category links

### utils/
- `http.py` - HTTP client with `get_url()` and `get_url_json()` helpers
- `debug.py` - Debug output utilities

## Main Entry Point

```python
from fix_refs import fix_one_page

fixed_text = fix_one_page(
    text="wikitext content",
    title="Page Title",
    lang="en",  # language code
    move_dots=True,
    expend_infobox=True,
    add_en_lang=False,
    add_category=False,
    source_title="",
    mdwiki_revid=0
)
```

The `DoChangesToText1()` function is the alternative entry point that loads language settings automatically.

## Processing Pipeline

`fix_one_page()` applies transformations in this order:
1. Skip if redirect page
2. Expand infobox templates
3. Apply mini_fixes (whitespace, section titles)
4. Fix missing refs (expand from source)
5. Remove duplicate refs
6. Move dots (if enabled)
7. Add language=en (if enabled)
8. Apply language-specific fixes
9. Add category (if enabled)
10. Apply post-fix mini_fixes

## Configuration

- `config.py` - Sets up paths for `resources_path` and `revisions_path` from environment variables
- `resources/language_settings.json` - Per-language settings (move_dots, expend, add_en_lang)
- Settings can also be loaded from `mdwiki.toolforge.org` API when `SERVER_NAME` env var is set

## Code Style

- Line length: 120 characters
- Python 3.10+ with type hints
- Uses `wikitextparser` library for parsing MediaWiki syntax
- Tests use pytest with class-based organization
