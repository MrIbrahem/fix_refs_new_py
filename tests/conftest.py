"""Configuration and fixtures for pytest"""

import sys
from collections.abc import Callable
from pathlib import Path

import pytest

# Get the project root directory (parent of pytests folder)
project_root = Path(__file__).parent.parent

# Add python_src to sys.path so we can import from 'fix_refs' as a package
python_src_path = project_root  # / "fix_refs"
sys.path.insert(0, str(python_src_path))


@pytest.fixture
def load_fixture() -> Callable[[str], str]:
    def loader(name: str) -> str:
        path = Path(__file__).parent / name
        assert path.exists(), f"Fixture file missing: {path}"

        return path.read_text(encoding="utf-8")

    return loader
