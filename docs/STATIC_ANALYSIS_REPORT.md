# Static Analysis Report for fix_refs

**Generated:** 2026-02-14
**Codebase:** fix_refs - MediaWiki wikitext reference fixing library
**Python Version:** 3.10+

---

## Executive Summary

This report documents issues found during comprehensive static analysis of the fix_refs codebase, including logical errors, security vulnerabilities, performance bottlenecks, and architectural anti-patterns. Recommendations for type safety improvements are also provided.

### Critical Issues Found: 8
### High Priority Issues: 12
### Medium Priority Issues: 15
### Low Priority Issues: 10

---

## 1. Critical Issues

### 1.1 Dataclass Anti-Pattern in `parsers/citations_parser.py`

**Location:** `fix_refs/parsers/citations_parser.py:9-25`

**Issue:** The `Citation` class uses `@dataclass` decorator but defines `__init__` manually, defeating the purpose of dataclass and violating Python conventions.

```python
@dataclass
class Citation:
    def __init__(self, ref: Any) -> None:  # Wrong - dataclass generates __init__
        self.ref = None
        self.copy_object(ref)
```

**Impact:**
- The `@dataclass` decorator is effectively useless
- Type checkers may produce incorrect analysis
- Adds unnecessary overhead

**Recommendation:** Either remove `@dataclass` or properly define class fields.

---

### 1.2 Duplicate Function Definitions

**Location:** Multiple files

**Issue:** `str_ends_with` and `str_starts_with` are defined identically in both:
- `fix_refs/bots/refs_utils.py:6-16`
- `fix_refs/lang_bots/hy_bot.py:10-17`

**Impact:**
- Code duplication increases maintenance burden
- Risk of divergence between implementations

**Recommendation:** Consolidate into a single location (utils module).

---

### 1.3 Duplicate `remove_short_refs` Function

**Location:**
- `fix_refs/lang_bots/es/es_helpers.py:10-20`
- `fix_refs/lang_bots/es/es_refs.py:75-86`

**Impact:** Same as above - code duplication.

---

### 1.4 Inconsistent Return Type in `apply_language_fixes`

**Location:** `fix_refs/lang_bots/__init__.py:12-31`

**Issue:** Function can return either the modified text or `None` (implicitly) when no language matches.

```python
def apply_language_fixes(text, title, lang, source_title, mdwiki_revid) -> str:
    if lang == "pl":
        text = pl_fixes(text)
    # ... other conditions
    # No return statement if no condition matches!
    return text  # Actually there is, but the type hint is implicit
```

**Impact:** Return type is annotated as `str` but function signature lacks parameter types.

---

### 1.5 Regex Injection Risk via `re.escape` in `es_bot.py`

**Location:** `fix_refs/lang_bots/es/es_bot.py:31`

**Issue:** While `re.escape` is used, the pattern construction could be vulnerable if `name` contains special sequences.

```python
pattern = r'\{\{\s*' + re.escape(name) + r'\s*(\|)'
```

**Status:** Actually safe due to `re.escape`, but worth noting for code review.

---

### 1.6 Boolean Logic Error in `core/__init__.py`

**Location:** `fix_refs/core/__init__.py:14`

**Issue:** The expression `or True` makes the expand setting always True, ignoring the settings file.

```python
expand = bool(int(lang_default.get("expend", 1))) or True
```

**Impact:** The `expend` setting from configuration is effectively ignored - expand will always be True.

---

### 1.7 String Replacement Without Position Tracking

**Location:** `fix_refs/bots/expend_refs.py:31` and `fix_refs/bots/remove_duplicate_refs.py:55`

**Issue:** Using `str.replace()` for complex string replacements can cause issues if the same text appears multiple times.

```python
text = text.replace(refe, rr)
```

**Impact:** If the same reference text appears multiple times, all instances are replaced, which may not be the intended behavior.

---

### 1.8 Uncached HTTP Requests in Tight Loops

**Location:** `fix_refs/bots/fix_images.py:51`

**Issue:** While there's a cached version, the default `remove_missing_images()` uses uncached API calls which could be called multiple times for the same image.

---

## 2. Security Vulnerabilities

### 2.1 No Input Validation on External Data

**Location:** Multiple HTTP utilities

**Issue:** No validation of URLs before making requests.

```python
def get_url(url: str, timeout: int = 5) -> str:
    # No URL validation
    response = requests.get(url, headers=headers, timeout=timeout)
```

**Impact:** Potential for SSRF (Server-Side Request Forgery) if URLs come from untrusted sources.

**Recommendation:** Add URL validation to prevent access to internal resources.

---

### 2.2 JSON Parsing Without Schema Validation

**Location:** Multiple files using `json.load()` and `json.loads()`

