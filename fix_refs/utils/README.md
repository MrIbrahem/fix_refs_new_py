# fix_refs/utils - Utility Functions

## Project Overview

The `utils/` module provides shared utility functions used across the fix_refs library: HTTP client helpers and debug/test output control.

### Main Modules

| File       | Purpose                                                                 |
| ---------- | ----------------------------------------------------------------------- |
| `http.py`  | HTTP client with `get_url()` and `get_url_json()` for API calls         |
| `debug.py` | Debug and test mode output control via `echo_debug()` and `echo_test()` |

### Technologies

-   **requests** - HTTP client library
-   **json** - JSON parsing

---

## Architecture & Code Quality Review

### Code Organization

Simple two-file structure. Both files are focused on a single concern.

### Design Patterns

-   **Global flags** for debug/test mode (`DEBUG`, `TEST_MODE`)
-   **Graceful degradation** - HTTP functions return empty/default values on failure
-   **User-Agent compliance** - Sets proper User-Agent for Wikimedia API requests

### Maintainability

Good. The functions are simple and well-documented.

### Readability

Clear function signatures with docstrings. Error handling is explicit.

---

## Strengths

1. **Proper User-Agent** - Complies with Wikimedia API policy with descriptive bot identification
2. **Graceful error handling** - Returns empty string/None on failure instead of raising
3. **Specific exception handling** - Catches `requests.RequestException`, `json.JSONDecodeError` separately
4. **Simple debug control** - Global flags make it easy to enable/disable output

---

## Weaknesses

### Debug Module Limitations

1. **Global mutable state** - `DEBUG` and `TEST_MODE` are module-level globals that can't be configured per-module or per-request
2. **Uses `print()`** - Should use Python's `logging` module for proper log level control, handlers, and formatting
3. **No way to capture output** - `echo_debug()` prints directly to stdout, making it hard to test or redirect

### HTTP Module Issues

1. **No retry logic** - Failed requests return empty immediately with no retry
2. **No connection pooling** - Each call creates a new connection (though `requests.Session` could help)
3. **Bare `except Exception`** (`http.py:32`) - Catches all exceptions including programming errors like `TypeError`, `AttributeError`
4. **Duplicate User-Agent string** - The User-Agent header is defined identically in both `get_url()` and `get_url_json()`

### Missing Utilities

The module is very thin. Common patterns across the codebase (like `start_end()`, `str_ends_with()`) could live here but don't.

---

## Critical Issues

1. **Bare `except Exception`** in `http.py:32` and `http.py:58` - Swallows programming errors that should propagate. Should at minimum log the exception.

2. **No timeout configuration** - Default timeout is 5 seconds, hardcoded. For batch operations (like image checking), this could be too short or too long.

---

## Areas That Need Attention

-   Replace `print()` with `logging` module
-   Remove bare `except Exception` clauses
-   Extract User-Agent string to a constant
-   Add retry logic for transient HTTP failures
-   Add request/session pooling for batch operations

---

## Improvement Plan

### Quick Wins

1. Extract User-Agent to a module-level constant
2. Replace bare `except Exception` with specific exception types
3. Add `logging` integration alongside or replacing `echo_debug()`

### Medium-term

1. Add retry logic with exponential backoff
2. Use `requests.Session` for connection pooling
3. Make timeout configurable via environment variable or settings

### Long-term

1. Add request metrics (count, latency, error rate)
2. Implement circuit breaker pattern for unreliable APIs

---

## Comprehensive Review

| Metric                   | Score      | Notes                                                           |
| ------------------------ | ---------- | --------------------------------------------------------------- |
| **Overall Rating**       | 7/10       | Functional but minimal; needs logging and better error handling |
| **Production Readiness** | Moderate   | Works but swallows errors silently                              |
| **Technical Debt**       | Low        | Simple code, but bare exceptions and print-based debugging      |
| **Risk Assessment**      | Low-Medium | Silent error swallowing could hide issues                       |
| **Maintainability**      | 8/10       | Simple and focused                                              |
