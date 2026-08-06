"""
Configuration Manager service for Scilab Studio core foundation.

Provides strongly-typed configuration models (dataclasses) and JSON persistence.
Broadcasts 'config.updated' events via EventBus when user or system preferences change.
"""

from dataclasses import asdict, dataclass, field
import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

from .service_registry import IService
from .event_bus import Event, EventBus

logger = logging.getLogger(__name__)


@dataclass
class UIConfig:
    """UI specific settings."""
    theme: str = "dark"  # dark, light, system
    window_width: int = 1280
    window_height: int = 800
    is_maximized: bool = False
    sidebar_visible: bool = True
    inspector_visible: bool = True
    console_visible: bool = True


@dataclass
class WorkspaceConfig:
    """Workspace default settings."""
    default_directory: str = field(default_factory=lambda: str(Path.home() / "ScilabProjects"))
    auto_save: bool = True
    recent_projects_limit: int = 10


@dataclass
class ProjectsConfig:
    """Project defaults settings."""
    default_scilab_version: str = "7.0.0"
    default_author: str = ""
    templates_directory: str = field(default_factory=lambda: str(Path.home() / ".scilab_studio" / "templates"))


@dataclass
class EditorConfig:
    """Code & script editor settings."""
    tab_size: int = 4
    word_wrap: bool = False
    show_line_numbers: bool = True
    auto_indentation: bool = True


@dataclass
class AdvancedConfig:
    """Advanced runtime and logging settings."""
    log_level: str = "INFO"
    file_watcher_enabled: bool = True
    max_log_lines: int = 1000


@dataclass
class AppConfig:
    """Root Application Configuration container."""
    ui: UIConfig = field(default_factory=UIConfig)
    workspace: WorkspaceConfig = field(default_factory=WorkspaceConfig)
    projects: ProjectsConfig = field(default_factory=ProjectsConfig)
    editor: EditorConfig = field(default_factory=EditorConfig)
    advanced: AdvancedConfig = field(default_factory=AdvancedConfig)
    custom: Dict[str, Any] = field(default_factory=dict)


class ConfigurationManager(IService):
    """
    Central Configuration Manager maintaining and persisting platform settings.
    """

    def __init__(self, config_path: Optional[str] = None, event_bus: Optional[EventBus] = None) -> None:
        if config_path is None:
            config_path = str(Path.home() / ".scilab_studio" / "config.json")
        self._config_file = Path(config_path)
        self._event_bus = event_bus
        self._config = AppConfig()

    @property
    def config(self) -> AppConfig:
        """Access current strongly-typed application configuration."""
        return self._config

    def set_event_bus(self, event_bus: EventBus) -> None:
        """Inject or update EventBus instance."""
        self._event_bus = event_bus

    def initialize(self) -> None:
        """Load configuration from JSON or initialize with default settings."""
        self.load()

    def start(self) -> None:
        """Activate configuration manager."""
        logger.info("ConfigurationManager started.")

    def stop(self) -> None:
        """Persist current configuration to JSON file on shutdown."""
        self.save()

    def dispose(self) -> None:
        """Release configuration manager resources."""
        logger.debug("ConfigurationManager disposed.")

    def load(self) -> None:
        """Load settings from JSON file on disk."""
        if not self._config_file.exists():
            logger.info("Configuration file not found. Creating default at %s", self._config_file)
            self.save()
            return

        try:
            with open(self._config_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            ui_data = data.get("ui", {})
            workspace_data = data.get("workspace", {})
            projects_data = data.get("projects", {})
            editor_data = data.get("editor", {})
            advanced_data = data.get("advanced", {})
            custom_data = data.get("custom", {})

            self._config = AppConfig(
                ui=UIConfig(**ui_data),
                workspace=WorkspaceConfig(**workspace_data),
                projects=ProjectsConfig(**projects_data),
                editor=EditorConfig(**editor_data),
                advanced=AdvancedConfig(**advanced_data),
                custom=custom_data,
            )
            logger.info("Configuration loaded from %s", self._config_file)
        except Exception as exc:
            logger.exception("Failed to load configuration from %s: %s. Using defaults.", self._config_file, exc)
            self._config = AppConfig()

    def save(self) -> None:
        """Write current settings to JSON file on disk."""
        try:
            self._config_file.parent.mkdir(parents=True, exist_ok=True)
            data = {
                "ui": asdict(self._config.ui),
                "workspace": asdict(self._config.workspace),
                "projects": asdict(self._config.projects),
                "editor": asdict(self._config.editor),
                "advanced": asdict(self._config.advanced),
                "custom": self._config.custom,
            }
            with open(self._config_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            logger.info("Configuration saved to %s", self._config_file)

            if self._event_bus is not None:
                self._event_bus.publish(
                    Event(
                        topic="config.updated",
                        payload={"config": data},
                        sender="ConfigurationManager",
                    )
                )
        except Exception as exc:
            logger.exception("Failed to save configuration to %s: %s", self._config_file, exc)

    def update_ui_config(self, **kwargs: Any) -> None:
        """Update fields in UIConfig and persist."""
        for key, value in kwargs.items():
            if hasattr(self._config.ui, key):
                setattr(self._config.ui, key, value)
        self.save()
