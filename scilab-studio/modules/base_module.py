"""
Base Module abstraction for Scilab Studio foundation.

All functional feature modules subclass BaseModule.

Architectural Enforcement Rules:
--------------------------------
1. No module may hold direct references to another feature module.
2. Modules resolve system dependencies exclusively via ServiceRegistry.
3. Modules emit state updates and listen to system events exclusively via EventBus.
"""

from abc import ABC, abstractmethod
import logging
from typing import Optional, Type, TypeVar

from core.service_registry import IService, ServiceRegistry
from core.event_bus import Event, EventBus, EventHandler

logger = logging.getLogger(__name__)

T = TypeVar("T")


class BaseModule(IService, ABC):
    """
    Abstract Base Class for Scilab Studio modules.
    """

    def __init__(self, module_name: str, service_registry: ServiceRegistry) -> None:
        self.module_name = module_name
        self.service_registry = service_registry
        self._event_bus: Optional[EventBus] = None

    @property
    def event_bus(self) -> EventBus:
        """Resolve EventBus from ServiceRegistry on demand."""
        if self._event_bus is None:
            self._event_bus = self.service_registry.get(EventBus)
        return self._event_bus

    def get_service(self, interface_or_class: Type[T]) -> T:
        """Helper to resolve a service dependency from ServiceRegistry."""
        return self.service_registry.get(interface_or_class)

    def subscribe_event(self, topic: str, handler: EventHandler) -> None:
        """Subscribe module callback to an EventBus topic."""
        self.event_bus.subscribe(topic, handler)

    def publish_event(self, topic: str, payload: Optional[dict] = None) -> None:
        """Publish a module event on EventBus."""
        self.event_bus.publish(
            Event(
                topic=topic,
                payload=payload or {},
                sender=self.module_name,
            )
        )

    def initialize(self) -> None:
        """Default module initialization hook. Override in subclasses."""
        logger.info("Module '%s' initialized.", self.module_name)

    def start(self) -> None:
        """Default module activation hook. Override in subclasses."""
        logger.info("Module '%s' started.", self.module_name)

    def stop(self) -> None:
        """Default module pause hook. Override in subclasses."""
        logger.info("Module '%s' stopped.", self.module_name)

    def dispose(self) -> None:
        """Default module cleanup hook. Override in subclasses."""
        logger.info("Module '%s' disposed.", self.module_name)
