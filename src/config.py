import os
from pathlib import Path

home = os.getenv("HOME", str(Path.home()))

html_path = Path("I:/medwiki/new/medwiki.toolforge.org_repo/public_html")

if not html_path.exists():
    html_path = Path(home) / "public_html"

revisions_path = html_path / "revisions_new"

if not revisions_path.exists():
    revisions_path = Path(__file__).parent.parent.parent.parent / "resources/revisions"
