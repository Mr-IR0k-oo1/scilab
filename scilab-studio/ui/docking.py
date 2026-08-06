"""
Dock Layout Manager for Scilab Studio PySide6 UI shell.

Wraps QDockWidget operations, floating panels, docking, layout preset resets,
and base64 state serialization for workspace & configuration storage.
"""

import base64
import logging
from typing import Dict, Optional
from PySide6.QtCore import Qt, QByteArray
from PySide6.QtWidgets import QDockWidget, QMainWindow

logger = logging.getLogger(__name__)


class DockManager:
    """
    Manager governing QDockWidget instances on QMainWindow.
    """

    def __init__(self, main_window: QMainWindow) -> None:
        self._main_window = main_window
        self._docks: Dict[str, QDockWidget] = {}
        self._default_state: Optional[QByteArray] = None

        # Enable nested and tabbed docking options on QMainWindow
        self._main_window.setDockOptions(
            QMainWindow.DockOption.AllowNestedDocks
            | QMainWindow.DockOption.AllowTabbedDocks
            | QMainWindow.DockOption.AnimatedDocks
        )

    def register_dock(
        self,
        dock_id: str,
        dock_widget: QDockWidget,
        area: Qt.DockWidgetArea = Qt.DockWidgetArea.LeftDockWidgetArea,
    ) -> None:
        """
        Register and attach a QDockWidget to the QMainWindow.
        
        Args:
            dock_id: Unique string identifier for the dock.
            dock_widget: QDockWidget instance.
            area: Initial Qt DockWidgetArea placement.
        """
        dock_widget.setObjectName(dock_id)
        self._docks[dock_id] = dock_widget
        self._main_window.addDockWidget(area, dock_widget)
        logger.debug("Registered dock '%s' in area %s", dock_id, area)

    def save_default_preset(self) -> None:
        """Capture default layout state after initialization."""
        self._default_state = self._main_window.saveState()

    def reset_layout(self) -> None:
        """Restore initial default dock layout preset."""
        if self._default_state is not None:
            self._main_window.restoreState(self._default_state)
            # Ensure all registered docks are visible
            for dock in self._docks.values():
                dock.show()
                dock.setFloating(False)
            logger.info("Reset dock layout to default preset.")

    def set_floating(self, dock_id: str, floating: bool = True) -> None:
        """Set floating status of a dock panel."""
        dock = self._docks.get(dock_id)
        if dock is not None:
            dock.setFloating(floating)

    def show_dock(self, dock_id: str) -> None:
        """Show a dock panel."""
        dock = self._docks.get(dock_id)
        if dock is not None:
            dock.show()
            dock.raise_()

    def hide_dock(self, dock_id: str) -> None:
        """Hide a dock panel."""
        dock = self._docks.get(dock_id)
        if dock is not None:
            dock.hide()

    def get_dock(self, dock_id: str) -> Optional[QDockWidget]:
        """Retrieve a registered QDockWidget by ID."""
        return self._docks.get(dock_id)

    def toggle_dock(self, dock_id: str, visible: Optional[bool] = None) -> None:
        """Toggle dock visibility state."""
        dock = self._docks.get(dock_id)
        if dock is not None:
            if visible is None:
                dock.setVisible(not dock.isVisible())
            else:
                dock.setVisible(visible)

    def save_state(self) -> QByteArray:
        """Serialize current dock state and geometry."""
        return self._main_window.saveState()

    def restore_state(self, state: QByteArray) -> bool:
        """Restore dock layout state from QByteArray."""
        return self._main_window.restoreState(state)

    def save_layout_b64(self) -> str:
        """Serialize dock layout state as a base64 encoded string."""
        raw_bytes = bytes(self.save_state())
        return base64.b64encode(raw_bytes).decode("ascii")

    def restore_layout_b64(self, layout_b64: str) -> bool:
        """Restore dock layout from a base64 encoded string."""
        if not layout_b64:
            return False
        try:
            raw_bytes = base64.b64decode(layout_b64.encode("ascii"))
            return self.restore_state(QByteArray(raw_bytes))
        except Exception as exc:
            logger.exception("Failed to restore layout from base64 string: %s", exc)
            return False