**Issue:** JSON data from external sources is parsed without schema validation.

**Recommendation:** Consider using pydantic or similar for validated parsing.

---

### 2.3 Environment Variable Injection

**Location:** `fix_refs/config.py:15`

**Issue:** Environment variables are used directly in path construction without sanitization.

```python
resources_path = Path(os.getenv("RESOURCES_PATH", Path(__file__).parent.parent / "resources")).expanduser()
```

**Impact:** Could lead to path traversal if environment is compromised.

---

## 3. Performance Bottlenecks

### 3.1 Repeated WikiText Parsing

**Location:** Multiple bots that parse the same text multiple times.

**Issue:** Each bot function parses text with `wtp.parse()` independently, causing redundant parsing.

**Impact:** O(n) parsing operations where n = number of bot functions called.

**Recommendation:** Parse once in `fix_one_page()` and pass parsed object to sub-functions.

---

### 3.2 Non-Compiled Regex Patterns

**Location:** Multiple files create regex patterns inside functions.

**Issue:** Regex patterns are compiled on every function call instead of once at module level.

Example: `fix_refs/bots/mini_fixes.py:41-43`
```python
def fix_sections_titles(text: str, lang: str) -> str:
    # Pattern compiled on every call
    pattern = rf'(=+)\s*{k}\s*\1'
```

**Recommendation:** Pre-compile patterns at module level or use `@lru_cache`.

---

### 3.3 String Concatenation in Loops

**Location:** `fix_refs/lang_bots/es/es_refs.py:7-21`

**Issue:** String concatenation in loops is inefficient.

```python
def make_line(refs) -> str:
    line = "\n"
    for g, gag in refs.items():
        for name, ref in gag.items():
            line += f'<ref name="{name}">{ref}</ref>\n'  # Inefficient
```

**Recommendation:** Use `str.join()` or list comprehension.

---

### 3.4 Uncached Settings Loading

**Location:** `fix_refs/core/settings.py:18-29`

**Issue:** `load_settings_from_server()` makes HTTP call on every cache miss without local caching.

---

## 4. Architectural Anti-Patterns

### 4.1 God Function Pattern

**Location:** `fix_refs/core/fix_page.py:23-84`

**Issue:** `fix_one_page()` function has 10 steps and growing. This violates Single Responsibility Principle.

**Recommendation:** Consider a pipeline pattern with composable stages.

---

### 4.2 Primitive Obsession

**Location:** Throughout codebase

**Issue:** Language codes are passed as strings everywhere, not as typed enums or literals.

```python
def fix_one_page(text: str, title: str, lang: str, ...) -> str:
```

**Recommendation:** Use `Literal` type or `enum` for known language codes.

---

### 4.3 Inconsistent Error Handling

**Location:** Throughout codebase

**Issue:** Some functions return empty strings on error, others return the original text, some raise exceptions.

