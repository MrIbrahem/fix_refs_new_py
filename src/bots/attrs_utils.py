"""
Attribute utilities for parsing reference attributes
"""

import re
from typing import Dict


def parse_attributes(text: str) -> Dict[str, str]:
    """Parse attributes from reference options text

    Args:
        text: Attribute text (e.g., 'name="ref1" lang="en"')

    Returns:
        Dictionary of attribute names (lowercase) to values
    """
    text = f"<ref {text}>"

    pattern = r'''
        ((?<=[\'"\s\/])[^\s\/>][^\s\/=>]*)            # Attribute name
        (\s*=+\s*                                      # Equals sign(s)
        (
            \'[^\']*\'                                 # Value in single quotes
            |"[^"]*"                                   # Value in double quotes
            |(?![\'"])[^>\s]*                          # Unquoted value
        ))?
        (?:\s|\/(?!>))*                                # Trailing space or slash not followed by >
    '''

    attributes_array: Dict[str, str] = {}

    matches = re.findall(pattern, text, re.VERBOSE | re.UNICODE)

    for match in matches:
        attr_name = match[0].lower()
        attr_value = match[2] if len(match) > 2 and match[2] else ""
        attributes_array[attr_name] = attr_value

    return attributes_array


def get_attrs(text: str) -> Dict[str, str]:
    """Get attributes from reference text

    Args:
        text: Reference text (e.g., 'name="ref1" lang="en"')

    Returns:
        Dictionary of attribute names (lowercase) to values
    """
    text = f"<ref {text}>"

    pattern = r"((?<=[\'\"\s\/])[^\s\/>][^\s\/=>]*)(\s*=+\s*(\'[^\']*\'|\"[^\"]*\"|(?![\'\"])[^>\s]*))?(?:\s|\/(?!>))*"

    attrs: Dict[str, str] = {}

    matches = re.findall(pattern, text, re.UNICODE)

    for match in matches:
        attr_name = match[0].lower()
        attr_value = match[2] if len(match) > 2 and match[2] else ""
        attrs[attr_name] = attr_value

    return attrs
