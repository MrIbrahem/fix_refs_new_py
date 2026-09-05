import functools
import json
import os

from ..config import resources_path
from ..utils.http import get_url


def load_settings_from_file() -> dict:
    file_path = resources_path / "language_settings.json"
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def load_settings_from_server(server_name) -> dict:
    url = "http://localhost:9001/api.php?get=language_settings"
    if server_name == "mdwiki.toolforge.org":
        url = "https://mdwiki.toolforge.org/api.php?get=language_settings"

    json_data = get_url(url)

    try:
        data = json.loads(json_data)
    except json.JSONDecodeError:
        data = {}
    return data


@functools.lru_cache(maxsize=1)
def load_settings() -> dict:
    server_name = os.environ.get("SERVER_NAME", "")
    if server_name:
        data = load_settings_from_server(server_name)
    else:
        data = load_settings_from_file()

    results = data.get("results", [])
    # {"lang_code": "aa", "move_dots": 0, "expend": 0, "add_en_lang": 0}, {"lang_code": "ab", "move_dots": 0, "expend": 1, "add_en_lang": 0}
    new = {}

    for value in results:
        lang_code = value.get("lang_code")
        if lang_code:
            new[lang_code] = value

    return new


__all__ = [
    "load_settings_from_file",
    "load_settings_from_server",
    "load_settings",
]
