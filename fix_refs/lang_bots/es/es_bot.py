"""
Spanish-specific bot fixes
"""

import re
import wikitextparser as wtp
from ...utils.debug import echo_test
from .es_data import REFS_TEMPS, ARGS_TO
from .es_helpers import fix_es_months_in_refs
from .es_refs import mv_es_refs


def work_one_temp(temp_text: str, name: str) -> str:
    """Transform a single template with Spanish name and parameters

    Args:
        temp_text: Original template text
        name: Template name

    Returns:
        Transformed template text
    """
    # Get Spanish template name
    temp_name2 = REFS_TEMPS.get(name.lower(), name)

    # Transform template name
    new_temp = temp_text
    if temp_name2.lower() != name.lower():
        # Replace template name in {{TemplateName|...}}
        pattern = r'\{\{\s*' + re.escape(name) + r'\s*(\|)'
        replacement = r'{{' + temp_name2 + r'\1'
        new_temp = re.sub(pattern, replacement, new_temp, flags=re.IGNORECASE)

    # Transform parameters
    for old_param, new_param in ARGS_TO.items():
        # Replace parameter names: |old_param=value -> |new_param=value
        pattern = r'\|\s*' + re.escape(old_param) + r'\s*='
        replacement = '|' + new_param + '='
        new_temp = re.sub(pattern, replacement, new_temp, flags=re.IGNORECASE)

    # Remove url-status parameter - match until next | or }}
    pattern = r'\|\s*url-status\s*=\s*[^|}]*'
    new_temp = re.sub(pattern, '', new_temp, flags=re.IGNORECASE)

    # Clean up double pipes
    new_temp = re.sub(r'\|\s*\|', '|', new_temp)

    # Strip trailing spaces from parameter values (value followed by |)
    new_temp = re.sub(r'\s+\|', '|', new_temp)

    # Strip trailing spaces before closing braces
    new_temp = re.sub(r'\s+\}\}', '}}', new_temp)

    return new_temp


def fix_temps(text: str) -> str:
    """Transform templates to Spanish equivalents

    Args:
        text: Text containing templates

    Returns:
        Text with transformed templates
    """
    parsed = wtp.parse(text)

    refs_temps_keys_lower = {k.lower() for k in REFS_TEMPS.keys()}
    refs_temps_values_lower = {k.lower() for k in REFS_TEMPS.values()}

    new_text = text

    for template in parsed.templates:
        name = template.name.strip()
        name_lower = name.lower()

        # Skip if not in refs_temps
        if name_lower not in refs_temps_keys_lower and name_lower not in refs_temps_values_lower:
            continue

        old_text_template = str(template)
        new_text_str = work_one_temp(old_text_template, name)
        new_text = new_text.replace(old_text_template, new_text_str)

    return new_text


def fix_es(text: str, title: str = "") -> str:
    """Apply Spanish-specific fixes to text

    Args:
        text: WikiText content
        title: Page title

    Returns:
        Fixed text
    """
    # Check for "#REDIRECCIÓN"
    if "#REDIRECCIÓN" in text.upper() and title != "test!":
        return text

    # Check if text has fewer than 10 lines (skip in test mode)
    line_count = text.count('\n')
    if line_count < 10 and title != "test!":
        echo_test("less than 10 lines\n")

    # Replace <references /> with {{listaref}}
    if "<references />" in text:
        text = text.replace("<references />", "{{listaref}}")

    # Apply transformations
    newtext = text
    newtext = fix_es_months_in_refs(newtext)
    newtext = fix_temps(newtext)
    newtext = mv_es_refs(newtext)
    return newtext
