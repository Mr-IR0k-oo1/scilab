"""
Toast Notification overlay manager for Scilab Studio PySide6 UI shell.

Displays sleek, non-blocking toast popups for Success, Warning, Error, and Info alerts.
"""

import logging
from typing import Optional
from PySide6.QtCore import QPropertyAnimation, QSequentialAnimationGroup, QTimer, Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from core.event_bus import Event, EventBus

logger = logging.getLogger(__name__)


class ToastWidget(QFrame):
    """Individual Toast Alert Popup Box."""

    def __init__(self, title: str, message: str, type_: str = "info", parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.SubWindow)
        self.setFrameShape(QFrame.Shape.StyledPanel)

        # Style based on notification type
        if type_ == "success":
            bg_color, border_color, icon_str = "#1b4d2e", "#2e7d32", "✓"
        elif type_ == "warning":
            bg_color, border_color, icon_str = "#4a3b00", "#f57f17", "⚠️"
        elif type_ == "error":
            bg_color, border_color, icon_str = "#4a1212", "#c62828", "❌"
        else:
            bg_color, border_color, icon_str = "#0d3b66", "#0288d1", "ℹ️"

        self.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border: 1px solid {border_color};
                border-radius: 4px;
                color: #ffffff;
                padding: 6px;
            }}
            QLabel {{
                background: transparent;
                color: #ffffff;
            }}
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(10)

        icon_lbl = QLabel(icon_str, self)
        icon_lbl.setStyleSheet("font-size: 16px;")
        layout.addWidget(icon_lbl)

        content_layout = QVBoxLayout()
        content_layout.setSpacing(2)

        title_lbl = QLabel(f"<b>{title}</b>", self)
        msg_lbl = QLabel(message, self)
        msg_lbl.setStyleSheet("font-size: 11px; color: #dddddd;")

        content_layout.addWidget(title_lbl)
        content_layout.addWidget(msg_lbl)

        layout.addLayout(content_layout)


class ToastOverlayManager(QWidget):
    """
    Overlay manager floating toast notifications in the top-right corner of MainWindow.
    """

    def __init__(self, parent_window: QWidget, event_bus: Optional[EventBus] = None) -> None:
        super().__init__(parent_window)
        self._parent_window = parent_window
        self._event_bus = event_bus

        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(8)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)

        self._register_event_handlers()

    def _register_event_handlers(self) -> None:
        """Subscribe to notification.show events."""
        if self._event_bus is not None:
            self._event_bus.subscribe("notification.show", self._on_notification_show)

    def _on_notification_show(self, event: Event) -> None:
        """Create and animate toast popup widget."""
        title = str(event.payload.get("title", "Notification"))
        message = str(event.payload.get("message", ""))
        type_ = str(event.payload.get("type", "info"))
        duration_ms = int(event.payload.get("duration_ms", 4000))

        toast = ToastWidget(title, message, type_, self)
        toast.setFixedWidth(300)
        self._layout.addWidget(toast)

        # Auto-dismiss timer
        QTimer.singleShot(duration_ms, lambda: self._dismiss_toast(toast))

    def _dismiss_toast(self, toast: ToastWidget) -> None:
        """Remove toast popup widget."""
        self._layout.removeWidget(toast)
        toast.deleteLater()
