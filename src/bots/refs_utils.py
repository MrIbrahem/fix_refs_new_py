"""
Reference utilities for string manipulation
"""


def str_ends_with(string: str, end_string: str) -> bool:
    """Check if string ends with a specific substring

    Args:
        string: String to check
        end_string: Substring to look for at the end

    Returns:
        True if string ends with end_string
    """
    return string.endswith(end_string)


def str_starts_with(text: str, start: str) -> bool:
    """Check if string starts with a specific substring

    Args:
        text: String to check
        start: Substring to look for at the start

    Returns:
        True if string starts with start
    """
    return text.startswith(start)


def rm_str_from_start_and_end(text: str, find: str) -> str:
    """Remove string from both start and end if present

    Args:
        text: Text to modify
        find: String to remove from start and end

    Returns:
        Modified text
    """
    if not find:
        return text

    text = text.strip()

    if str_starts_with(text, find) and str_ends_with(text, find):
        text = text[len(find):-len(find)]

    return text.strip()


def remove_start_end_quotes(text: str) -> str:
    """Normalize quotes around text

    Removes quotes from start and end, then wraps in double quotes

    Args:
        text: Text to normalize

    Returns:
        Text wrapped in double quotes
    """
    text = text.strip()
    text = rm_str_from_start_and_end(text, '"')
    text = rm_str_from_start_and_end(text, "'")

    # Check if text already has partial quotes (start or end)
    starts_with_double = text.startswith('"')
    starts_with_single = text.startswith("'")
    ends_with_double = text.endswith('"')
    ends_with_single = text.endswith("'")

    # If text has a quote at only one end (partial quote)
    # Rule: Always add " at start, and also add ' at start if already has " at start
    if starts_with_double and not ends_with_double:
        # Has " at start but no " at end - add ' after the " at start
        return "'" + text
    if ends_with_double and not starts_with_double:
        # Has " at end but no " at start - add " at start
        return '"' + text
    if starts_with_single and not ends_with_single:
        # Has ' at start but no ' at end - add ' at end (after adding " at start)
        return '"' + text + '"'
    if ends_with_single and not starts_with_single:
        # Has ' at end but no ' at start - add ' at start (before existing text)
        return '"' + "'" + text

    # Otherwise, wrap in appropriate quote type
    quote = '"' if '"' not in text else "'"
    return f"{quote}{text}{quote}"
