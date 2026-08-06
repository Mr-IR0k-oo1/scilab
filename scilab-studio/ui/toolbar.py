"""
Main Toolbar for Scilab Studio PySide6 UI shell.

Provides fast access actions for workspace operations, theme toggling,
and execution triggers.
"""

import logging
from typing import Optional
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QToolBar, QWidget

logger = logging.getLogger(__name__)


class MainToolBar(QToolBar):
    """
    Main Action Toolbar displayed beneath Menu Bar.
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__("Main Toolbar", parent)
        self.setObjectName("MainToolBar")
        self.setMovable(False)
        self.setIconSize(QSize(18, 18))
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self._setup_actions()

    def _setup_actions(self) -> None:
        """Create toolbar action items."""
        self.action_new = QAction("➕ New Project", self)
        self.action_new.setToolTip("Create a new Scilab Studio project package (.scstudio)")
        self.addAction(self.action_new)

        self.action_open = QAction("📂 Open Project", self)
        self.action_open.setToolTip("Open an existing .scstudio project")
        self.addAction(self.action_open)

        self.action_save = QAction("💾 Save Project", self)
        self.action_save.setToolTip("Save current project changes")
        self.addAction(self.action_save)

        self.addSeparator()

        self.action_theme = QAction("🌓 Toggle Theme", self)
        self.action_theme.setToolTip("Switch between Dark and Light engineering themes")
        self.addAction(self.action_theme)

        self.addSeparator()

        self.action_scilab_console = QAction("⚡ Scilab Console", self)
        self.action_scilab_console.setToolTip("Focus Scilab interactive output console")
        self.addAction(self.action_scilab_console)
