"""
Fix missing images by checking Wikimedia Commons and clearing invalid image references
"""

import urllib.parse
from typing import Optional
from functools import lru_cache
import wikitextparser as wtp
from ..utils.http import get_url_json


# User-Agent for Wikimedia API requests (required by Wikimedia policy)
USER_AGENT = "fix_refs_bot/1.0 (https://github.com/MrIbrahem/fix_refs_new_py)"

# Image parameter patterns (image, image2, image3, etc.)
IMAGE_PARAM_PATTERNS = ['image', 'image2', 'image3', 'image4', 'image5']
CAPTION_PARAM_PATTERNS = ['caption', 'caption2', 'caption3', 'caption4', 'caption5']


def check_commons_image_exists(filename: str, timeout: int = 10) -> bool:
    """Check if an image exists on Wikimedia Commons

    Args:
        filename: Image filename (with or without File: prefix)
        timeout: Request timeout in seconds

    Returns:
        True if image exists, False otherwise
        Returns True on API failure to avoid removing valid images
    """
    if not filename or not filename.strip():
        return False

    # Clean up filename
    filename = filename.strip()

    # Remove File: or Image: prefix if present
    for prefix in ['File:', 'file:', 'Image:', 'image:']:
        if filename.startswith(prefix):
            filename = filename[len(prefix):]
            break

    # Build API URL
    params = urllib.parse.urlencode({
        'action': 'query',
        'titles': f'File:{filename}',
        'format': 'json'
    })
    url = f"https://commons.wikimedia.org/w/api.php?{params}"

    data = get_url_json(url, timeout=timeout)
    if not data:
        # On API error, assume image exists to avoid false positives
        return True

    pages = data.get('query', {}).get('pages', {})
    for page in pages.values():
        # If 'missing' key exists, file doesn't exist
        return 'missing' not in page

    return True


@lru_cache(maxsize=1000)
def check_commons_image_exists_cached(filename: str) -> bool:
    """Cached version of check_commons_image_exists

    Uses LRU cache to avoid repeated API calls for the same filename.

    Args:
        filename: Image filename

    Returns:
        True if image exists, False otherwise
    """
    return check_commons_image_exists(filename)


def clear_image_cache() -> None:
    """Clear the image existence cache"""
    check_commons_image_exists_cached.cache_clear()


def _get_image_param_number(param_name: str) -> Optional[str]:
    """Extract the number suffix from image/caption parameter

    Args:
        param_name: Parameter name like 'image', 'image2', 'caption3'

    Returns:
        Number suffix or empty string for base param, None if not an image/caption param
    """
    param_lower = param_name.strip().lower()

    # Check image params
    if param_lower == 'image':
        return ''
    if param_lower.startswith('image') and param_lower[5:].isdigit():
        return param_lower[5:]

    # Check caption params
    if param_lower == 'caption':
        return ''
    if param_lower.startswith('caption') and param_lower[7:].isdigit():
        return param_lower[7:]

    return None


def _find_caption_arg(template: wtp.Template, number: str) -> Optional[wtp.Argument]:
    """Find the caption argument matching an image number

    Args:
        template: wikitextparser Template object
        number: Number suffix ('' for base, '2' for image2, etc.)

    Returns:
        Caption argument or None
    """
    caption_name = f'caption{number}' if number else 'caption'

    for arg in template.arguments:
        if arg.name.strip().lower() == caption_name.lower():
            return arg

    return None


def remove_missing_infobox_images(text: str, use_cache: bool = False) -> str:
    """Remove infobox images that don't exist on Commons

    Sets image and caption values to empty instead of removing the parameters.

    Args:
        text: WikiText containing templates
        use_cache: Whether to use cached API results

    Returns:
        Text with missing image values cleared
    """
    parsed = wtp.parse(text)
    check_fn = check_commons_image_exists_cached if use_cache else check_commons_image_exists

    for template in parsed.templates:
        # Process each argument looking for image parameters
        for arg in template.arguments:
            param_name = arg.name.strip().lower()

            # Check if this is an image parameter
            if not (param_name == 'image' or
                    (param_name.startswith('image') and param_name[5:].isdigit())):
                continue

            image_value = arg.value.strip()

            # Skip if already empty
            if not image_value:
                continue

            # Check if image exists on Commons
            if not check_fn(image_value):
                # Set image value to empty
                arg.value = ''

                # Find and clear corresponding caption
                number = param_name[5:] if len(param_name) > 5 else ''
                caption_arg = _find_caption_arg(template, number)
                if caption_arg:
                    caption_arg.value = ''

    return parsed.string


def _extract_filename_from_wikilink(wikilink: wtp.WikiLink) -> Optional[str]:
    """Extract filename from a File/Image wikilink

    Args:
        wikilink: wikitextparser WikiLink object

    Returns:
        Filename or None if not a file link
    """
    target = wikilink.target.strip()

    # Check if it's a File: or Image: link
    target_lower = target.lower()
    if target_lower.startswith('file:'):
        return target[5:].strip()
    elif target_lower.startswith('image:'):
        return target[6:].strip()

    return None


def remove_missing_inline_images(text: str, use_cache: bool = False) -> str:
    """Remove inline [[File:...]] images that don't exist on Commons

    Args:
        text: WikiText containing wikilinks
        use_cache: Whether to use cached API results

    Returns:
        Text with missing file links removed
    """
    parsed = wtp.parse(text)
    check_fn = check_commons_image_exists_cached if use_cache else check_commons_image_exists

    # Process wikilinks in reverse order to maintain string positions
    for wikilink in reversed(parsed.wikilinks):
        filename = _extract_filename_from_wikilink(wikilink)

        if filename is None:
            continue

        # Check if image exists on Commons
        if not check_fn(filename):
            # Remove the entire wikilink
            wikilink.string = ''

    return parsed.string


def remove_missing_images(text: str) -> str:
    """Remove all missing images from text (both infobox and inline)

    Main function that processes both infobox-style images and inline [[File:...]] links.

    Args:
        text: WikiText content

    Returns:
        Text with missing images handled:
        - Infobox images: values set to empty
        - Inline images: wikilinks removed
    """
    text = remove_missing_infobox_images(text, use_cache=False)
    text = remove_missing_inline_images(text, use_cache=False)
    return text


def remove_missing_images_cached(text: str) -> str:
    """Remove all missing images using cached API calls

    Same as remove_missing_images but uses caching for API calls.
    Useful for batch processing multiple texts.

    Args:
        text: WikiText content

    Returns:
        Text with missing images handled
    """
    text = remove_missing_infobox_images(text, use_cache=True)
    text = remove_missing_inline_images(text, use_cache=True)
    return text
