# fix_refs/parsers - Low-Level Wikitext Parsers

## Project Overview

The `parsers/` module provides low-level parsing utilities for extracting structured data from MediaWiki wikitext. It wraps `wikitextparser` with domain-specific abstractions for citations and categories.

### Main Modules

| File | Purpose |
|------|---------|
| `citations.py` | Parses `<ref>` tags into `Citation` dataclass objects; provides extraction functions |
| `category.py` | Parses `[[Category:...]]` links into structured data |

### Technologies

- **wikitextparser** - Core parsing engine for wikitext
- **dataclasses** - Structured data representation
- **re** - Regex for category parsing

---

## Architecture & Code Quality Review

### Code Organization

Clean two-file structure. `citations.py` provides a `Citation` class and extraction functions. `category.py` provides category parsing functions.

### Design Patterns

- **Dataclass** - `Citation` encapsulates reference tag data with accessor methods
- **Factory functions** - `get_citations()`, `get_short_citations()`, `get_full_refs()` create Citation objects
- **Facade** - `Citation` class wraps wikitextparser's `Tag` object with a cleaner API

### Maintainability

Good. The `Citation` class provides a stable interface over wikitextparser's internals.

### Readability

Good docstrings with Args/Returns. The `Citation` class methods are self-documenting.

---

## Strengths

1. **`Citation` dataclass** - Clean abstraction over wikitextparser's Tag object with clear accessor methods
2. **Multiple extraction functions** - `get_citations()`, `get_short_citations()`, `get_full_refs()` cover different use cases
3. **Good docstrings** - Every function and method has documentation
4. **Category parser** - Handles case-insensitive category detection and pipe-separated parameters

---

## Weaknesses

### `Citation` Class Design Issues

1. **`@dataclass` decorator is unused** - The class defines its own `__init__()` and doesn't use dataclass-generated methods (`__eq__`, `__repr__`, etc.):
   ```python
   @dataclass
   class Citation:
       def __init__(self, ref: Any) -> None:
           self.ref = None
           self.copy_object(ref)
   ```
   The `@dataclass` decorator does nothing here since `__init__` is manually defined.

2. **`copy_object()` re-parses** - To work around wikitextparser's `deepcopy` limitation, the method converts to string and re-parses:
   ```python
   def copy_object(self, ref):
       parsed = wtp.parse(str(ref.string))
       for tag in parsed.get_tags():
           if tag.string == parsed.string:
               self.ref = tag
               break
   ```
   This is a workaround, not a solution. If the tag's string appears in nested content, it could match the wrong tag.

3. **Redundant accessor methods** - `get_original_text()`, `get_content()`, `get_name()` just call properties (`self.tag`, `self.content`, `self.name`). The properties already exist.

4. **`get_attributes()` uses string manipulation** instead of the `attrs` property:
   ```python
   def get_attributes(self) -> str:
       str_attrs = str(self.ref.string).split(">")[0].replace("<ref", "").strip()
       return str_attrs.strip()
   ```
   This is fragile - it breaks if the ref content contains `>`.

### Category Parser

`category.py` uses regex instead of wikitextparser for category parsing, which is less robust for edge cases (categories inside templates, comments, etc.).

---

## Critical Issues

1. **`Citation.get_attributes()` string parsing** - Splitting on `>` will break if reference content contains `>`. Should use `self.ref.attrs` directly.

2. **`copy_object()` fragility** - Matching `tag.string == parsed.string` could match nested tags incorrectly.

---

## Areas That Need Attention

- Remove unused `@dataclass` decorator from `Citation`
- Fix `get_attributes()` to use `self.ref.attrs` instead of string manipulation
- Consider if `copy_object()` workaround is still needed with current wikitextparser version
- Use wikitextparser for category parsing instead of regex
- Remove redundant getter methods that duplicate properties

---

## Improvement Plan

### Quick Wins

1. Remove `@dataclass` decorator from `Citation`
2. Fix `get_attributes()` to use attrs dict
3. Remove redundant `get_original_text()`, `get_content()`, `get_name()` methods

### Medium-term

1. Replace `copy_object()` with proper cloning if wikitextparser now supports it
2. Rewrite category parser using wikitextparser
3. Add `__repr__` and `__eq__` to Citation for debugging

### Long-term

1. Add validation to Citation construction
2. Support additional reference formats beyond `<ref>` tags

---

## Comprehensive Review

| Metric | Score | Notes |
|--------|-------|-------|
| **Overall Rating** | 7/10 | Good abstractions, but Citation class has design issues |
| **Production Readiness** | Good | Works correctly for common cases |
| **Technical Debt** | Medium | Unused decorator, fragile string parsing, redundant methods |
| **Risk Assessment** | Low-Medium | `get_attributes()` could break on edge cases |
| **Maintainability** | 7/10 | Clear API, but some internal fragility |
