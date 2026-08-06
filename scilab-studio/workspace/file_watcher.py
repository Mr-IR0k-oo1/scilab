"""
File Watcher service for Scilab Studio workspace system.

Uses PySide6 QFileSystemWatcher to recursively monitor active project directories,
detecting file creations, deletions, modifications, and path updates, and publishing
events to EventBus so Project Explorer and editors update dynamically.
"""

import logging
from pathlib import Path
from typing import List, Optional, Set
from PySide6.QtCore import QFileSystemWatcher, QObject, Slot

from core.service_registry import IService
from core.event_bus import Event, EventBus

logger = logging.getLogger(__name__)


class FileWatcherService(IService):
    """
    Service monitoring file system mutations inside active workspace.
    """

    def __init__(self, event_bus: Optional[EventBus] = None) -> None:
        self._event_bus = event_bus
        self._watcher: Optional[QFileSystemWatcher] = None
        self._watched_paths: Set[str] = set()
        self._root_path: Optional[Path] = None

    def set_event_bus(self, event_bus: EventBus) -> None:
        """Inject or update EventBus dependency."""
        self._event_bus = event_bus

    def initialize(self) -> None:
        """Initialize QFileSystemWatcher."""
        self._watcher = QFileSystemWatcher()
        self._watcher.fileChanged.connect(self._on_file_changed)
        self._watcher.directoryChanged.connect(self._on_directory_changed)
        logger.debug("FileWatcherService initialized.")

    def start(self) -> None:
        """Activate file watcher service."""
        if self._event_bus is not None:
            self._event_bus.subscribe("workspace.opened", self._on_workspace_opened)
            self._event_bus.subscribe("workspace.closed", self._on_workspace_closed)
        logger.info("FileWatcherService started.")

    def stop(self) -> None:
        """Unwatch all paths."""
        self._clear_watched_paths()
        logger.info("FileWatcherService stopped.")

    def dispose(self) -> None:
        """Release watcher resources."""
        self._clear_watched_paths()
        self._watcher = None
        logger.debug("FileWatcherService disposed.")

    def set_watch_directory(self, root_path: Path) -> None:
        """Set active project root directory to watch recursively."""
        self._clear_watched_paths()
        if not root_path.exists() or not root_path.is_dir():
            logger.warning("Invalid directory path for FileWatcherService: %s", root_path)
            return

        self._root_path = root_path
        dirs_to_watch = [str(root_path)]
        for sub in root_path.rglob("*"):
            if sub.is_dir():
                dirs_to_watch.append(str(sub))

        if self._watcher is not None and dirs_to_watch:
            self._watcher.addPaths(dirs_to_watch)
            self._watched_paths.update(dirs_to_watch)
            logger.info("FileWatcherService watching %d directory path(s) under %s", len(dirs_to_watch), root_path)

    def _clear_watched_paths(self) -> None:
        """Remove all paths from watcher."""
        if self._watcher is not None and self._watched_paths:
            self._watcher.removePaths(list(self._watched_paths))
            self._watched_paths.clear()
        self._root_path = None

    def _on_workspace_opened(self, event: Event) -> None:
        """Event handler for workspace.opened."""
        path_str = event.payload.get("path")
        if path_str:
            self.set_watch_directory(Path(path_str))

    def _on_workspace_closed(self, event: Event) -> None:
        """Event handler for workspace.closed."""
        self._clear_watched_paths()

    @Slot(str)
    def _on_file_changed(self, path_str: str) -> None:
        """Qt slot triggered when a monitored file changes."""
        logger.debug("File changed: %s", path_str)
        if self._event_bus is not None:
            self._event_bus.publish(
                Event(
                    topic="workspace.file_modified",
                    payload={"path": path_str},
                    sender="FileWatcherService",
                )
            )

    @Slot(str)
    def _on_directory_changed(self, path_str: str) -> None:
        """Qt slot triggered when a monitored directory mutates (file added/removed/renamed)."""
        logger.debug("Directory mutated: %s", path_str)
        # Re-index newly created subdirectories
        if self._root_path is not None and Path(path_str).exists():
            for sub in Path(path_str).iterdir():
                if sub.is_dir() and str(sub) not in self._watched_paths:
                    if self._watcher is not None:
                        self._watcher.addPath(str(sub))
                        self._watched_paths.add(str(sub))

        if self._event_bus is not None:
            self._event_bus.publish(
                Event(
                    topic="workspace.directory_changed",
                    payload={"path": path_str},
                    sender="FileWatcherService",
                )
            )
