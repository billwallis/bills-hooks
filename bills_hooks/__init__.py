"""
Pre-commit hooks for my own projects.
"""

import pathlib

PROJECT_ROOT = pathlib.Path(__file__).parent.parent  # resolves to `bills-hooks/`
SOURCE_ROOT = PROJECT_ROOT / "bills_hooks"
