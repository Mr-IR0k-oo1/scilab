"""
Main Window for Scilab Studio PySide6 UI shell.

Assembles Menu Bar, Toolbar, Left Sidebar Explorer, Central Tabbed Workspace,
Right Inspector Dock, Bottom Console Dock, Status Bar, and Toast Notifications
into a professional engineering workbench interface.
"""

import logging
from pathlib import Path
from typing import Optional
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QFont, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QDockWidget,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMenu,
    QMessageBox,
    QPushButton,
    QTabWidget,
    QTextEdit,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from core.runtime import RuntimeContext
from core.event_bus import Event, EventBus
from core.configuration import ConfigurationManager
from core.command import Command, CommandRegistry
from core.notification import NotificationManager
from workspace.manager import WorkspaceManager
from workspace.recent_projects import RecentProjectsStore
from workspace.project import Project
from .theme import ThemeManager, ThemeMode
from .docking import DockManager
from .sidebar import SidebarPanel
from .toolbar import MainToolBar
from .statusbar import MainStatusBar
from .welcome import WelcomeWidget
from .settings_dialog import SettingsDialog
from .console import LoggingConsolePanel
from .toast import ToastOverlayManager

logger = logging.getLogger(__name__)


class NewProjectDialog(QDialog):
    """Dialog for creating a new Scilab Studio project."""

    def __init__(self, default_dir: str, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Create New Scilab Studio Project")
        self.resize(500, 250)

        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        self.name_input = QLineEdit("UntitledProject", self)
        form_layout.addRow("Project Name:", self.name_input)

        dir_layout = QHBoxLayout()
        self.dir_input = QLineEdit(default_dir, self)
        self.browse_btn = QPushButton("Browse...", self)
        self.browse_btn.clicked.connect(self._browse_dir)
        dir_layout.addWidget(self.dir_input)
        dir_layout.addWidget(self.browse_btn)
        form_layout.addRow("Location:", dir_layout)

        self.author_input = QLineEdit("", self)
        form_layout.addRow("Author:", self.author_input)

        self.desc_input = QLineEdit("", self)
        form_layout.addRow("Description:", self.desc_input)

        layout.addLayout(form_layout)

        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
            self,
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def _browse_dir(self) -> None:
        chosen = QFileDialog.getExistingDirectory(self, "Select Project Parent Directory", self.dir_input.text())
        if chosen:
            self.dir_input.setText(chosen)


class MainWindow(QMainWindow):
    """
    Main Platform Window for Scilab Studio.
    """

    def __init__(self, runtime_context: RuntimeContext) -> None:
        super().__init__()
        self._ctx = runtime_context
        self._event_bus = self._ctx.event_bus
        self._config_mgr = self._ctx.config
        self._workspace_mgr = self._ctx.get_service(WorkspaceManager)
        self._recent_store = self._ctx.get_service(RecentProjectsStore)
        self._theme_mgr = self._ctx.get_service(ThemeManager)
        self._cmd_registry = self._ctx.get_service(CommandRegistry)
        self._notif_mgr = self._ctx.get_service(NotificationManager)

        self.setWindowTitle("Scilab Studio - Open Engineering Platform")
        self.resize(
            self._config_mgr.config.ui.window_width,
            self._config_mgr.config.ui.window_height,
        )

        self._dock_mgr = DockManager(self)

        self._register_commands()
        self._setup_ui()
        self._register_events()

        # Save initial default preset
        self._dock_mgr.save_default_preset()

    def _register_commands(self) -> None:
        """Register application commands in CommandRegistry."""
        self._cmd_registry.register_command(
            Command("project.new", "New Project", "Create a new .scstudio project", "Project", "Ctrl+N", self.on_action_new_project)
        )
        self._cmd_registry.register_command(
            Command("project.open", "Open Project", "Open an existing .scstudio project", "Project", "Ctrl+O", self.on_action_open_project)
        )
        self._cmd_registry.register_command(
            Command("project.save", "Save Project", "Save active project", "Project", "Ctrl+S", self.on_action_save_project)
        )
        self._cmd_registry.register_command(
            Command("project.close", "Close Project", "Close active project", "Project", None, self.on_action_close_project)
        )
        self._cmd_registry.register_command(
            Command("settings.open", "Open Settings", "Open platform settings dialog", "Settings", None, self.on_open_settings)
        )
        self._cmd_registry.register_command(
            Command("theme.toggle", "Toggle Theme", "Switch UI theme", "View", None, self.on_toggle_theme)
        )
        self._cmd_registry.register_command(
            Command("dock.reset", "Reset Dock Layout", "Reset docks to default engineering preset", "View", None, self.on_reset_dock_layout)
        )
        self._cmd_registry.register_command(
            Command("app.exit", "Exit Application", "Exit Scilab Studio", "Application", "Ctrl+Q", self.close)
        )

    def _setup_ui(self) -> None:
        """Build menu bar, toolbar, docks, central workspace, and status bar."""
        self._setup_menu_bar()
        self._setup_toolbar()
        self._setup_sidebar_dock()
        self._setup_central_workspace()
        self._setup_inspector_dock()
        self._setup_console_dock()
        self._setup_status_bar()
        self._setup_toast_overlay()

    def _setup_toast_overlay(self) -> None:
        """Attach Toast Overlay manager."""
        self._toast_mgr = ToastOverlayManager(self, self._event_bus)

    def _setup_menu_bar(self) -> None:
        """Create platform menu hierarchy."""
        menu_bar = self.menuBar()

        # File Menu
        self._file_menu = menu_bar.addMenu("&File")

        new_action = QAction("&New Project...", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.on_action_new_project)
        self._file_menu.addAction(new_action)

        open_action = QAction("&Open Project...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.on_action_open_project)
        self._file_menu.addAction(open_action)

        save_action = QAction("&Save Project", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.on_action_save_project)
        self._file_menu.addAction(save_action)

        self._recent_menu = self._file_menu.addMenu("Recent &Projects")
        self._rebuild_recent_menu()

        self._file_menu.addSeparator()

        close_proj_action = QAction("Close Project", self)
        close_proj_action.triggered.connect(self.on_action_close_project)
        self._file_menu.addAction(close_proj_action)

        self._file_menu.addSeparator()

        settings_action = QAction("Preferences / &Settings...", self)
        settings_action.triggered.connect(self.on_open_settings)
        self._file_menu.addAction(settings_action)

        self._file_menu.addSeparator()

        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        self._file_menu.addAction(exit_action)

        # Edit Menu
        edit_menu = menu_bar.addMenu("&Edit")
        undo_act = QAction("Undo", self)
        undo_act.setShortcut("Ctrl+Z")
        undo_act.triggered.connect(lambda: self._cmd_registry.undo())
        edit_menu.addAction(undo_act)

        redo_act = QAction("Redo", self)
        redo_act.setShortcut("Ctrl+Y")
        redo_act.triggered.connect(lambda: self._cmd_registry.redo())
        edit_menu.addAction(redo_act)

        edit_menu.addSeparator()
        edit_menu.addAction(QAction("Cut", self))
        edit_menu.addAction(QAction("Copy", self))
        edit_menu.addAction(QAction("Paste", self))

        # View Menu
        view_menu = menu_bar.addMenu("&View")
        
        toggle_sidebar_act = QAction("Toggle Left Sidebar", self)
        toggle_sidebar_act.setShortcut("Ctrl+B")
        toggle_sidebar_act.triggered.connect(lambda: self._dock_mgr.toggle_dock("SidebarDock"))
        view_menu.addAction(toggle_sidebar_act)

        toggle_inspector_act = QAction("Toggle Right Inspector", self)
        toggle_inspector_act.triggered.connect(lambda: self._dock_mgr.toggle_dock("InspectorDock"))
        view_menu.addAction(toggle_inspector_act)

        toggle_console_act = QAction("Toggle Bottom Console", self)
        toggle_console_act.setShortcut("Ctrl+`")
        toggle_console_act.triggered.connect(lambda: self._dock_mgr.toggle_dock("ConsoleDock"))
        view_menu.addAction(toggle_console_act)

        view_menu.addSeparator()
        reset_layout_act = QAction("Reset Dock Layout Preset", self)
        reset_layout_act.triggered.connect(self.on_reset_dock_layout)
        view_menu.addAction(reset_layout_act)

        view_menu.addSeparator()
        toggle_theme_act = QAction("Switch Theme (Dark / Light / System)", self)
        toggle_theme_act.triggered.connect(self.on_toggle_theme)
        view_menu.addAction(toggle_theme_act)

        # Workspace Menu
        ws_menu = menu_bar.addMenu("&Workspace")
        ws_menu.addAction("Project Settings...", lambda: QMessageBox.information(self, "Project Settings", "Project settings dialog placeholder."))

        # Tools Menu
        tools_menu = menu_bar.addMenu("&Tools")
        tools_menu.addAction("Scilab Interactive Shell", lambda: self._dock_mgr.toggle_dock("ConsoleDock", True))

        # Help Menu
        help_menu = menu_bar.addMenu("&Help")
        help_menu.addAction("Documentation", self.on_open_docs)
        help_menu.addAction("Engineering Examples", self.on_open_examples)
        help_menu.addSeparator()
        help_menu.addAction("About Scilab Studio", self.on_about)

    def _rebuild_recent_menu(self) -> None:
        """Dynamic sub-menu listing recent projects."""
        self._recent_menu.clear()
        entries = self._recent_store.get_recent_projects(limit=8)
        if not entries:
            no_rec_act = QAction("No Recent Projects", self)
            no_rec_act.setEnabled(False)
            self._recent_menu.addAction(no_rec_act)
            return

        for entry in entries:
            act = QAction(f"{entry.name} ({entry.path})", self)
            act.triggered.connect(lambda checked=False, p=entry.path: self._open_project_path(p))
            self._recent_menu.addAction(act)

    def _setup_toolbar(self) -> None:
        """Attach MainToolBar."""
        self._toolbar = MainToolBar(self)
        self._toolbar.action_new.triggered.connect(self.on_action_new_project)
        self._toolbar.action_open.triggered.connect(self.on_action_open_project)
        self._toolbar.action_save.triggered.connect(self.on_action_save_project)
        self._toolbar.action_theme.triggered.connect(self.on_toggle_theme)
        self._toolbar.action_scilab_console.triggered.connect(lambda: self._dock_mgr.toggle_dock("ConsoleDock", True))
        self.addToolBar(self._toolbar)

    def _setup_sidebar_dock(self) -> None:
        """Attach Sidebar Dock widget."""
        self._sidebar = SidebarPanel(
            event_bus=self._event_bus,
            workspace_mgr=self._workspace_mgr,
            recent_store=self._recent_store,
            on_open_recent_cb=self._open_project_path,
            on_open_file_cb=self.open_file_tab,
            parent=self,
        )
        self._dock_mgr.register_dock("SidebarDock", self._sidebar, Qt.DockWidgetArea.LeftDockWidgetArea)

    def _setup_central_workspace(self) -> None:
        """Setup central tabbed document workspace."""
        self._central_tabs = QTabWidget(self)
        self._central_tabs.setDocumentMode(True)
        self._central_tabs.setTabsClosable(True)
        self._central_tabs.tabCloseRequested.connect(self._on_close_tab)

        # Build Welcome Page Widget
        self._welcome_page = WelcomeWidget(
            recent_store=self._recent_store,
            on_new_project_cb=self.on_action_new_project,
            on_open_project_cb=self.on_action_open_project,
            on_open_recent_cb=self._open_project_path,
            on_open_settings_cb=self.on_open_settings,
            on_open_docs_cb=self.on_open_docs,
            on_open_examples_cb=self.on_open_examples,
            parent=self,
        )

        self._central_tabs.addTab(self._welcome_page, "Welcome")
        self.setCentralWidget(self._central_tabs)

    def open_file_tab(self, file_path: str) -> None:
        """Open a file tab in Central Workspace."""
        p = Path(file_path)
        if not p.exists() or not p.is_file():
            return

        # Check if already open
        for i in range(self._central_tabs.count()):
            widget = self._central_tabs.widget(i)
            if hasattr(widget, "file_path") and widget.file_path == file_path:
                self._central_tabs.setCurrentIndex(i)
                return

        editor = QTextEdit()
        editor.file_path = file_path
        try:
            with open(p, "r", encoding="utf-8", errors="replace") as f:
                editor.setText(f.read())
        except Exception as exc:
            editor.setText(f"Error opening file: {exc}")

        index = self._central_tabs.addTab(editor, p.name)
        self._central_tabs.setCurrentIndex(index)
        self._workspace_mgr.add_opened_file(file_path)

    def _setup_inspector_dock(self) -> None:
        """Setup Right Inspector Property Dock."""
        self._inspector_dock = QDockWidget("Inspector", self)
        self._inspector_dock.setObjectName("InspectorDock")
        self._inspector_dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea | Qt.DockWidgetArea.LeftDockWidgetArea)

        inspector_widget = QWidget()
        inspector_layout = QVBoxLayout(inspector_widget)
        inspector_layout.setContentsMargins(4, 4, 4, 4)

        self._property_tree = QTreeWidget(inspector_widget)
        self._property_tree.setHeaderLabels(["Property", "Value"])
        self._property_tree.header().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Default inspector rows
        self._update_inspector_properties(None)

        inspector_layout.addWidget(self._property_tree)
        self._inspector_dock.setWidget(inspector_widget)
        self._dock_mgr.register_dock("InspectorDock", self._inspector_dock, Qt.DockWidgetArea.RightDockWidgetArea)

    def _setup_console_dock(self) -> None:
        """Setup Bottom Tabbed Console Dock."""
        self._console_dock = QDockWidget("Console & Output", self)
        self._console_dock.setObjectName("ConsoleDock")
        self._console_dock.setAllowedAreas(Qt.DockWidgetArea.BottomDockWidgetArea | Qt.DockWidgetArea.TopDockWidgetArea)

        console_tabs = QTabWidget(self._console_dock)
        console_tabs.setDocumentMode(True)

        # Tab 1: Structured Logging Console
        self._logging_console = LoggingConsolePanel(event_bus=self._event_bus, parent=console_tabs)
        console_tabs.addTab(self._logging_console, "📋 System Log Stream")

        # Tab 2: Scilab Interactive Console Placeholder
        scilab_console = QTextEdit()
        scilab_console.setReadOnly(True)
        scilab_console.setText("Scilab 7.0.0 Interactive Engine Console (Placeholder)\nReady for computational execution.\n--> ")
        console_tabs.addTab(scilab_console, "⚡ Scilab Console")

        self._console_dock.setWidget(console_tabs)
        self._dock_mgr.register_dock("ConsoleDock", self._console_dock, Qt.DockWidgetArea.BottomDockWidgetArea)

    def _setup_status_bar(self) -> None:
        """Attach MainStatusBar."""
        self._status_bar = MainStatusBar(event_bus=self._event_bus, parent=self)
        self.setStatusBar(self._status_bar)

    def _register_events(self) -> None:
        """Subscribe to platform EventBus topics."""
        self._event_bus.subscribe("workspace.opened", self._on_workspace_opened)
        self._event_bus.subscribe("workspace.closed", self._on_workspace_closed)

    def _on_workspace_opened(self, event: Event) -> None:
        """Handle project opened event."""
        project: Project = event.payload.get("project")
        name = event.payload.get("name", "Project")
        self.setWindowTitle(f"Scilab Studio - {name} [{project.root_path}]")
        self._update_inspector_properties(project)
        self._rebuild_recent_menu()
        self._welcome_page.refresh_recent_projects()
        self._sidebar.refresh_recent_list()
        self._notif_mgr.success("Workspace Opened", f"Loaded project '{name}'.")

    def _on_workspace_closed(self, event: Event) -> None:
        """Handle project closed event."""
        self.setWindowTitle("Scilab Studio - Open Engineering Platform")
        self._update_inspector_properties(None)
        self._rebuild_recent_menu()
        self._welcome_page.refresh_recent_projects()
        self._sidebar.refresh_recent_list()
        self._notif_mgr.info("Workspace Closed", "Active project closed.")

    def _update_inspector_properties(self, project: Optional[Project]) -> None:
        """Refresh property tree items."""
        self._property_tree.clear()

        root_item = QTreeWidgetItem(["Active Workspace", ""])
        if project is not None:
            root_item.addChild(QTreeWidgetItem(["Project Name", project.metadata.name]))
            root_item.addChild(QTreeWidgetItem(["Author", project.metadata.author or "N/A"]))
            root_item.addChild(QTreeWidgetItem(["Version", project.metadata.version]))
            root_item.addChild(QTreeWidgetItem(["Scilab Engine", project.metadata.scilab_version]))
            root_item.addChild(QTreeWidgetItem(["Root Directory", str(project.root_path)]))
        else:
            root_item.addChild(QTreeWidgetItem(["Project Name", "None"]))
            root_item.addChild(QTreeWidgetItem(["Status", "No active project loaded"]))

        self._property_tree.addTopLevelItem(root_item)
        self._property_tree.expandAll()

    def on_action_new_project(self) -> None:
        """Show New Project Dialog and create project."""
        default_dir = self._config_mgr.config.workspace.default_directory
        dlg = NewProjectDialog(default_dir=default_dir, parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            name = dlg.name_input.text().strip()
            parent_dir = dlg.dir_input.text().strip()
            author = dlg.author_input.text().strip()
            desc = dlg.desc_input.text().strip()

            if not name or not parent_dir:
                QMessageBox.warning(self, "Invalid Input", "Project Name and Location are required.")
                return

            try:
                self._workspace_mgr.create_project(
                    name=name,
                    parent_dir=parent_dir,
                    author=author,
                    description=desc,
                )
            except Exception as exc:
                QMessageBox.critical(self, "Project Creation Error", str(exc))

    def on_action_open_project(self) -> None:
        """Show Open File / Directory dialog."""
        chosen = QFileDialog.getExistingDirectory(
            self,
            "Select Scilab Studio Project Directory",
            self._config_mgr.config.workspace.default_directory,
        )
        if chosen:
            self._open_project_path(chosen)

    def _open_project_path(self, path_str: str) -> None:
        """Open project path."""
        try:
            self._workspace_mgr.open_project(path_str)
        except Exception as exc:
            QMessageBox.critical(self, "Failed to Open Project", f"Could not load project at {path_str}:\n{exc}")

    def on_action_save_project(self) -> None:
        """Save active project."""
        if self._workspace_mgr.current_project is not None:
            # Remember dock layout state
            self._workspace_mgr.set_dock_layout(self._dock_mgr.save_layout_b64())
            self._workspace_mgr.save_project()
            self._notif_mgr.success("Saved Project", f"Project '{self._workspace_mgr.current_project.metadata.name}' saved successfully.")
        else:
            QMessageBox.information(self, "Save Project", "No active project is currently loaded.")

    def on_action_close_project(self) -> None:
        """Close active project."""
        if self._workspace_mgr.current_project is not None:
            self._workspace_mgr.close_project()

    def on_open_settings(self) -> None:
        """Open Settings Dialog."""
        dlg = SettingsDialog(self._config_mgr, self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self._notif_mgr.info("Settings Saved", "Platform configuration updated.")

    def on_reset_dock_layout(self) -> None:
        """Reset dock layout to preset default."""
        self._dock_mgr.reset_layout()
        self._notif_mgr.info("Layout Reset", "Restored default docking layout preset.")

    def on_toggle_theme(self) -> None:
        """Toggle Theme mode."""
        app = QApplication.instance()
        if isinstance(app, QApplication):
            new_mode = self._theme_mgr.toggle_theme(app)
            self._notif_mgr.info("Theme Switch", f"Switched UI theme to {new_mode.value.capitalize()}.")

    def on_open_docs(self) -> None:
        """Show documentation info."""
        QMessageBox.information(self, "Documentation", "Scilab Studio Phase 1 Platform Documentation.")

    def on_open_examples(self) -> None:
        """Show engineering examples info."""
        QMessageBox.information(self, "Engineering Examples", "Scilab Studio Engineering Benchmark & Tutorial Examples.")

    def on_about(self) -> None:
        """Display About dialog."""
        QMessageBox.about(
            self,
            "About Scilab Studio",
            "<h3>Scilab Studio (Sprint 1 Application Framework)</h3>"
            "<p>An Engineering Development Platform built around Scilab for engineering education, research, and industry.</p>"
            "<p>Built with Python 3.12+ and PySide6 (Qt6).</p>"
            "<p>Open Source & FOSSEE compliant clean modular architecture.</p>",
        )

    def _on_close_tab(self, index: int) -> None:
        """Close file tab (keep Welcome page at index 0 open)."""
        if index > 0:
            widget = self._central_tabs.widget(index)
            if hasattr(widget, "file_path"):
                self._workspace_mgr.remove_opened_file(widget.file_path)
            self._central_tabs.removeTab(index)

    def closeEvent(self, event) -> None:
        """Window close event handler."""
        self._config_mgr.update_ui_config(
            window_width=self.width(),
            window_height=self.height(),
        )
        super().closeEvent(event)
