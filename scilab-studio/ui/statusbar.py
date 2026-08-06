"""
Main Status Bar for Scilab Studio PySide6 UI shell.

Displays active project status, memory utilization monitor, theme indicator,
and system status messages.
"""

import logging
import os
try:
    import psutil
except ImportError:
    psutil = None

from typing import Optional
from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import QLabel, QStatusBar, QWidget

from core.event_bus import Event, EventBus

logger = logging.getLogger(__name__)


class MainStatusBar(QStatusBar):
    """
    Bottom Status Bar component.
    """

    def __init__(self, event_bus: Optional[EventBus] = None, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("MainStatusBar")
        self._event_bus = event_bus

        self._setup_ui()
        self._register_event_handlers()

        # Update memory usage periodically
        self._timer = QTimer(self)
        self._timer.setInterval(3000)  # Every 3 seconds
        self._timer.timeout.connect(self._update_memory_usage)
        self._timer.start()

    def _setup_ui(self) -> None:
        """Construct status bar label widgets."""
        self._status_label = QLabel("Ready", self)
        self.addWidget(self._status_label, 1)

        self._memory_label = QLabel("RAM: -- MB", self)
        self._memory_label.setStyleSheet("padding: 0 10px;")
        self.addPermanentWidget(self._memory_label)

        self._theme_label = QLabel("Theme: Dark", self)
        self._theme_label.setStyleSheet("padding: 0 10px;")
        self.addPermanentWidget(self._theme_label)

        self._health_label = QLabel("● Core Engine: Ready", self)
        self._health_label.setStyleSheet("padding: 0 10px; color: #4caf50;")
        self.addPermanentWidget(self._health_label)

        self._update_memory_usage()

    def _register_event_handlers(self) -> None:
        """Subscribe to status events."""
        if self._event_bus is not None:
            self._event_bus.subscribe("workspace.opened", self._on_workspace_opened)
            self._event_bus.subscribe("workspace.closed", self._on_workspace_closed)
            self._event_bus.subscribe("theme.changed", self._on_theme_changed)

    def _on_workspace_opened(self, event: Event) -> None:
        """Update status label when workspace opens a project."""
        name = event.payload.get("name", "Project")
        self._status_label.setText(f"Project: {name}")

    def _on_workspace_closed(self, event: Event) -> None:
        """Reset status label when project closes."""
        self._status_label.setText("Ready")

    def _on_theme_changed(self, event: Event) -> None:
        """Update theme mode label."""
        mode = event.payload.get("mode", "dark").capitalize()
        self._theme_label.setText(f"Theme: {mode}")

    def _update_memory_usage(self) -> None:
        """Update process RAM utilization label."""
        try:
            process = psutil.Process(os.getpid())
            mem_mb = process.memory_info().rss / (1024 * 1024)
            self._memory_label.setText(f"RAM: {mem_mb:.1f} MB")
        except Exception:
            self._memory_label.setText("RAM: -- MB")
