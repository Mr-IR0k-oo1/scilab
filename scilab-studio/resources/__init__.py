"""
Resources package for Scilab Studio foundation.

Provides helper utilities to locate assets, QSS style templates, and icons.
"""

from pathlib import Path

RESOURCES_DIR = Path(__file__).parent.resolve()
STYLES_DIR = RESOURCES_DIR / "styles"


def get_resource_path(relative_path: str) -> Path:
    """Return absolute path for a resource asset."""
    return RESOURCES_DIR / relative_path


def get_style_path(theme_name: str) -> Path:
    """Return absolute path for a theme QSS stylesheet."""
    return STYLES_DIR / f"{theme_name}.qss"
