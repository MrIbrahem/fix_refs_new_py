"""
Armenian-specific bot fixes
"""

import re
from typing import Optional


def str_ends_with(string: str, end_string: str) -> bool:
    """Check if string ends with substring"""
    return string.endswith(end_string)


def str_starts_with(text: str, start: str) -> bool:
    """Check if string starts with substring"""
    return text.startswith(start)


def remove_spaces_between_ref_and_punctuation(text: str, lang: Optional[str] = None) -> str:
    """Remove spaces between ref tags and punctuation

    Args:
        text: WikiText content
        lang: Language code

    Returns:
        Text with spaces removed
    """
    # Use superset of punctuation across supported languages
    dots = ".,。։।:"
    cls = re.escape(dots)

    # Keep punctuation right after <ref ... /> with no space
    # Pattern: <ref[^>]*/>\s*[punctuation]
    text = re.sub(r'(<ref[^>]*\/>)\s*([' + cls + r'])', r'\1\2', text)

    # Normalize endings: </ref> followed by any punctuation remains attached
    # Pattern: </ref>\s*[punctuation]
    text = re.sub(r'<\/ref>\s*([' + cls + r'])', r'</ref>\1', text)

    return text


def get_parts(newtext: str, charters: str) -> list:
    """Split text by double newlines and find parts ending with punctuation

    Args:
        newtext: Text to process
        charters: Punctuation characters to match

    Returns:
        List of [part, char] pairs
    """
    matches = newtext.split("\n\n")

    if len(matches) == 1:
        matches = newtext.split("\r\n\r\n")

    new_parts = []

    for part in matches:
        # Match </ref> or /> followed by punctuation at end
        pattern = r'(?:<\/ref>|\/>)\s*([' + re.escape(charters) + r'])\s*$'
        match = re.search(pattern, part, re.MULTILINE)
        if match:
            new_parts.append([part, match.group(1)])

    return new_parts


def remove_spaces_between_last_word_and_beginning_of_ref(newtext: str, lang: str) -> str:
    """Remove spaces around refs in specific patterns

    This function removes spaces in several patterns:
    1. 'word <ref /> :' -> 'word<ref />:' (space between ref/punct)
    2. 'word  <ref />:' -> 'word<ref />:' (multiple spaces before ref)
    3. At end of text with content ref: 'word <ref>...</ref>:$' -> 'word<ref>...</ref>:$'

    Note: Pattern 3 only applies when the last ref is a content ref (>...</ref>),
    not a self-closing ref (/>).

    Args:
        newtext: Text to process
        lang: Language code

    Returns:
        Fixed text
    """
    # Define punctuation marks based on language
    if lang == "hy":
        dots = r".,。։:"
    else:
        dots = r".,।"

    # Pattern 1: space between ref ending and punctuation - remove all spaces
    # Use [^<]* for simple refs, pattern won't match complex nested content
    pattern1 = r'(\S)(\s+)((?:<ref[^>]*(?:/\s*>|>[^<]*</ref>))+)(\s+)([' + re.escape(dots) + r'])'

    def replace_func1(match):
        return match.group(1) + match.group(3) + match.group(5)

    newtext = re.sub(pattern1, replace_func1, newtext)

    # Pattern 2: multiple spaces (2+) before ref followed by punctuation
    pattern2 = r'(\S)(\s{2,})((?:<ref[^>]*(?:/\s*>|>[^<]*</ref>))+)([' + re.escape(dots) + r'])'

    def replace_func2(match):
        return match.group(1) + match.group(3) + match.group(4)

    newtext = re.sub(pattern2, replace_func2, newtext)

    # Pattern 3: at end of text with CONTENT ref - handle manually to avoid greedy matching
    # Find last punctuation character
    last_punct_pos = -1
    for c in dots:
        pos = newtext.rfind(c)
        if pos > last_punct_pos:
            last_punct_pos = pos

    if last_punct_pos >= 0:
        before_punct = newtext[:last_punct_pos]
        after_punct = newtext[last_punct_pos:]

        stripped_before = before_punct.rstrip()

        # Pattern 3a: ends with content ref (</ref>)
        if stripped_before.endswith('</ref>'):
            # Look for pattern: word + space + consecutive refs at end
            # single_ref pattern explanation:
            #   <ref[^>]*          - Match <ref followed by any attributes (but not >)
            #   (?:                - Non-capturing group for alternatives:
            #     /\s*>            - Self-closing ref: /> with optional whitespace
            #     |                - OR
            #     >                - Opening > for content ref
            #     (?:              - Content matching (non-greedy, doesn't cross refs):
            #       (?!<ref)[^<]   - Any non-< char that's not start of <ref
            #       |<(?!ref)      - Or < not followed by 'ref'
            #     )*               - Zero or more content chars
            #     </ref>           - Closing tag
            #   )
            single_ref = r'<ref[^>]*(?:/\s*>|>(?:(?!<ref)[^<]|<(?!ref))*</ref>)'
            end_pattern = r'(\S)(\s+)((?:' + single_ref + r')+)$'
            match = re.search(end_pattern, before_punct)

            if match:
                # Check if this match is for consecutive refs (no text between refs)
                refs_text = match.group(3)
                # Strip ref tags and templates to check for intervening text
                # Combine into single regex for efficiency
                refs_stripped = re.sub(r'<ref[^>]*>|</ref>|\{\{[^}]*\}\}', '', refs_text)
                # Check for any letter characters (indicates text between refs)
                has_text_between = bool(re.search(r'[a-zA-Z]', refs_stripped))

                if not has_text_between:
                    # Replace: remove space before refs
                    new_before = before_punct[:match.start()] + match.group(1) + match.group(3)
                    newtext = new_before + after_punct

        # Pattern 3b: ends with single self-closing ref (/>) - only if it's a SINGLE ref
        elif stripped_before.endswith('/>'):
            # Check for single ref (not multiple consecutive refs)
            # Pattern: word + space + single self-closing ref at end
            single_ref_pattern = r'(\S)(\s+)(<ref[^>]*/\s*>)$'
            match = re.search(single_ref_pattern, before_punct)

            if match:
                # Only process if this is a single ref (no other ref immediately before)
                before_match = before_punct[:match.start()]
                # Check that the text before doesn't end with a ref
                if not before_match.rstrip().endswith(('</ref>', '/>')):
                    # Replace: remove space before single ref
                    new_before = before_punct[:match.start()] + match.group(1) + match.group(3)
                    newtext = new_before + after_punct

    return newtext


def hy_fixes(text: str) -> str:
    """Apply Armenian-specific fixes to text

    Args:
        text: WikiText content

    Returns:
        Fixed text
    """
    text = remove_spaces_between_last_word_and_beginning_of_ref(text, "hy")
    text = remove_spaces_between_ref_and_punctuation(text, "hy")
    return text
