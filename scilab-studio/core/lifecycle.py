"""
Application Lifecycle service for Scilab Studio core foundation.

Manages application-wide phase transitions and state machine.
Publishes lifecycle events to notify UI and services when the platform boots,
runs, or initiates graceful termination.
"""

from enum import Enum, auto
import logging
import signal
import sys
from typing import Optional

from .service_registry import IService
from .event_bus import Event, EventBus

logger = logging.getLogger(__name__)


class LifecycleState(Enum):
    """Enumeration of platform lifecycle stages."""
    PRE_INIT = auto()
    INITIALIZING = auto()
    STARTING = auto()
    RUNNING = auto()
    SHUTTING_DOWN = auto()
    STOPPED = auto()


class ApplicationLifecycle(IService):
    """
    Coordinates application lifecycle phases and broadcasts state transitions.
    
    Acts as the master state machine governing startup sequences, runtime execution,
    and orderly shutdown handling.
    """

    def __init__(self, event_bus: Optional[EventBus] = None) -> None:
        self._state = LifecycleState.PRE_INIT
        self._event_bus = event_bus

    @property
    def state(self) -> LifecycleState:
        """Get current platform lifecycle state."""
        return self._state

    def set_event_bus(self, event_bus: EventBus) -> None:
        """Inject or update EventBus dependency."""
        self._event_bus = event_bus

    def initialize(self) -> None:
        """Transition lifecycle state to INITIALIZING."""
        self._transition_to(LifecycleState.INITIALIZING)
        self._register_signal_handlers()

    def start(self) -> None:
        """Transition lifecycle state to STARTING, then RUNNING."""
        self._transition_to(LifecycleState.STARTING)
        self._transition_to(LifecycleState.RUNNING)

    def stop(self) -> None:
        """Transition lifecycle state to SHUTTING_DOWN."""
        if self._state not in (LifecycleState.SHUTTING_DOWN, LifecycleState.STOPPED):
            self._transition_to(LifecycleState.SHUTTING_DOWN)

    def dispose(self) -> None:
        """Transition lifecycle state to STOPPED."""
        self._transition_to(LifecycleState.STOPPED)

    def _transition_to(self, new_state: LifecycleState) -> None:
        """Execute validated lifecycle state transition."""
        old_state = self._state
        self._state = new_state
        logger.info("Lifecycle state changed: %s -> %s", old_state.name, new_state.name)

        if self._event_bus is not None:
            self._event_bus.publish(
                Event(
                    topic="lifecycle.state_changed",
                    payload={"old_state": old_state.name, "new_state": new_state.name},
                    sender="ApplicationLifecycle",
                )
            )

    def _register_signal_handlers(self) -> None:
        """Register OS signal traps for SIGINT and SIGTERM."""
        def handle_signal(sig: int, frame: Optional[object]) -> None:
            logger.warning("Received termination signal %d. Triggering graceful shutdown.", sig)
            self.stop()

        try:
            signal.signal(signal.SIGINT, handle_signal)
            signal.signal(signal.SIGTERM, handle_signal)
        except (ValueError, OSError) as err:
            logger.debug("Could not register OS signal handlers: %s", err)
