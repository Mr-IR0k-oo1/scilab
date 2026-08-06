"""
Unit tests for Settings Manager / Configuration persistence.
"""

from pathlib import Path
import tempfile
import unittest

from core.configuration import ConfigurationManager


class TestSettingsManager(unittest.TestCase):

    def test_settings_persistence_and_categories(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            config_file = Path(tmp_dir) / "test_settings.json"
            mgr = ConfigurationManager(config_path=str(config_file))
            mgr.initialize()

            # Test default values
            self.assertEqual(mgr.config.ui.theme, "dark")
            self.assertEqual(mgr.config.editor.tab_size, 4)
            self.assertEqual(mgr.config.advanced.log_level, "INFO")

            # Update settings across categories
            mgr.config.ui.theme = "light"
            mgr.config.editor.tab_size = 2
            mgr.config.projects.default_author = "FOSSEE Senior Architect"
            mgr.save()

            # Load new instance from same file
            mgr2 = ConfigurationManager(config_path=str(config_file))
            mgr2.initialize()

            self.assertEqual(mgr2.config.ui.theme, "light")
            self.assertEqual(mgr2.config.editor.tab_size, 2)
            self.assertEqual(mgr2.config.projects.default_author, "FOSSEE Senior Architect")


if __name__ == "__main__":
    unittest.main()