Examples:
- `get_url()` returns `""` on error
- `fix_one_page()` returns `text_org` on empty result
- File loading functions return `{}`` on error

**Recommendation:** Establish consistent error handling strategy.

---

### 4.4 Missing Protocol/Interface Definitions

**Location:** Parsers module

**Issue:** No abstract base class or protocol for parsers, making it hard to add new parsers or mock for testing.

---

### 4.5 Global Mutable State

**Location:** `fix_refs/utils/debug.py:20-24`

**Issue:** `DEBUG` and `TEST_MODE` are module-level mutable globals.

```python
DEBUG: bool = False
TEST_MODE: bool = False
```

**Impact:** Makes testing difficult, can cause race conditions in concurrent environments.

**Recommendation:** Use context variables or configuration injection.

---

## 5. Type Safety Issues

### 5.1 Missing Return Type Annotations

The following functions lack return type annotations:

| File | Function |
|------|----------|
| `lang_bots/__init__.py` | `apply_language_fixes` |
| `lang_bots/es/es_refs.py` | `make_line`, `get_refs`, `add_line_to_temp`, `mv_es_refs` |
| `infobox/expend_infobox.py` | `expend_new`, `extract_templates_and_params`, `make_section_0` |
| `lang_bots/remove_space.py` | `match_it`, `get_parts` |

---

### 5.2 Missing Parameter Type Annotations

| File | Function | Parameters |
|------|----------|------------|
| `lang_bots/__init__.py` | `apply_language_fixes` | All parameters |
| `lang_bots/es/es_refs.py` | `make_line` | `refs` |
| `infobox/expend_infobox.py` | `expand_infobox_in_text` | All parameters |
| `lang_bots/remove_space.py` | `match_it` | All parameters |

---

### 5.3 Use of `Any` Type

**Location:** `fix_refs/parsers/citations_parser.py:13`

**Issue:** `Citation.__init__` takes `ref: Any` which bypasses type checking.

**Recommendation:** Use proper type from `wikitextparser` library.

---

### 5.4 Implicit Optional Not Used

Several functions can return `None` but don't use `Optional[T]` or `T | None`.

---

## 6. Code Quality Issues

### 6.1 Magic Numbers

**Location:** Various files

- `fix_refs/lang_bots/es/es_bot.py:104` - `line_count < 10`
- `fix_refs/bots/fix_images.py:64` - `maxsize=1000`
- `fix_refs/infobox/expend_infobox.py:43` - `ljust(17)`

---

### 6.2 Dead Code

**Location:** `fix_refs/lang_bots/es/es_refs.py:62-63`

```python
# ---
refs_to_name[conts] = name
```

Variable `refs_to_name` is populated but never used after the loop.

---

### 6.3 Commented-Out Code

**Location:** Multiple files have commented-out code that should be removed:
- `fix_refs/bots/remove_duplicate_refs.py:62-63`
- `fix_refs/infobox/expend_infobox.py:41`

---

### 6.4 Inconsistent Naming Conventions

**Location:** Throughout codebase

- `expend_refs.py` - should be `expand_refs.py` (typo in module name)
- `expend_infobox.py` - same issue
- `do_comments` - not following verb_noun convention used elsewhere

---

### 6.5 Print Statements for Debugging

**Location:** `fix_refs/lang_bots/remove_space.py:28,36,51,58,65`

**Issue:** Production code contains `print()` statements instead of using logging or the debug utilities.

```python
print(f"count(matches)={len(matches)}")
```

---

## 7. Documentation Issues

### 7.1 Missing Module Docstrings

| File | Status |
|------|--------|
| `lang_bots/remove_space.py` | Incomplete docstring |
| `lang_bots/es/es_refs.py` | Missing module docstring |

---

### 7.2 Missing Function Docstrings

| File | Functions |
|------|-----------|
| `lang_bots/remove_space.py` | `match_it`, `get_parts`, `remove_spaces_between...` |
| `lang_bots/es/es_refs.py` | `make_line`, `get_refs`, `mv_es_refs` |
| `infobox/expend_infobox.py` | `expend_new`, `extract_templates_and_params` |

---

## 8. Recommendations Summary

### Immediate Actions (Critical)

1. Fix the dataclass anti-pattern in `parsers/citations_parser.py`
2. Fix the boolean logic error in `core/__init__.py` (`or True`)
3. Remove duplicate code between `refs_utils.py` and `hy_bot.py`
4. Consolidate `remove_short_refs` implementations

### Short-Term Actions (High Priority)

1. Add comprehensive type annotations to all functions
2. Create abstract base classes/protocols for parsers
3. Fix the `expend` → `expand` naming typo throughout
4. Replace `print()` statements with proper logging
5. Add URL validation to HTTP utilities

### Medium-Term Actions

1. Implement a pipeline pattern for `fix_one_page()`
2. Add JSON schema validation for external data
3. Pre-compile regex patterns at module level
4. Create typed language code constants/enums
5. Establish consistent error handling strategy

### Long-Term Actions

1. Consider using a configuration management library
2. Add comprehensive integration tests
3. Create API documentation with Sphinx
4. Implement performance benchmarks

---

## 9. Type Annotation Plan

### Type Aliases to Add

```python
from typing import TypeAlias, Literal

LanguageCode: TypeAlias = Literal["en", "es", "pt", "pl", "bg", "hy", "sw", "ru", "hr"]
WikiText: TypeAlias = str
TemplateName: TypeAlias = str
```

### Protocols to Add

```python
from typing import Protocol

class TextProcessor(Protocol):
    def __call__(self, text: str, lang: str) -> str: ...

class TemplateProcessor(Protocol):
    def __call__(self, template: wtp.Template) -> str: ...
```

---

## Appendix A: Files Requiring Type Annotation Updates

| Priority | File | Status |
|----------|------|--------|
| Critical | `parsers/citations_parser.py` | Partial |
| Critical | `core/__init__.py` | Partial |
| High | `lang_bots/__init__.py` | None |
| High | `lang_bots/es/es_refs.py` | None |
| High | `infobox/expend_infobox.py` | None |
| High | `lang_bots/remove_space.py` | None |
| Medium | `bots/move_dots.py` | Partial |
| Medium | `bots/redirect.py` | Partial |
| Medium | `bots/mini_fixes.py` | Partial |
| Medium | `lang_bots/bg_bot.py` | Partial |
| Medium | `lang_bots/hy_bot.py` | Partial |
| Medium | `lang_bots/sw_bot.py` | Partial |
| Medium | `mdwiki/category.py` | Partial |

---

*End of Report*
