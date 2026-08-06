"""
Scilab Studio Workspace Package.

Manages engineering project structures (.scstudio manifest and subfolders),
project lifecycle operations (Create, Open, Save, Close), and SQLite-backed
recent projects tracking.
"""

from .project import Project, ProjectMetaData
from .recent_projects import RecentProjectsStore, RecentProjectEntry
from .manager import WorkspaceManager

__all__ = [
    "Project",
    "ProjectMetaData",
    "RecentProjectsStore",
    "RecentProjectEntry",
    "WorkspaceManager",
]
