"""
Unit tests for workspace Project creation, loading, and RecentProjectsStore SQLite DB.
"""

from pathlib import Path
import tempfile
import unittest

from core.event_bus import EventBus
from workspace.project import Project, REQUIRED_SUBDIRECTORIES, PROJECT_MANIFEST_NAME
from workspace.recent_projects import RecentProjectsStore
from workspace.manager import WorkspaceManager


class TestWorkspace(unittest.TestCase):

    def test_project_creation_and_loading(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            proj = Project.create(
                name="TestEngineeringProj",
                parent_dir=tmp_path,
                author="FOSSEE Contributor",
                description="Testing Phase 1 foundation workspace.",
            )

            self.assertTrue(proj.root_path.exists())
            self.assertTrue((proj.root_path / PROJECT_MANIFEST_NAME).exists())

            for sub in REQUIRED_SUBDIRECTORIES:
                self.assertTrue((proj.root_path / sub).is_dir())

            loaded = Project.load(proj.root_path)
            self.assertEqual(loaded.metadata.name, "TestEngineeringProj")
            self.assertEqual(loaded.metadata.author, "FOSSEE Contributor")

    def test_recent_projects_store_sqlite(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            db_file = tmp_path / "recent.db"
            store = RecentProjectsStore(db_path=str(db_file))
            store.initialize()
            store.start()

            proj1_path = str(tmp_path / "Proj1")
            proj2_path = str(tmp_path / "Proj2")

            store.add_project("Proj1", proj1_path)
            store.add_project("Proj2", proj2_path)

            recents = store.get_recent_projects(limit=5)
            self.assertEqual(len(recents), 2)
            # Most recently added is first
            self.assertEqual(recents[0].name, "Proj2")

            store.pin_project(proj1_path, pinned=True)
            recents_after_pin = store.get_recent_projects(limit=5)
            # Pinned item comes first
            self.assertEqual(recents_after_pin[0].name, "Proj1")

            store.stop()
            store.dispose()

    def test_workspace_manager_lifecycle(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            bus = EventBus()
            bus.initialize()
            bus.start()

            db_file = tmp_path / "recent.db"
            store = RecentProjectsStore(db_path=str(db_file))
            store.initialize()
            store.start()

            ws_mgr = WorkspaceManager(recent_store=store, event_bus=bus)
            ws_mgr.initialize()

            proj = ws_mgr.create_project("EngineSim", parent_dir=str(tmp_path))
            self.assertIs(ws_mgr.current_project, proj)
            self.assertEqual(ws_mgr.current_project.metadata.name, "EngineSim")

            ws_mgr.close_project()
            self.assertIsNone(ws_mgr.current_project)

            opened = ws_mgr.open_project(str(proj.root_path))
            self.assertIs(ws_mgr.current_project, opened)

            bus.stop()
            bus.dispose()
            store.stop()
            store.dispose()


if __name__ == "__main__":
    unittest.main()
