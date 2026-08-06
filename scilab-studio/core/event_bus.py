"""
EventBus module for Scilab Studio core foundation.

Provides an asynchronous and synchronous publish-subscribe message broker.
Modules and services communicate strictly through EventBus to enforce complete
decoupling and loose integration across components.

Architectural Rationale:
-----------------------
By preventing direct method invocation or imports between feature modules,
the EventBus ensures that modules can be enabled, disabled, or tested in isolation.
It also includes a PySide6 Qt Signal Bridge to guarantee thread safety when background
tasks notify UI components.
"""

from dataclasses import dataclass, field
import fnmatch
import logging
import threading
import time
from typing import Any, Callable, Dict, List, Optional, Set
from PySide6.QtCore import QObject, Signal

from .service_registry import IService

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Event:
    """
    Immutable Event object transferred via EventBus.
    
    Attributes:
        topic: Hierarchical dot-separated topic string (e.g., 'workspace.project.opened').
        payload: Event data dictionary.
        sender: Identifier string of the publishing component.
        timestamp: Epoch timestamp when event was instantiated.
    """
    topic: str
    payload: Dict[str, Any] = field(default_factory=dict)
    sender: str = "system"
    timestamp: float = field(default_factory=time.time)


EventHandler = Callable[[Event], None]


class _QtSignalBridge(QObject):
    """Internal PySide6 QObject to marshal event dispatching to the main Qt GUI thread."""
    event_emitted = Signal(object, object)  # (Event, EventHandler)

    def __init__(self) -> None:
        super().__init__()
        self.event_emitted.connect(self._handle_signal)

    def _handle_signal(self, event: Event, handler: EventHandler) -> None:
        try:
            handler(event)
        except Exception as exc:
            logger.exception("Error executing Qt event handler for topic '%s': %s", event.topic, exc)


class EventBus(IService):
    """
    Central event dispatching service implementing publish-subscribe pattern.
    
    Supports hierarchical topic matching (e.g., 'workspace.*' matching 'workspace.opened')
    and thread-safe delivery via Qt signals when dispatching across thread boundaries.
    """

    def __init__(self) -> None:
        self._subscriptions: Dict[str, Set[EventHandler]] = {}
        self._lock = threading.RLock()
        self._active = False
        self._qt_bridge: Optional[_QtSignalBridge] = None

    def initialize(self) -> None:
        """Initialize subscriptions map and instantiate Qt Signal bridge."""
        with self._lock:
            if self._qt_bridge is None:
                self._qt_bridge = _QtSignalBridge()
            logger.debug("EventBus initialized.")

    def start(self) -> None:
        """Activate event processing."""
        with self._lock:
            self._active = True
            logger.info("EventBus started.")

    def stop(self) -> None:
        """Deactivate event processing."""
        with self._lock:
            self._active = False
            logger.info("EventBus stopped.")

    def dispose(self) -> None:
        """Clear all subscriptions and release bridge resources."""
        with self._lock:
            self._subscriptions.clear()
            self._qt_bridge = None
            self._active = False
            logger.debug("EventBus disposed.")

    def subscribe(self, topic_pattern: str, handler: EventHandler) -> None:
        """
        Subscribe a callback function to a topic or wildcard topic pattern.
        
        Args:
            topic_pattern: Exact topic (e.g., 'workspace.opened') or wildcard pattern (e.g., 'workspace.*').
            handler: Callable taking an Event instance as its single argument.
        """
        with self._lock:
            if topic_pattern not in self._subscriptions:
                self._subscriptions[topic_pattern] = set()
            self._subscriptions[topic_pattern].add(handler)
            logger.debug("Subscribed to '%s' with handler %s", topic_pattern, handler.__name__)

    def unsubscribe(self, topic_pattern: str, handler: EventHandler) -> None:
        """Unsubscribe a callback function from a topic pattern."""
        with self._lock:
            if topic_pattern in self._subscriptions:
                self._subscriptions[topic_pattern].discard(handler)
                if not self._subscriptions[topic_pattern]:
                    del self._subscriptions[topic_pattern]
                logger.debug("Unsubscribed handler %s from '%s'", handler.__name__, topic_pattern)

    def publish(self, event: Event, async_gui: bool = False) -> None:
        """
        Publish an event to all matching subscribers.
        
        Args:
            event: Event object containing topic, sender, payload.
            async_gui: If True, dispatches through Qt Signal bridge to ensure execution on main GUI thread.
        """
        if not self._active:
            logger.warning("EventBus received event '%s' while inactive. Dropping event.", event.topic)
            return

        matching_handlers: List[EventHandler] = []
        with self._lock:
            for pattern, handlers in list(self._subscriptions.items()):
                if pattern == "*" or pattern == event.topic or fnmatch.fnmatch(event.topic, pattern):
                    matching_handlers.extend(handlers)

        logger.debug("Publishing event '%s' from '%s' to %d subscriber(s)", event.topic, event.sender, len(matching_handlers))

        for handler in matching_handlers:
            if async_gui and self._qt_bridge is not None:
                self._qt_bridge.event_emitted.emit(event, handler)
            else:
                try:
                    handler(event)
                except Exception as exc:
                    logger.exception("Error executing handler %s for topic '%s': %s", getattr(handler, '__name__', str(handler)), event.topic, exc)
