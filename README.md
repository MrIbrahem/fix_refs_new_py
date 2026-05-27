# Fix Refs

A Python library to parse and fix references in MediaWiki wikitext. Built for WikiProjectMed's Translation Dashboard to process Wikipedia article translations from MDWiki.

## Project Overview

fix_refs processes wikitext pages to normalize references, translate templates, fix formatting, and add metadata for translated medical articles across multiple Wikipedia language editions.

### Supported Languages

Spanish, Portuguese, Bulgarian, Armenian, Polish, Swahili (with English as the source language).

### Key Capabilities

- Expand short references (`<ref name="x"/>`) from MDWiki source text
- Remove duplicate references
- Move punctuation before/after reference tags (language-specific)
- Translate citation templates (English -> Spanish/Portuguese)
- Add `|language=en` parameter to English source citations
- Expand and format infobox templates
- Validate images against Wikimedia Commons
- Add translation attribution categories

## Installation

```bash
pip install git+https://github.com/MrIbrahem/fix_refs_new_py.git

# or
pip install -e .

# with dev dependencies
pip install -e ".[dev]"
```

## Usage

```python
from fix_refs import fix_one_page

# Direct usage
fixed_text = fix_one_page(
    text="Your wikitext here",
    title="Page Title",
    lang="es",           # target language code
    move_dots=True,      # move punctuation before refs
    expend_infobox=True, # expand infobox templates
    add_en_lang=False,   # add |language=en to citations
    add_category=False,  # add MDWiki translation category
    source_title="",     # source page title
    mdwiki_revid=0       # MDWiki revision ID
)

# With automatic settings
from fix_refs import DoChangesToText1

fixed_text = DoChangesToText1(
    source_title="Source Article",
    title="Translated Title",
    text="wikitext content",
    lang="es",
    mdwiki_revid=12345
)
```

## Architecture

```
fix_refs/
├── core/           # Entry points and pipeline orchestration
│   ├── fix_page.py # Main fix_one_page() function
│   └── settings.py # Language settings loader
├── bots/           # Individual transformation functions
│   ├── mini_fixes.py
│   ├── fix_missing_refs.py
│   ├── remove_duplicate_refs.py
│   ├── move_dots.py
│   ├── add_lang_en_bot.py
│   ├── fix_images.py
│   └── months.py
├── lang_bots/      # Language-specific processing
│   ├── es/         # Spanish (most complex)
│   ├── bg_bot.py   # Bulgarian
│   ├── hy_bot.py   # Armenian
│   ├── pl_bot.py   # Polish
│   ├── pt_bot.py   # Portuguese
│   └── sw_bot.py   # Swahili
├── parsers/        # Low-level wikitext parsers
│   ├── citations.py
│   └── category.py
├── infobox/        # Infobox template expansion
├── mdwiki/         # MDWiki category integration
├── utils/          # HTTP client and debug utilities
└── resources/      # Local data files and cached revisions
```

### Processing Pipeline

`fix_one_page()` applies transformations in this order:

1. Skip if redirect page
2. Expand infobox templates
3. Apply mini fixes (whitespace, section titles, ref spacing)
4. Fix missing refs (expand from MDWiki source)
5. Remove duplicate refs
6. Move dots (if enabled)
7. Add language=en (if enabled)
8. Apply language-specific fixes
9. Add category (if enabled)
10. Apply post-fix mini fixes

## Development

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

# Format with ruff (line-length: 120)
ruff format fix_refs/
```

## Dependencies

- **requests** >= 2.31.0 - HTTP client
- **wikitextparser** >= 0.55.0 - MediaWiki wikitext parsing
- **python-dotenv** - Environment variable loading

### Dev Dependencies

- pytest, pytest-cov - Testing
- mypy - Type checking
- pylint - Linting
- ruff, black, isort - Formatting

## Configuration

| Environment Variable | Default | Purpose |
|---------------------|---------|---------|
| `RESOURCES_PATH` | `./resources` | Path to local data files |
| `REVISIONS_PATH` | `$RESOURCES_PATH/revisions` | Path to cached revisions |
| `SERVER_NAME` | (empty) | If set, loads settings from remote API |

## License

GPL-3.0-or-later (see pyproject.toml)
