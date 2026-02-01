import os
from pathlib import Path
from dotenv import load_dotenv

_env_file_path = None

try:
    load_dotenv()
except Exception:
    _HOME = os.getenv("HOME")
    if _HOME:
        _env_file_path = Path(f"{_HOME}/.env")
        load_dotenv(_env_file_path)

resources_path = Path(os.getenv("RESOURCES_PATH", Path(__file__).parent.parent / "resources")).expanduser()
revisions_path = Path(os.getenv("REVISIONS_PATH", Path(resources_path) / "revisions")).expanduser()
