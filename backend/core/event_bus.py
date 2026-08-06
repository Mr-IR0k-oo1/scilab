"""
Async EventBus module for Scilab Studio Backend.

Allows decoupled event emission and real-time WebSocket streaming of Scilab
console outputs, progress updates, execution states, and warnings.
"""

from dataclasses import dataclass, field
import asyncio
import logging
import time
from typing import Any, Callable, Dict, List, Set

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Event:
    """Immutable Event object."""
    topic: str
    payload: Dict[str, Any] = field(default_factory=dict)
    sender: str = "backend"
    timestamp: float = field(default_factory=time.time)


AsyncEventHandler = Callable[[Event], Any]


class AsyncEventBus:
    """
    Asynchronous Publish-Subscribe Message Broker.
    """

    def __init__(self) -> None:
        self._subscriptions: Dict[str, Set[AsyncEventHandler]] = {}
        self._lock = asyncio.Lock()

    async def subscribe(self, topic: str, handler: AsyncEventHandler) -> None:
        """Subscribe an async handler to a topic."""
        async with self._lock:
            if topic not in self._subscriptions:
                self._subscriptions[topic] = set()
            self._subscriptions[topic].add(handler)

    async def unsubscribe(self, topic: str, handler: AsyncEventHandler) -> None:
        """Unsubscribe an async handler from a topic."""
        async with self._lock:
            if topic in self._subscriptions:
                self._subscriptions[topic].discard(handler)
                if not self._subscriptions[topic]:
                    del self._subscriptions[topic]

    async def publish(self, event: Event) -> None:
        """Publish an event asynchronously to subscribers."""
        subscribers: List[AsyncEventHandler] = []
        async with self._lock:
            for pattern, handlers in self._subscriptions.items():
                if pattern == "*" or pattern == event.topic:
                    subscribers.extend(handlers)

        for handler in subscribers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(event)
                else:
                    handler(event)
            except Exception as exc:
                logger.exception("Error executing event handler for topic '%s': %s", event.topic, exc)


event_bus = AsyncEventBus()
