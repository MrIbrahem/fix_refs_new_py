"""
Swahili-specific bot fixes
"""

import re


def sw_fixes(text: str) -> str:
    """Apply Swahili-specific fixes to text

    Fixes section title: == Marejeleo == to == Marejeo ==
    Works case-insensitively but only on standalone section headers.
    If there are multiple occurrences on the same line separated by text,
    only the later ones are changed.

    Args:
        text: WikiText content

    Returns:
        Fixed text
    """
    # Pattern for Marejeleo section headers (case insensitive)
    pattern = r'(=+)[\s]*[Mm][Aa][Rr][Ee][Jj][Ee][Ll][Ee][Oo][\s]*(\1)'

    # First, handle multiline cases where = signs have newlines between them
    # These are single headers split across lines - always replace
    # Only match patterns that span multiple lines (contain \n)
    def multiline_replacer(match):
        if '\n' in match.group(0):
            return match.group(1) + ' Marejeo ' + match.group(2)
        return match.group(0)  # Don't change single-line matches here

    text = re.sub(pattern, multiline_replacer, text, flags=re.DOTALL)

    # Now process line by line for the edge case of multiple headers per line
    lines = text.split('\n')
    result_lines = []

    for line in lines:
        matches = list(re.finditer(pattern, line))

        if len(matches) == 0:
            result_lines.append(line)
        elif len(matches) == 1:
            # Single occurrence - always replace
            line = re.sub(pattern, r'\1 Marejeo \2', line)
            result_lines.append(line)
        else:
            # Multiple occurrences on same line - keep first, fix rest
            first_match = matches[0]
            first_end = first_match.end()
            first_part = line[:first_end]
            rest_part = line[first_end:]

            rest_part = re.sub(pattern, r'\1 Marejeo \2', rest_part)
            result_lines.append(first_part + rest_part)

    return '\n'.join(result_lines)
