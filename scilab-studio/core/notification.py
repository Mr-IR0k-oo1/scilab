"""
Notification Manager service for Scilab Studio foundation.

Provides platform notification dispatching (Success, Warning, Error, Info)
broadcasting 'notification.show' events to UI toast overlays and status bars.
"""

from dataclasses import dataclass
from enum import Enum, auto
import logging
from typing import Optional

from .service_registry import IService
from .event_bus import Event, EventBus

logger = logging.getLogger(__name__)


class NotificationType(Enum):
    """Notification severity types."""
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


@dataclass
class Notification:
    """Notification payload structure."""
    title: str
    message: str
    type: NotificationType = NotificationType.INFO
    duration_ms: int = 4000


class NotificationManager(IService):
    """
    Central Notification Service managing toast alerts across the application.
    """

    def __init__(self, event_bus: Optional[EventBus] = None) -> None:
        self._event_bus = event_bus

    def set_event_bus(self, event_bus: EventBus) -> None:
        """Inject or update EventBus dependency."""
        self._event_bus = event_bus

    def initialize(self) -> None:
        """Initialize notification manager."""
        logger.debug("NotificationManager initialized.")

    def start(self) -> None:
        """Activate notification service."""
        logger.info("NotificationManager started.")

    def stop(self) -> None:
        """Deactivate notification service."""
        logger.info("NotificationManager stopped.")

    def dispose(self) -> None:
        """Release notification service resources."""
        logger.debug("NotificationManager disposed.")

    def notify(
        self,
        title: str,
        message: str,
        type_: NotificationType = NotificationType.INFO,
        duration_ms: int = 4000,
    ) -> None:
        """
        Dispatch a notification object to the EventBus.
        """
        notif = Notification(title=title, message=message, type=type_, duration_ms=duration_ms)
        logger.info("[%s Notification] %s: %s", type_.value.upper(), title, message)

        if self._event_bus is not None:
            self._event_bus.publish(
                Event(
                    topic="notification.show",
                    payload={
                        "title": notif.title,
                        "message": notif.message,
                        "type": notif.type.value,
                        "duration_ms": notif.duration_ms,
                    },
                    sender="NotificationManager",
                ),
                async_gui=True,
            )

    def success(self, title: str, message: str, duration_ms: int = 4000) -> None:
        """Convenience method to dispatch a Success notification."""
        self.notify(title, message, NotificationType.SUCCESS, duration_ms)

    def warning(self, title: str, message: str, duration_ms: int = 4000) -> None:
        """Convenience method to dispatch a Warning notification."""
        self.notify(title, message, NotificationType.WARNING, duration_ms)

    def error(self, title: str, message: str, duration_ms: int = 5000) -> None:
        """Convenience method to dispatch an Error notification."""
        self.notify(title, message, NotificationType.ERROR, duration_ms)

    def info(self, title: str, message: str, duration_ms: int = 4000) -> None:
        """Convenience method to dispatch an Information notification."""
        self.notify(title, message, NotificationType.INFO, duration_ms)
