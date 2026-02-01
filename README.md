# Fix Refs

A Python library to parse and fix references in MediaWiki wikitext.

## Installation

```bash
pip install -e .
```

## Usage

```python
from fix_refs import fix_one_page

text = "Your wikitext here"
title = "title"
lang = "en"
fixed_text = fix_one_page(text, title, lang)
```

## Testing

```bash
pytest
```

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests with coverage
pytest --cov=fix_refs --cov-report=html

# Type checking
mypy fix_refs/

# Linting
pylint fix_refs/
```
