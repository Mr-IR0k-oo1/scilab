"""
Application class for Scilab Studio PySide6 foundation.

Subclasses PySide6 QApplication, handling Qt signal bindings, exception trapping,
and graceful application exit hooks.
"""

import logging
import sys
from typing import List, Optional
from PySide6.QtWidgets import QApplication

from core.runtime import RuntimeContext
from ui.theme import ThemeManager, ThemeMode

logger = logging.getLogger(__name__)


class ScilabStudioApplication(QApplication):
    """
    Custom PySide6 QApplication managing Qt event loop and shutdown sequence.
    """

    def __init__(self, sys_argv: List[str], runtime_context: RuntimeContext) -> None:
        super().__init__(sys_argv)
        self._runtime_context = runtime_context

        self.setApplicationName("Scilab Studio")
        self.setApplicationVersion("0.1.0")
        self.setOrganizationName("Scilab-Studio")
        self.setOrganizationDomain("scilab-studio.org")

        self.aboutToQuit.connect(self._on_about_to_quit)

        # Apply default theme
        theme_mgr = self._runtime_context.get_service(ThemeManager)
        theme_mgr.apply_theme(self, theme_mgr.current_mode)

    def _on_about_to_quit(self) -> None:
        """Handle Qt application exit hook and trigger orderly service teardown."""
        logger.info("Application about to quit. Initiating graceful shutdown...")
        self._runtime_context.lifecycle.stop()
        self._runtime_context.service_registry.stop_all()
        self._runtime_context.service_registry.dispose_all()
        self._runtime_context.lifecycle.dispose()
        logger.info("Graceful shutdown completed.")
