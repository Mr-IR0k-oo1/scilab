"""
Recent Projects database store for Scilab Studio workspace system.

Uses SQLite database to manage Most Recently Used (MRU) projects list,
persisting project paths, opening timestamps, and pinned status across app sessions.
"""

from dataclasses import dataclass
import datetime
import logging
from pathlib import Path
import sqlite3

from core.service_registry import IService

logger = logging.getLogger(__name__)


@dataclass
class RecentProjectEntry:
    """DTO representing a recently opened project record."""
    name: str
    path: str
    last_opened: str
    is_pinned: bool = False


class RecentProjectsStore(IService):
    """
    SQLite-backed storage manager for recent project history.
    """

    def __init__(self, db_path: Optional[str] = None) -> None:
        if db_path is None:
            db_path = str(Path.home() / ".scilab_studio" / "recent_projects.db")
        self._db_file = Path(db_path)
        self._conn: Optional[sqlite3.Connection] = None

    def initialize(self) -> None:
        """Connect to SQLite database and ensure schema exists."""
        self._db_file.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(self._db_file), check_same_thread=False)
        self._create_tables()
        logger.info("RecentProjectsStore initialized at %s", self._db_file)

    def start(self) -> None:
        """Activate store service."""
        logger.info("RecentProjectsStore started.")

    def stop(self) -> None:
        """Commit transactions and close SQLite connection."""
        if self._conn:
            self._conn.commit()
            logger.info("RecentProjectsStore stopped.")

    def dispose(self) -> None:
        """Close database connection handle."""
        if self._conn:
            self._conn.close()
            self._conn = None
            logger.debug("RecentProjectsStore disposed.")

    def _create_tables(self) -> None:
        """Initialize SQLite database tables."""
        if not self._conn:
            return
        query = """
        CREATE TABLE IF NOT EXISTS recent_projects (
            path TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            last_opened TEXT NOT NULL,
            is_pinned INTEGER DEFAULT 0
        );
        """
        with self._conn:
            self._conn.execute(query)

    def add_project(self, name: str, path: str) -> None:
        """Record or update project opening in MRU database."""
        if not self._conn:
            return
        now_str = datetime.datetime.now(datetime.timezone.utc).isoformat()
        query = """
        INSERT INTO recent_projects (path, name, last_opened, is_pinned)
        VALUES (?, ?, ?, 0)
        ON CONFLICT(path) DO UPDATE SET
            name = excluded.name,
            last_opened = excluded.last_opened;
        """
        with self._conn:
            self._conn.execute(query, (str(Path(path).resolve()), name, now_str))

    def remove_project(self, path: str) -> None:
        """Remove a project path from recent projects list."""
        if not self._conn:
            return
        query = "DELETE FROM recent_projects WHERE path = ?"
        with self._conn:
            self._conn.execute(query, (str(Path(path).resolve()),))

    def pin_project(self, path: str, pinned: bool) -> None:
        """Toggle pinned status of a recent project entry."""
        if not self._conn:
            return
        query = "UPDATE recent_projects SET is_pinned = ? WHERE path = ?"
        with self._conn:
            self._conn.execute(query, (1 if pinned else 0, str(Path(path).resolve())))

    def get_recent_projects(self, limit: int = 10) -> List[RecentProjectEntry]:
        """Fetch recently opened projects ordered by pinned status and last_opened timestamp."""
        if not self._conn:
            return []
        query = """
        SELECT name, path, last_opened, is_pinned
        FROM recent_projects
        ORDER BY is_pinned DESC, last_opened DESC
        LIMIT ?;
        """
        cursor = self._conn.cursor()
        cursor.execute(query, (limit,))
        rows = cursor.fetchall()
        return [
            RecentProjectEntry(
                name=row[0],
                path=row[1],
                last_opened=row[2],
                is_pinned=bool(row[3]),
            )
            for row in rows
        ]

    def clear_all(self) -> None:
        """Purge all recent project records."""
        if not self._conn:
            return
        with self._conn:
            self._conn.execute("DELETE FROM recent_projects;")
