# Fix Refs

A Python library to parse and fix references in MediaWiki wikitext.

## Installation

```bash
pip install -e .
```

## Usage

```python
from fix_refs import fix_refs

text = "Your wikitext here"
lang = "en"
fixed_text = fix_refs(text, lang)
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
pytest --cov=src --cov-report=html

# Type checking
mypy src/

# Linting
pylint src/
```
