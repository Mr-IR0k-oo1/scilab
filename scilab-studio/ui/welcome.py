"""
Welcome Screen Landing Page for Scilab Studio PySide6 UI shell.

Modern engineering landing page incorporating dynamic Recent Projects list,
New/Open Project triggers, Documentation, Examples, and Settings dialog actions.
"""

import logging
from typing import Callable, Optional
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from workspace.recent_projects import RecentProjectsStore

logger = logging.getLogger(__name__)


class WelcomeWidget(QWidget):
    """
    Modern Landing Page displayed in Central Workspace when no files are open.
    """

    def __init__(
        self,
        recent_store: Optional[RecentProjectsStore] = None,
        on_new_project_cb: Optional[Callable[[], None]] = None,
        on_open_project_cb: Optional[Callable[[], None]] = None,
        on_open_recent_cb: Optional[Callable[[str], None]] = None,
        on_open_settings_cb: Optional[Callable[[], None]] = None,
        on_open_docs_cb: Optional[Callable[[], None]] = None,
        on_open_examples_cb: Optional[Callable[[], None]] = None,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self._recent_store = recent_store
        self._on_new_project_cb = on_new_project_cb
        self._on_open_project_cb = on_open_project_cb
        self._on_open_recent_cb = on_open_recent_cb
        self._on_open_settings_cb = on_open_settings_cb
        self._on_open_docs_cb = on_open_docs_cb
        self._on_open_examples_cb = on_open_examples_cb

        self._setup_ui()
        self.refresh_recent_projects()

    def _setup_ui(self) -> None:
        """Construct landing page layout."""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)

        # Left Column: Quick Actions & Navigation
        left_col = QWidget(self)
        left_layout = QVBoxLayout(left_col)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(16)

        title = QLabel("Scilab Studio", left_col)
        font_title = QFont()
        font_title.setPointSize(26)
        font_title.setBold(True)
        title.setFont(font_title)

        subtitle = QLabel("Open Engineering Development Platform for Research & Industry", left_col)
        subtitle.setStyleSheet("color: #888888; font-size: 13px;")

        left_layout.addWidget(title)
        left_layout.addWidget(subtitle)
        left_layout.addSpacing(10)

        # Start Section
        start_lbl = QLabel("<b>START</b>", left_col)
        start_lbl.setStyleSheet("color: #aaaaaa; letter-spacing: 1px;")
        left_layout.addWidget(start_lbl)

        new_btn = QPushButton("➕ Create New Project", left_col)
        new_btn.setFixedHeight(38)
        new_btn.setStyleSheet("text-align: left; padding-left: 14px; font-size: 13px;")
        if self._on_new_project_cb:
            new_btn.clicked.connect(self._on_new_project_cb)
        left_layout.addWidget(new_btn)

        open_btn = QPushButton("📂 Open Project Folder", left_col)
        open_btn.setFixedHeight(38)
        open_btn.setStyleSheet("text-align: left; padding-left: 14px; font-size: 13px;")
        if self._on_open_project_cb:
            open_btn.clicked.connect(self._on_open_project_cb)
        left_layout.addWidget(open_btn)

        left_layout.addSpacing(10)

        # Resources & Settings Section
        res_lbl = QLabel("<b>RESOURCES & SETTINGS</b>", left_col)
        res_lbl.setStyleSheet("color: #aaaaaa; letter-spacing: 1px;")
        left_layout.addWidget(res_lbl)

        docs_btn = QPushButton("📖 Documentation & Tutorials", left_col)
        docs_btn.setFixedHeight(34)
        docs_btn.setStyleSheet("text-align: left; padding-left: 14px;")
        if self._on_open_docs_cb:
            docs_btn.clicked.connect(self._on_open_docs_cb)
        left_layout.addWidget(docs_btn)

        ex_btn = QPushButton("💡 Engineering Examples", left_col)
        ex_btn.setFixedHeight(34)
        ex_btn.setStyleSheet("text-align: left; padding-left: 14px;")
        if self._on_open_examples_cb:
            ex_btn.clicked.connect(self._on_open_examples_cb)
        left_layout.addWidget(ex_btn)

        cfg_btn = QPushButton("⚙️ Platform Settings", left_col)
        cfg_btn.setFixedHeight(34)
        cfg_btn.setStyleSheet("text-align: left; padding-left: 14px;")
        if self._on_open_settings_cb:
            cfg_btn.clicked.connect(self._on_open_settings_cb)
        left_layout.addWidget(cfg_btn)

        left_layout.addStretch()
        main_layout.addWidget(left_col, stretch=1)

        # Vertical Divider Line
        line = QFrame(self)
        line.setFrameShape(QFrame.Shape.VLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet("color: #333333;")
        main_layout.addWidget(line)

        # Right Column: Recent Projects List
        right_col = QWidget(self)
        right_layout = QVBoxLayout(right_col)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(12)

        recent_lbl = QLabel("<b>RECENT PROJECTS</b>", right_col)
        recent_lbl.setStyleSheet("color: #aaaaaa; letter-spacing: 1px;")
        right_layout.addWidget(recent_lbl)

        self._recent_list = QListWidget(right_col)
        self._recent_list.setStyleSheet("border: 1px solid #333333; border-radius: 4px; padding: 4px;")
        self._recent_list.itemDoubleClicked.connect(self._on_recent_item_double_clicked)
        right_layout.addWidget(self._recent_list)

        main_layout.addWidget(right_col, stretch=1)

    def refresh_recent_projects(self) -> None:
        """Dynamically load recent projects from RecentProjectsStore."""
        self._recent_list.clear()
        if self._recent_store is None:
            return

        entries = self._recent_store.get_recent_projects(limit=10)
        if not entries:
            item = QListWidgetItem("No recent projects found")
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            self._recent_list.addItem(item)
            return

        for entry in entries:
            pin_mark = "📌 " if entry.is_pinned else "📁 "
            item = QListWidgetItem(f"{pin_mark}{entry.name}\n   {entry.path}")
            item.setData(Qt.ItemDataRole.UserRole, entry.path)
            self._recent_list.addItem(item)

    def _on_recent_item_double_clicked(self, item: QListWidgetItem) -> None:
        path = item.data(Qt.ItemDataRole.UserRole)
        if path and self._on_open_recent_cb is not None:
            self._on_open_recent_cb(path)
