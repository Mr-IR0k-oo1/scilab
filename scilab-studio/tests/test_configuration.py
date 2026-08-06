"""
Unit tests for ConfigurationManager JSON load, update, and persistence.
"""

from pathlib import Path
import tempfile
import unittest

from core.configuration import ConfigurationManager


class TestConfigurationManager(unittest.TestCase):

    def test_configuration_defaults_and_updates(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            config_file = Path(tmp_dir) / "test_config.json"
            mgr = ConfigurationManager(config_path=str(config_file))
            mgr.initialize()

            self.assertEqual(mgr.config.ui.theme, "dark")
            self.assertEqual(mgr.config.ui.window_width, 1280)

            mgr.update_ui_config(theme="light", window_width=1600)
            self.assertEqual(mgr.config.ui.theme, "light")
            self.assertEqual(mgr.config.ui.window_width, 1600)

            # Test persistence by instantiating new manager reading same file
            mgr2 = ConfigurationManager(config_path=str(config_file))
            mgr2.initialize()
            self.assertEqual(mgr2.config.ui.theme, "light")
            self.assertEqual(mgr2.config.ui.window_width, 1600)


if __name__ == "__main__":
    unittest.main()
