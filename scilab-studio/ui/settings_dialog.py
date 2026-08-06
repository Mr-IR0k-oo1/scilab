"""
Settings Dialog for Scilab Studio PySide6 UI shell.

Provides tabbed configuration dialog covering General, Appearance, Projects,
Editor, and Advanced settings, persisting changes to ConfigurationManager.
"""

import logging
from typing import Optional
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from core.configuration import ConfigurationManager

logger = logging.getLogger(__name__)


class SettingsDialog(QDialog):
    """
    Tabbed Settings Dialog for platform configuration.
    """

    def __init__(self, config_mgr: ConfigurationManager, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._config_mgr = config_mgr
        self.setWindowTitle("Scilab Studio Settings")
        self.resize(550, 400)

        self._setup_ui()
        self._load_current_settings()

    def _setup_ui(self) -> None:
        """Build settings tabs and controls."""
        main_layout = QVBoxLayout(self)

        self._tab_widget = QTabWidget(self)

        # Tab 1: General
        gen_widget = QWidget()
        gen_form = QFormLayout(gen_widget)

        self._gen_dir_input = QLineEdit(self)
        browse_btn = QPushButton("Browse...", self)
        browse_btn.clicked.connect(self._browse_gen_dir)
        dir_layout = QHBoxLayout()
        dir_layout.addWidget(self._gen_dir_input)
        dir_layout.addWidget(browse_btn)
        gen_form.addRow("Default Project Directory:", dir_layout)

        self._gen_autosave_chk = QCheckBox("Enable Workspace Auto-Save", self)
        gen_form.addRow("Auto Save:", self._gen_autosave_chk)

        self._gen_recent_limit_spin = QSpinBox(self)
        self._gen_recent_limit_spin.setRange(1, 50)
        gen_form.addRow("Recent Projects Limit:", self._gen_recent_limit_spin)

        self._tab_widget.addTab(gen_widget, "General")

        # Tab 2: Appearance
        app_widget = QWidget()
        app_form = QFormLayout(app_widget)

        self._app_theme_combo = QComboBox(self)
        self._app_theme_combo.addItems(["Dark", "Light", "System"])
        app_form.addRow("Theme:", self._app_theme_combo)

        self._app_width_spin = QSpinBox(self)
        self._app_width_spin.setRange(800, 3840)
        app_form.addRow("Window Width:", self._app_width_spin)

        self._app_height_spin = QSpinBox(self)
        self._app_height_spin.setRange(600, 2160)
        app_form.addRow("Window Height:", self._app_height_spin)

        self._tab_widget.addTab(app_widget, "Appearance")

        # Tab 3: Projects
        proj_widget = QWidget()
        proj_form = QFormLayout(proj_widget)

        self._proj_scilab_ver_input = QLineEdit(self)
        proj_form.addRow("Default Scilab Version:", self._proj_scilab_ver_input)

        self._proj_author_input = QLineEdit(self)
        proj_form.addRow("Default Author Name:", self._proj_author_input)

        self._proj_templates_input = QLineEdit(self)
        proj_form.addRow("Templates Directory:", self._proj_templates_input)

        self._tab_widget.addTab(proj_widget, "Projects")

        # Tab 4: Editor
        ed_widget = QWidget()
        ed_form = QFormLayout(ed_widget)

        self._ed_tab_size_spin = QSpinBox(self)
        self._ed_tab_size_spin.setRange(2, 8)
        ed_form.addRow("Tab Size (spaces):", self._ed_tab_size_spin)

        self._ed_word_wrap_chk = QCheckBox("Enable Word Wrap", self)
        ed_form.addRow("Word Wrap:", self._ed_word_wrap_chk)

        self._ed_line_nums_chk = QCheckBox("Show Line Numbers", self)
        ed_form.addRow("Line Numbers:", self._ed_line_nums_chk)

        self._ed_auto_indent_chk = QCheckBox("Enable Auto Indentation", self)
        ed_form.addRow("Auto Indent:", self._ed_auto_indent_chk)

        self._tab_widget.addTab(ed_widget, "Editor")

        # Tab 5: Advanced
        adv_widget = QWidget()
        adv_form = QFormLayout(adv_widget)

        self._adv_log_level_combo = QComboBox(self)
        self._adv_log_level_combo.addItems(["DEBUG", "INFO", "WARNING", "ERROR"])
        adv_form.addRow("Log Level:", self._adv_log_level_combo)

        self._adv_watcher_chk = QCheckBox("Enable File System Watcher", self)
        adv_form.addRow("File Watcher:", self._adv_watcher_chk)

        self._adv_max_logs_spin = QSpinBox(self)
        self._adv_max_logs_spin.setRange(100, 10000)
        adv_form.addRow("Max Log Lines:", self._adv_max_logs_spin)

        self._tab_widget.addTab(adv_widget, "Advanced")

        main_layout.addWidget(self._tab_widget)

        # Dialog Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
            self,
        )
        button_box.accepted.connect(self._save_and_accept)
        button_box.rejected.connect(self.reject)
        main_layout.addWidget(button_box)

    def _browse_gen_dir(self) -> None:
        chosen = QFileDialog.getExistingDirectory(self, "Select Default Directory", self._gen_dir_input.text())
        if chosen:
            self._gen_dir_input.setText(chosen)

    def _load_current_settings(self) -> None:
        """Populate dialog widgets from ConfigurationManager."""
        cfg = self._config_mgr.config

        # General
        self._gen_dir_input.setText(cfg.workspace.default_directory)
        self._gen_autosave_chk.setChecked(cfg.workspace.auto_save)
        self._gen_recent_limit_spin.setValue(cfg.workspace.recent_projects_limit)

        # Appearance
        theme_index = self._app_theme_combo.findText(cfg.ui.theme.capitalize())
        if theme_index >= 0:
            self._app_theme_combo.setCurrentIndex(theme_index)
        self._app_width_spin.setValue(cfg.ui.window_width)
        self._app_height_spin.setValue(cfg.ui.window_height)

        # Projects
        self._proj_scilab_ver_input.setText(cfg.projects.default_scilab_version)
        self._proj_author_input.setText(cfg.projects.default_author)
        self._proj_templates_input.setText(cfg.projects.templates_directory)

        # Editor
        self._ed_tab_size_spin.setValue(cfg.editor.tab_size)
        self._ed_word_wrap_chk.setChecked(cfg.editor.word_wrap)
        self._ed_line_nums_chk.setChecked(cfg.editor.show_line_numbers)
        self._ed_auto_indent_chk.setChecked(cfg.editor.auto_indentation)

        # Advanced
        log_index = self._adv_log_level_combo.findText(cfg.advanced.log_level.upper())
        if log_index >= 0:
            self._adv_log_level_combo.setCurrentIndex(log_index)
        self._adv_watcher_chk.setChecked(cfg.advanced.file_watcher_enabled)
        self._adv_max_logs_spin.setValue(cfg.advanced.max_log_lines)

    def _save_and_accept(self) -> None:
        """Write dialog values back into ConfigurationManager and save to JSON."""
        cfg = self._config_mgr.config

        # General
        cfg.workspace.default_directory = self._gen_dir_input.text().strip()
        cfg.workspace.auto_save = self._gen_autosave_chk.isChecked()
        cfg.workspace.recent_projects_limit = self._gen_recent_limit_spin.value()

        # Appearance
        cfg.ui.theme = self._app_theme_combo.currentText().lower()
        cfg.ui.window_width = self._app_width_spin.value()
        cfg.ui.window_height = self._app_height_spin.value()

        # Projects
        cfg.projects.default_scilab_version = self._proj_scilab_ver_input.text().strip()
        cfg.projects.default_author = self._proj_author_input.text().strip()
        cfg.projects.templates_directory = self._proj_templates_input.text().strip()

        # Editor
        cfg.editor.tab_size = self._ed_tab_size_spin.value()
        cfg.editor.word_wrap = self._ed_word_wrap_chk.isChecked()
        cfg.editor.show_line_numbers = self._ed_line_nums_chk.isChecked()
        cfg.editor.auto_indentation = self._ed_auto_indent_chk.isChecked()

        # Advanced
        cfg.advanced.log_level = self._adv_log_level_combo.currentText()
        cfg.advanced.file_watcher_enabled = self._adv_watcher_chk.isChecked()
        cfg.advanced.max_log_lines = self._adv_max_logs_spin.value()

        self._config_mgr.save()
        logger.info("Saved settings via SettingsDialog.")
        self.accept()
