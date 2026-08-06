"""
Unit tests for PySide6 UI components in offscreen test mode.
"""

from pathlib import Path
import sys
import tempfile
import unittest

from PySide6.QtWidgets import QApplication
from app.bootstrap import Bootstrap
from ui.main_window import MainWindow
from ui.theme import ThemeManager, ThemeMode


class TestUI(unittest.TestCase):

    def setUp(self):
        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication(sys.argv)

    def test_ui_main_window_instantiation(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            config_path = str(tmp_path / "config.json")
            log_dir = str(tmp_path / "logs")
            db_path = str(tmp_path / "recent.db")

            runtime = Bootstrap.setup(config_path=config_path, log_dir=log_dir, db_path=db_path)

            main_win = MainWindow(runtime)
            self.assertTrue(main_win.windowTitle().startswith("Scilab Studio"))

            # Test Theme Manager
            theme_mgr = runtime.get_service(ThemeManager)
            theme_mgr.apply_theme(self.app, ThemeMode.DARK)
            self.assertEqual(theme_mgr.current_mode, ThemeMode.DARK)

            theme_mgr.apply_theme(self.app, ThemeMode.LIGHT)
            self.assertEqual(theme_mgr.current_mode, ThemeMode.LIGHT)

            # Clean up
            runtime.service_registry.stop_all()
            runtime.service_registry.dispose_all()


if __name__ == "__main__":
    unittest.main()
