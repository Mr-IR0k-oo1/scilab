"""
Scilab Studio Application Package.

Contains bootstrap initialization, PySide6 QApplication subclass,
and application main entry point.
"""

from .bootstrap import Bootstrap
from .application import ScilabStudioApplication

__all__ = ["Bootstrap", "ScilabStudioApplication"]
