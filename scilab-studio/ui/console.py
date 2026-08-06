"""
Logging Console panel for Scilab Studio PySide6 UI shell.

Bottom dock widget displaying real-time system & module log streams,
providing filtering by severity level, text search, log clearance, and export.
"""

import datetime
import logging
from typing import Optional
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from core.event_bus import Event, EventBus

logger = logging.getLogger(__name__)


class LoggingConsolePanel(QWidget):
    """
    Structured Logging Console with table view, search, filtering, and export.
    """

    def __init__(self, event_bus: Optional[EventBus] = None, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._event_bus = event_bus

        self._setup_ui()
        self._register_event_handlers()

    def _setup_ui(self) -> None:
        """Construct control toolbar and log record table."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(4, 4, 4, 4)

        # Controls bar
        ctrl_layout = QHBoxLayout()

        ctrl_layout.addWidget(QLabel("Level Filter:", self))
        self._level_filter = QComboBox(self)
        self._level_filter.addItems(["ALL", "INFO", "WARNING", "ERROR", "DEBUG"])
        self._level_filter.currentTextChanged.connect(self._apply_filters)
        ctrl_layout.addWidget(self._level_filter)

        ctrl_layout.addWidget(QLabel("Search:", self))
        self._search_input = QLineEdit(self)
        self._search_input.setPlaceholderText("Filter log messages...")
        self._search_input.textChanged.connect(self._apply_filters)
        ctrl_layout.addWidget(self._search_input)

        ctrl_layout.addStretch()

        self._clear_btn = QPushButton("🗑️ Clear", self)
        self._clear_btn.clicked.connect(self.clear_logs)
        ctrl_layout.addWidget(self._clear_btn)

        self._export_btn = QPushButton("💾 Export Log...", self)
        self._export_btn.clicked.connect(self.export_logs)
        ctrl_layout.addWidget(self._export_btn)

        main_layout.addLayout(ctrl_layout)

        # Log Table
        self._table = QTableWidget(0, 4, self)
        self._table.setHorizontalHeaderLabels(["Timestamp", "Level", "Module", "Message"])
        self._table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self._table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self._table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self._table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self._table.setAlternatingRowColors(True)

        main_layout.addWidget(self._table)

    def _register_event_handlers(self) -> None:
        """Subscribe to logger.entry topic."""
        if self._event_bus is not None:
            self._event_bus.subscribe("logger.entry", self._on_log_entry)

    def _on_log_entry(self, event: Event) -> None:
        """Event handler appending log record to table."""
        level = str(event.payload.get("level", "INFO")).upper()
        msg = str(event.payload.get("message", ""))
        logger_name = str(event.payload.get("logger_name", "system"))
        ts = event.payload.get("timestamp", 0)

        dt_str = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S.%f")[:-3] if ts else "--:--:--"

        row = self._table.rowCount()
        self._table.insertRow(row)

        ts_item = QTableWidgetItem(dt_str)
        level_item = QTableWidgetItem(level)
        mod_item = QTableWidgetItem(logger_name)
        msg_item = QTableWidgetItem(msg)

        # Level coloring
        if level == "ERROR":
            level_item.setForeground(Qt.GlobalColor.red)
        elif level == "WARNING":
            level_item.setForeground(Qt.GlobalColor.yellow)
        elif level == "DEBUG":
            level_item.setForeground(Qt.GlobalColor.gray)
        else:
            level_item.setForeground(Qt.GlobalColor.green)

        self._table.setItem(row, 0, ts_item)
        self._table.setItem(row, 1, level_item)
        self._table.setItem(row, 2, mod_item)
        self._table.setItem(row, 3, msg_item)

        self._apply_row_visibility(row, level, msg, logger_name)

        # Auto-scroll
        self._table.scrollToBottom()

    def _apply_filters(self) -> None:
        """Filter table rows based on dropdown level and text search."""
        target_level = self._level_filter.currentText()
        search_text = self._search_input.text().lower()

        for row in range(self._table.rowCount()):
            level_item = self._table.item(row, 1)
            msg_item = self._table.item(row, 3)
            mod_item = self._table.item(row, 2)

            level = level_item.text() if level_item else ""
            msg = msg_item.text() if msg_item else ""
            mod = mod_item.text() if mod_item else ""

            self._apply_row_visibility(row, level, msg, mod)

    def _apply_row_visibility(self, row: int, level: str, msg: str, mod: str) -> None:
        target_level = self._level_filter.currentText()
        search_text = self._search_input.text().lower()

        match_level = (target_level == "ALL") or (level == target_level)
        match_search = (not search_text) or (search_text in msg.lower() or search_text in mod.lower())

        self._table.setRowHidden(row, not (match_level and match_search))

    def clear_logs(self) -> None:
        """Purge table contents."""
        self._table.setRowCount(0)

    def export_logs(self) -> None:
        """Export current log entries to file."""
        chosen, _ = QFileDialog.getSaveFileName(self, "Export Log Stream", "scilab_studio.log", "Log Files (*.log *.txt)")
        if not chosen:
            return

        try:
            with open(chosen, "w", encoding="utf-8") as f:
                for row in range(self._table.rowCount()):
                    if not self._table.isRowHidden(row):
                        ts = self._table.item(row, 0).text()
                        lvl = self._table.item(row, 1).text()
                        mod = self._table.item(row, 2).text()
                        msg = self._table.item(row, 3).text()
                        f.write(f"[{ts}] [{lvl}] [{mod}]: {msg}\n")
            logger.info("Exported log stream to %s", chosen)
        except Exception as exc:
            logger.exception("Failed to export log stream to %s: %s", chosen, exc)
