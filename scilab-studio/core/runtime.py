"""
Runtime Context module for Scilab Studio core foundation.

Provides a unified facade wrapping the core services (ServiceRegistry, EventBus,
Lifecycle, ConfigurationManager, Logger) for convenient bootstrap injection.
"""

from dataclasses import dataclass
from typing import Optional

from .service_registry import ServiceRegistry
from .event_bus import EventBus
from .lifecycle import ApplicationLifecycle
from .logger import AppLogger
from .configuration import ConfigurationManager


@dataclass
class RuntimeContext:
    """
    Convenience container holding core runtime infrastructure instances.
    
    Acts as the primary dependency bundle returned by app.bootstrap.Bootstrap.setup()
    and injected into MainWindow and UI controllers.
    """
    service_registry: ServiceRegistry
    event_bus: EventBus
    lifecycle: ApplicationLifecycle
    config: ConfigurationManager
    logger: AppLogger

    def get_service(self, interface_or_class: type) -> type:
        """Lookup a service instance in the registry."""
        return self.service_registry.get(interface_or_class)
