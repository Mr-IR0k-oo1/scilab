"""
Theme Manager for Scilab Studio PySide6 UI shell.

Provides Dark, Light, and System QSS theme loading, runtime switching, and broadcasting.
"""

from enum import Enum
import logging
from typing import Optional
from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QApplication

from core.service_registry import IService
from core.event_bus import Event, EventBus
from core.configuration import ConfigurationManager
from resources import get_style_path

logger = logging.getLogger(__name__)


class ThemeMode(Enum):
    """Supported UI themes."""
    DARK = "dark"
    LIGHT = "light"
    SYSTEM = "system"


class ThemeManager(IService):
    """
    Service managing application QSS stylesheet injection and theme state.
    """

    def __init__(
        self,
        config_mgr: Optional[ConfigurationManager] = None,
        event_bus: Optional[EventBus] = None,
    ) -> None:
        self._current_mode = ThemeMode.DARK
        self._config_mgr = config_mgr
        self._event_bus = event_bus

    @property
    def current_mode(self) -> ThemeMode:
        """Get active theme mode."""
        return self._current_mode

    def set_dependencies(self, config_mgr: ConfigurationManager, event_bus: EventBus) -> None:
        """Inject runtime dependencies."""
        self._config_mgr = config_mgr
        self._event_bus = event_bus

    def initialize(self) -> None:
        """Load default theme mode from configuration."""
        if self._config_mgr is not None:
            theme_str = self._config_mgr.config.ui.theme.lower()
            if theme_str == "light":
                self._current_mode = ThemeMode.LIGHT
            elif theme_str == "system":
                self._current_mode = ThemeMode.SYSTEM
            else:
                self._current_mode = ThemeMode.DARK
        logger.info("ThemeManager initialized with mode: %s", self._current_mode.value)

    def start(self) -> None:
        """Activate theme service."""
        logger.info("ThemeManager started.")

    def stop(self) -> None:
        """Save active theme mode into configuration."""
        if self._config_mgr is not None:
            self._config_mgr.update_ui_config(theme=self._current_mode.value)

    def dispose(self) -> None:
        """Release theme manager resources."""
        logger.debug("ThemeManager disposed.")

    def resolve_effective_theme(self, mode: ThemeMode) -> str:
        """Resolve effective theme string ('dark' or 'light') when mode is SYSTEM."""
        if mode == ThemeMode.SYSTEM:
            try:
                hints = QGuiApplication.styleHints()
                if hasattr(hints, "colorScheme") and hints.colorScheme() == Qt.ColorScheme.Light:
                    return "light"
            except Exception:
                pass
            return "dark"
        return mode.value

    def apply_theme(self, app: QApplication, mode: ThemeMode) -> None:
        """
        Apply specified ThemeMode QSS stylesheet to QApplication.
        
        Args:
            app: Active PySide6 QApplication instance.
            mode: Target ThemeMode (DARK, LIGHT, or SYSTEM).
        """
        effective_name = self.resolve_effective_theme(mode)
        qss_path = get_style_path(effective_name)
        if not qss_path.exists():
            logger.error("QSS file not found: %s", qss_path)
            return

        try:
            with open(qss_path, "r", encoding="utf-8") as f:
                stylesheet = f.read()
            app.setStyleSheet(stylesheet)
            self._current_mode = mode
            logger.info("Applied theme '%s' (effective: %s) to application.", mode.value, effective_name)

            if self._config_mgr is not None:
                self._config_mgr.update_ui_config(theme=mode.value)

            if self._event_bus is not None:
                self._event_bus.publish(
                    Event(
                        topic="theme.changed",
                        payload={"mode": mode.value, "effective": effective_name},
                        sender="ThemeManager",
                    )
                )
        except Exception as exc:
            logger.exception("Failed to apply theme '%s': %s", mode.value, exc)

    def toggle_theme(self, app: QApplication) -> ThemeMode:
        """Toggle through Dark -> Light -> System -> Dark."""
        if self._current_mode == ThemeMode.DARK:
            new_mode = ThemeMode.LIGHT
        elif self._current_mode == ThemeMode.LIGHT:
            new_mode = ThemeMode.SYSTEM
        else:
            new_mode = ThemeMode.DARK

        self.apply_theme(app, new_mode)
        return new_mode
