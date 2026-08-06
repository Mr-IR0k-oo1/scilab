"""
Bootstrap module for Scilab Studio foundation.

Orchestrates system startup sequence, dependency injection wiring into ServiceRegistry,
service initialization, and Returns initialized RuntimeContext.
"""

import logging
from typing import Optional

from core.service_registry import ServiceRegistry
from core.event_bus import EventBus
from core.lifecycle import ApplicationLifecycle
from core.logger import AppLogger
from core.configuration import ConfigurationManager
from core.runtime import RuntimeContext
from core.command import CommandRegistry
from core.notification import NotificationManager
from workspace.recent_projects import RecentProjectsStore
from workspace.manager import WorkspaceManager
from workspace.file_watcher import FileWatcherService
from ui.theme import ThemeManager

logger = logging.getLogger(__name__)


class Bootstrap:
    """
    Application Bootstrapper.
    """

    @classmethod
    def setup(cls, config_path: Optional[str] = None, log_dir: Optional[str] = None, db_path: Optional[str] = None) -> RuntimeContext:
        """
        Execute stage-by-stage platform initialization and dependency wiring.
        
        Returns:
            Fully initialized RuntimeContext container.
        """
        registry = ServiceRegistry()

        # Step 1: Core Logging
        app_logger = AppLogger(log_dir=log_dir)
        registry.register(app_logger)

        # Step 2: Configuration Manager
        config_mgr = ConfigurationManager(config_path=config_path)
        registry.register(config_mgr)

        # Step 3: EventBus Message Broker
        event_bus = EventBus()
        registry.register(event_bus)

        # Step 4: Application Lifecycle State Machine
        lifecycle = ApplicationLifecycle(event_bus=event_bus)
        registry.register(lifecycle)

        # Connect EventBus back to Logger and Config
        app_logger.set_event_bus(event_bus)
        config_mgr.set_event_bus(event_bus)

        # Step 5: Command Registry & Notification Manager
        cmd_registry = CommandRegistry(event_bus=event_bus)
        registry.register(cmd_registry)

        notif_mgr = NotificationManager(event_bus=event_bus)
        registry.register(notif_mgr)

        # Step 6: Workspace Storage & Recent Projects
        recent_store = RecentProjectsStore(db_path=db_path)
        registry.register(recent_store)

        # Step 7: Workspace Manager & File Watcher
        workspace_mgr = WorkspaceManager(recent_store=recent_store, event_bus=event_bus)
        registry.register(workspace_mgr)

        file_watcher = FileWatcherService(event_bus=event_bus)
        registry.register(file_watcher)

        # Step 8: Theme Manager
        theme_mgr = ThemeManager(config_mgr=config_mgr, event_bus=event_bus)
        registry.register(theme_mgr)

        # Initialize all services in registration order
        registry.initialize_all()

        # Start all services in registration order
        registry.start_all()

        runtime = RuntimeContext(
            service_registry=registry,
            event_bus=event_bus,
            lifecycle=lifecycle,
            config=config_mgr,
            logger=app_logger,
        )

        logger.info("Application bootstrap completed successfully.")
        return runtime
