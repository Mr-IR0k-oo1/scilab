"""
Workspace Manager service for Scilab Studio foundation.

Coordinates active project & workspace state, project creation, loading, saving,
closing, opened files tracking, layout memory, and integrates with RecentProjectsStore and EventBus.
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from core.service_registry import IService
from core.event_bus import Event, EventBus
from .project import Project, ProjectMetaData
from .recent_projects import RecentProjectsStore

logger = logging.getLogger(__name__)


class WorkspaceManager(IService):
    """
    Central Service managing workspace active project lifecycle and workspace state memory.
    """

    def __init__(
        self,
        recent_store: Optional[RecentProjectsStore] = None,
        event_bus: Optional[EventBus] = None,
    ) -> None:
        self._current_project: Optional[Project] = None
        self._recent_store = recent_store
        self._event_bus = event_bus

    @property
    def current_project(self) -> Optional[Project]:
        """Access currently loaded active project instance."""
        return self._current_project

    def set_dependencies(self, recent_store: RecentProjectsStore, event_bus: EventBus) -> None:
        """Inject or update service dependencies."""
        self._recent_store = recent_store
        self._event_bus = event_bus

    def initialize(self) -> None:
        """Initialize workspace manager state."""
        logger.debug("WorkspaceManager initialized.")

    def start(self) -> None:
        """Activate workspace manager."""
        logger.info("WorkspaceManager started.")

    def stop(self) -> None:
        """Save active project state before shutdown."""
        if self._current_project is not None:
            self.save_project()
        logger.info("WorkspaceManager stopped.")

    def dispose(self) -> None:
        """Release active project references."""
        self._current_project = None
        logger.debug("WorkspaceManager disposed.")

    def create_project(self, name: str, parent_dir: str, author: str = "", description: str = "") -> Project:
        """
        Create a new .scstudio project package and set as active project.
        
        Args:
            name: Project name.
            parent_dir: Parent directory path.
            author: Author string.
            description: Project description.
            
        Returns:
            Created Project instance.
        """
        if self._current_project is not None:
            self.close_project()

        project = Project.create(
            name=name,
            parent_dir=Path(parent_dir),
            author=author,
            description=description,
        )
        self._current_project = project

        if self._recent_store is not None:
            self._recent_store.add_project(project.metadata.name, str(project.root_path))

        if self._event_bus is not None:
            self._event_bus.publish(
                Event(
                    topic="workspace.opened",
                    payload={
                        "project": project,
                        "name": project.metadata.name,
                        "path": str(project.root_path),
                        "manifest_path": str(project.manifest_path),
                    },
                    sender="WorkspaceManager",
                )
            )

        logger.info("Workspace set active project: '%s'", project.metadata.name)
        return project

    # Workspace API Aliases
    create_workspace = create_project

    def open_project(self, path: str) -> Project:
        """
        Open an existing project from disk and set as active project.
        
        Args:
            path: Path to directory or project.scstudio manifest file.
            
        Returns:
            Loaded Project instance.
        """
        if self._current_project is not None:
            self.close_project()

        project = Project.load(Path(path))
        self._current_project = project

        if self._recent_store is not None:
            self._recent_store.add_project(project.metadata.name, str(project.root_path))

        if self._event_bus is not None:
            self._event_bus.publish(
                Event(
                    topic="workspace.opened",
                    payload={
                        "project": project,
                        "name": project.metadata.name,
                        "path": str(project.root_path),
                        "manifest_path": str(project.manifest_path),
                    },
                    sender="WorkspaceManager",
                )
            )

        logger.info("Workspace opened active project: '%s'", project.metadata.name)
        return project

    # Workspace API Aliases
    open_workspace = open_project

    def save_project(self) -> None:
        """Persist active project metadata and workspace state to disk."""
        if self._current_project is None:
            logger.warning("No active project to save.")
            return

        self._current_project.save()

        if self._event_bus is not None:
            self._event_bus.publish(
                Event(
                    topic="workspace.saved",
                    payload={
                        "project": self._current_project,
                        "name": self._current_project.metadata.name,
                        "path": str(self._current_project.root_path),
                    },
                    sender="WorkspaceManager",
                )
            )

        logger.info("Workspace saved active project: '%s'", self._current_project.metadata.name)

    # Workspace API Aliases
    save_workspace = save_project

    def close_project(self) -> None:
        """Close active project and reset workspace state."""
        if self._current_project is None:
            return

        closing_project = self._current_project
        self.save_project()
        self._current_project = None

        if self._event_bus is not None:
            self._event_bus.publish(
                Event(
                    topic="workspace.closed",
                    payload={
                        "name": closing_project.metadata.name,
                        "path": str(closing_project.root_path),
                    },
                    sender="WorkspaceManager",
                )
            )

        logger.info("Workspace closed active project: '%s'", closing_project.metadata.name)

    # Workspace API Aliases
    close_workspace = close_project

    # Workspace State Memory (Opened Files, Layout, Datasets, Window State)
    def _get_state_dict(self) -> Dict[str, Any]:
        if self._current_project is None:
            return {}
        if "workspace_state" not in self._current_project.metadata.settings:
            self._current_project.metadata.settings["workspace_state"] = {
                "opened_files": [],
                "recent_datasets": [],
                "dock_layout": "",
                "theme": "dark",
            }
        return self._current_project.metadata.settings["workspace_state"]

    def add_opened_file(self, file_path: str) -> None:
        """Track an opened file tab in workspace memory."""
        if self._current_project is None:
            return
        state = self._get_state_dict()
        opened = state.setdefault("opened_files", [])
        if file_path not in opened:
            opened.append(file_path)
            self.save_project()

        if self._event_bus is not None:
            self._event_bus.publish(
                Event(
                    topic="workspace.file_opened",
                    payload={"file_path": file_path},
                    sender="WorkspaceManager",
                )
            )

    def remove_opened_file(self, file_path: str) -> None:
        """Remove an opened file tab from workspace memory."""
        if self._current_project is None:
            return
        state = self._get_state_dict()
        opened = state.setdefault("opened_files", [])
        if file_path in opened:
            opened.remove(file_path)
            self.save_project()

        if self._event_bus is not None:
            self._event_bus.publish(
                Event(
                    topic="workspace.file_closed",
                    payload={"file_path": file_path},
                    sender="WorkspaceManager",
                )
            )

    def get_opened_files(self) -> List[str]:
        """Retrieve list of remembered open file paths."""
        if self._current_project is None:
            return []
        state = self._get_state_dict()
        return list(state.get("opened_files", []))

    def add_recent_dataset(self, dataset_path: str) -> None:
        """Track a dataset file in workspace memory."""
        if self._current_project is None:
            return
        state = self._get_state_dict()
        datasets = state.setdefault("recent_datasets", [])
        if dataset_path in datasets:
            datasets.remove(dataset_path)
        datasets.insert(0, dataset_path)
        state["recent_datasets"] = datasets[:10]
        self.save_project()

    def get_recent_datasets(self) -> List[str]:
        """Retrieve list of recent datasets."""
        if self._current_project is None:
            return []
        state = self._get_state_dict()
        return list(state.get("recent_datasets", []))

    def set_dock_layout(self, layout_b64: str) -> None:
        """Save dock layout string into workspace state."""
        if self._current_project is None:
            return
        state = self._get_state_dict()
        state["dock_layout"] = layout_b64
        self.save_project()

    def get_dock_layout(self) -> Optional[str]:
        """Get remembered dock layout string."""
        if self._current_project is None:
            return None
        state = self._get_state_dict()
        return state.get("dock_layout")
