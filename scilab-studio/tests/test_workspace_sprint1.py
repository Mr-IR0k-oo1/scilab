"""
Unit tests for Workspace Manager Sprint 1 extensions.
"""

from pathlib import Path
import tempfile
import unittest

from core.event_bus import EventBus
from workspace.recent_projects import RecentProjectsStore
from workspace.manager import WorkspaceManager


class TestWorkspaceSprint1(unittest.TestCase):

    def test_workspace_state_memory(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            bus = EventBus()
            bus.initialize()
            bus.start()

            db_file = tmp_path / "recent.db"
            store = RecentProjectsStore(db_path=str(db_file))
            store.initialize()

            ws_mgr = WorkspaceManager(recent_store=store, event_bus=bus)
            ws_mgr.initialize()

            proj = ws_mgr.create_workspace("QuantumSimulation", parent_dir=str(tmp_path))
            self.assertEqual(ws_mgr.current_project.metadata.name, "QuantumSimulation")

            # Track opened files
            ws_mgr.add_opened_file(str(proj.root_path / "scripts" / "main.sce"))
            ws_mgr.add_opened_file(str(proj.root_path / "datasets" / "data.csv"))
            self.assertEqual(len(ws_mgr.get_opened_files()), 2)

            # Track dock layout
            ws_mgr.set_dock_layout("mock_b64_layout_data")
            self.assertEqual(ws_mgr.get_dock_layout(), "mock_b64_layout_data")

            # Close and reopen workspace
            proj_path = str(proj.root_path)
            ws_mgr.close_workspace()
            self.assertIsNone(ws_mgr.current_project)

            reopened = ws_mgr.open_workspace(proj_path)
            self.assertEqual(len(ws_mgr.get_opened_files()), 2)
            self.assertEqual(ws_mgr.get_dock_layout(), "mock_b64_layout_data")

            bus.stop()
            bus.dispose()
            store.stop()
            store.dispose()


if __name__ == "__main__":
    unittest.main()
