"""
Sidebar Explorer Panel for Scilab Studio PySide6 UI shell.

Left dock panel hosting Project Explorer tree view widget and Workspace Navigator.
Updates automatically when workspace open/close events occur.
"""

import logging
from typing import Callable, Optional
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDockWidget,
    QListWidget,
    QListWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from core.event_bus import EventBus
from workspace.manager import WorkspaceManager
from workspace.recent_projects import RecentProjectsStore
from .explorer import ProjectExplorerWidget

logger = logging.getLogger(__name__)


class SidebarPanel(QDockWidget):
    """
    Left Sidebar Panel containing Project Explorer tree view and Recent Projects navigator.
    """

    def __init__(
        self,
        event_bus: Optional[EventBus] = None,
        workspace_mgr: Optional[WorkspaceManager] = None,
        recent_store: Optional[RecentProjectsStore] = None,
        on_open_recent_cb: Optional[Callable[[str], None]] = None,
        on_open_file_cb: Optional[Callable[[str], None]] = None,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__("Project Explorer", parent)
        self.setObjectName("SidebarDock")
        self._event_bus = event_bus
        self._workspace_mgr = workspace_mgr
        self._recent_store = recent_store
        self._on_open_recent_cb = on_open_recent_cb
        self._on_open_file_cb = on_open_file_cb

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Construct sidebar tabs and views."""
        self.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)

        self._tab_widget = QTabWidget(self)
        self._tab_widget.setDocumentMode(True)

        # Tab 1: Project Explorer Widget
        self.explorer_widget = ProjectExplorerWidget(
            event_bus=self._event_bus,
            workspace_mgr=self._workspace_mgr,
            on_open_file_cb=self._on_open_file_cb,
            parent=self,
        )
        self._tab_widget.addTab(self.explorer_widget, "Project Explorer")

        # Tab 2: Recent Projects
        self._recent_container = QWidget()
        recent_layout = QVBoxLayout(self._recent_container)
        recent_layout.setContentsMargins(4, 4, 4, 4)

        self._recent_list = QListWidget(self._recent_container)
        self._recent_list.itemDoubleClicked.connect(self._on_recent_double_clicked)
        recent_layout.addWidget(self._recent_list)

        self._tab_widget.addTab(self._recent_container, "Recent Projects")

        self.setWidget(self._tab_widget)
        self.refresh_recent_list()

    def refresh_recent_list(self) -> None:
        """Reload items from RecentProjectsStore."""
        self._recent_list.clear()
        if self._recent_store is None:
            return

        entries = self._recent_store.get_recent_projects(limit=10)
        if not entries:
            item = QListWidgetItem("No recent projects")
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            self._recent_list.addItem(item)
            return

        for entry in entries:
            pin_prefix = "📌 " if entry.is_pinned else "📁 "
            item = QListWidgetItem(f"{pin_prefix}{entry.name}")
            item.setToolTip(entry.path)
            item.setData(Qt.ItemDataRole.UserRole, entry.path)
            self._recent_list.addItem(item)

    def _on_recent_double_clicked(self, item: QListWidgetItem) -> None:
        """Handle double-clicking a recent project item."""
        path = item.data(Qt.ItemDataRole.UserRole)
        if path and self._on_open_recent_cb is not None:
            self._on_open_recent_cb(path)
