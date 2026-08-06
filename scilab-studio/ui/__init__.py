"""
Scilab Studio UI Package.

Contains PySide6 Qt main window shell, toolbar, sidebar explorer, statusbar,
docking layout manager, and theme engine.
"""

from .theme import ThemeManager, ThemeMode
from .docking import DockManager
from .sidebar import SidebarPanel
from .toolbar import MainToolBar
from .statusbar import MainStatusBar
from .main_window import MainWindow

__all__ = [
    "ThemeManager",
    "ThemeMode",
    "DockManager",
    "SidebarPanel",
    "MainToolBar",
    "MainStatusBar",
    "MainWindow",
]
