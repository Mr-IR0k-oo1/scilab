"""
Project Explorer Tree View component for Scilab Studio PySide6 UI shell.

Provides complete workspace file system management: Tree view with icons, expand/collapse,
refresh, file/folder creation, rename, delete (confirmation dialog), context menu,
and auto-updates when project or file watcher events fire.
"""

import logging
from pathlib import Path
import shutil
from typing import Callable, Optional
from PySide6.QtCore import QDir, QFileInfo, QModelIndex, Qt, Slot
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QFileIconProvider,
    QFileSystemModel,
    QInputDialog,
    QMenu,
    QMessageBox,
    QTreeView,
    QVBoxLayout,
    QWidget,
    QLabel,
)

from core.event_bus import Event, EventBus
from workspace.manager import WorkspaceManager

logger = logging.getLogger(__name__)


class EngineeringFileIconProvider(QFileIconProvider):
    """Custom icon provider adding visual distinction for Scilab scripts, datasets, and docs."""

    def icon(self, info: QFileInfo) -> QIcon:
        ext = info.suffix().lower()
        # Fallback to Qt default icons
        return super().icon(info)


class ProjectExplorerWidget(QWidget):
    """
    Project Explorer file tree view widget with context menus and actions.
    """

    def __init__(
        self,
        event_bus: Optional[EventBus] = None,
        workspace_mgr: Optional[WorkspaceManager] = None,
        on_open_file_cb: Optional[Callable[[str], None]] = None,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self._event_bus = event_bus
        self._workspace_mgr = workspace_mgr
        self._on_open_file_cb = on_open_file_cb
        self._root_path: Optional[Path] = None

        self._setup_ui()
        self._register_event_handlers()

    def _setup_ui(self) -> None:
        """Construct file tree view."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self._model = QFileSystemModel(self)
        self._model.setIconProvider(EngineeringFileIconProvider())
        self._model.setFilter(QDir.Filter.AllEntries | QDir.Filter.NoDotAndDotDot)

        self._tree_view = QTreeView(self)
        self._tree_view.setModel(self._model)
        self._tree_view.setHeaderHidden(True)
        self._tree_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self._tree_view.customContextMenuRequested.connect(self._show_context_menu)
        self._tree_view.doubleClicked.connect(self._on_double_clicked)

        # Hide extra columns for clean view
        for i in range(1, 4):
            self._tree_view.setColumnHidden(i, True)

        self._no_proj_lbl = QLabel("No active project loaded.", self)
        self._no_proj_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._no_proj_lbl.setStyleSheet("color: #888888; font-style: italic; padding: 20px;")

        layout.addWidget(self._no_proj_lbl)
        layout.addWidget(self._tree_view)
        self._tree_view.hide()

    def _register_event_handlers(self) -> None:
        """Subscribe to workspace and file watcher events."""
        if self._event_bus is not None:
            self._event_bus.subscribe("workspace.opened", self._on_workspace_opened)
            self._event_bus.subscribe("workspace.closed", self._on_workspace_closed)
            self._event_bus.subscribe("workspace.directory_changed", self.refresh)

    def set_project_root(self, root_path: Path) -> None:
        """Set root path of active workspace project."""
        self._root_path = root_path
        self._model.setRootPath(str(root_path))
        self._tree_view.setRootIndex(self._model.index(str(root_path)))
        self._no_proj_lbl.hide()
        self._tree_view.show()

    def clear_project_root(self) -> None:
        """Reset tree view when project closes."""
        self._root_path = None
        self._tree_view.hide()
        self._no_proj_lbl.show()

    def _on_workspace_opened(self, event: Event) -> None:
        """Event handler for workspace.opened."""
        path_str = event.payload.get("path")
        if path_str:
            self.set_project_root(Path(path_str))

    def _on_workspace_closed(self, event: Event) -> None:
        """Event handler for workspace.closed."""
        self.clear_project_root()

    def expand_all(self) -> None:
        """Expand all tree view nodes."""
        self._tree_view.expandAll()

    def collapse_all(self) -> None:
        """Collapse all tree view nodes."""
        self._tree_view.collapseAll()

    def refresh(self, event: Optional[Event] = None) -> None:
        """Refresh file system model."""
        if self._root_path is not None:
            self._model.setRootPath("")
            self._model.setRootPath(str(self._root_path))

    def _on_double_clicked(self, index: QModelIndex) -> None:
        """Handle double-clicking a file item."""
        path_str = self._model.filePath(index)
        if Path(path_str).is_file() and self._on_open_file_cb is not None:
            self._on_open_file_cb(path_str)

    def _show_context_menu(self, pos) -> None:
        """Display right-click context menu for selected tree node."""
        index = self._tree_view.indexAt(pos)
        selected_path = Path(self._model.filePath(index)) if index.isValid() else self._root_path

        if selected_path is None:
            return

        target_dir = selected_path if selected_path.is_dir() else selected_path.parent

        menu = QMenu(self)

        new_file_act = QAction("📄 New File...", self)
        new_file_act.triggered.connect(lambda: self.create_file(target_dir))
        menu.addAction(new_file_act)

        new_folder_act = QAction("📁 New Folder...", self)
        new_folder_act.triggered.connect(lambda: self.create_folder(target_dir))
        menu.addAction(new_folder_act)

        menu.addSeparator()

        if index.isValid():
            rename_act = QAction("✏️ Rename...", self)
            rename_act.triggered.connect(lambda: self.rename_item(selected_path))
            menu.addAction(rename_act)

            delete_act = QAction("🗑️ Delete", self)
            delete_act.triggered.connect(lambda: self.delete_item(selected_path))
            menu.addAction(delete_act)

            menu.addSeparator()

        expand_act = QAction("➕ Expand All", self)
        expand_act.triggered.connect(self.expand_all)
        menu.addAction(expand_act)

        collapse_act = QAction("➖ Collapse All", self)
        collapse_act.triggered.connect(self.collapse_all)
        menu.addAction(collapse_act)

        refresh_act = QAction("🔄 Refresh Explorer", self)
        refresh_act.triggered.connect(self.refresh)
        menu.addAction(refresh_act)

        menu.exec(self._tree_view.viewport().mapToGlobal(pos))

    def create_file(self, target_dir: Path) -> None:
        """Dialog to create a new file on disk."""
        filename, ok = QInputDialog.getText(self, "Create File", "File Name (e.g. script.sce):")
        if ok and filename.strip():
            new_file = target_dir / filename.strip()
            if new_file.exists():
                QMessageBox.warning(self, "File Exists", f"File already exists: {new_file.name}")
                return
            try:
                new_file.touch()
                logger.info("Created file: %s", new_file)
                self.refresh()
            except Exception as exc:
                QMessageBox.critical(self, "Create File Error", str(exc))

    def create_folder(self, target_dir: Path) -> None:
        """Dialog to create a new directory on disk."""
        foldername, ok = QInputDialog.getText(self, "Create Folder", "Folder Name:")
        if ok and foldername.strip():
            new_dir = target_dir / foldername.strip()
            if new_dir.exists():
                QMessageBox.warning(self, "Folder Exists", f"Folder already exists: {new_dir.name}")
                return
            try:
                new_dir.mkdir(parents=True, exist_ok=True)
                logger.info("Created folder: %s", new_dir)
                self.refresh()
            except Exception as exc:
                QMessageBox.critical(self, "Create Folder Error", str(exc))

    def rename_item(self, target_path: Path) -> None:
        """Dialog to rename a file or directory."""
        new_name, ok = QInputDialog.getText(self, "Rename", "New Name:", text=target_path.name)
        if ok and new_name.strip() and new_name.strip() != target_path.name:
            destination = target_path.parent / new_name.strip()
            if destination.exists():
                QMessageBox.warning(self, "Destination Exists", f"Item already exists: {destination.name}")
                return
            try:
                target_path.rename(destination)
                logger.info("Renamed %s -> %s", target_path, destination)
                self.refresh()
            except Exception as exc:
                QMessageBox.critical(self, "Rename Error", str(exc))

    def delete_item(self, target_path: Path) -> None:
        """Confirmation dialog to delete a file or directory."""
        res = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to permanently delete '{target_path.name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if res == QMessageBox.StandardButton.Yes:
            try:
                if target_path.is_dir():
                    shutil.rmtree(target_path)
                else:
                    target_path.unlink()
                logger.info("Deleted: %s", target_path)
                self.refresh()
            except Exception as exc:
                QMessageBox.critical(self, "Delete Error", str(exc))
