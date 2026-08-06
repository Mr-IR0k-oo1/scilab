"""
Scilab Studio Core Package.

Provides the runtime container, service registry, event bus,
lifecycle management, logging, and configuration services.
"""

from .service_registry import IService, ServiceRegistry, ServiceState
from .event_bus import Event, EventBus, EventHandler
from .lifecycle import ApplicationLifecycle, LifecycleState
from .logger import AppLogger
from .configuration import ConfigurationManager, AppConfig, UIConfig, WorkspaceConfig
from .runtime import RuntimeContext
from .command import Command, CommandRegistry
from .notification import Notification, NotificationType, NotificationManager

__all__ = [
    "IService",
    "ServiceRegistry",
    "ServiceState",
    "Event",
    "EventBus",
    "EventHandler",
    "ApplicationLifecycle",
    "LifecycleState",
    "AppLogger",
    "ConfigurationManager",
    "AppConfig",
    "UIConfig",
    "WorkspaceConfig",
    "RuntimeContext",
    "Command",
    "CommandRegistry",
    "Notification",
    "NotificationType",
    "NotificationManager",
]
