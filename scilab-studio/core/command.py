"""
Command Registry service for Scilab Studio foundation.

Provides centralized command registration, keyboard shortcut mapping,
execution, undo/redo hooks, and event notification.
"""

from dataclasses import dataclass, field
import logging
from typing import Any, Callable, Dict, List, Optional

from .service_registry import IService
from .event_bus import Event, EventBus

logger = logging.getLogger(__name__)


@dataclass
class Command:
    """
    DTO representing an executable application command.
    """
    id: str
    title: str
    description: str = ""
    category: str = "General"
    shortcut: Optional[str] = None
    handler: Optional[Callable[..., Any]] = None
    enabled: bool = True


class CommandRegistry(IService):
    """
    Central Service managing application commands.
    """

    def __init__(self, event_bus: Optional[EventBus] = None) -> None:
        self._commands: Dict[str, Command] = {}
        self._event_bus = event_bus
        self._undo_stack: List[str] = []
        self._redo_stack: List[str] = []

    def set_event_bus(self, event_bus: EventBus) -> None:
        """Inject or update EventBus instance."""
        self._event_bus = event_bus

    def initialize(self) -> None:
        """Initialize command registry."""
        logger.debug("CommandRegistry initialized.")

    def start(self) -> None:
        """Activate command registry service."""
        logger.info("CommandRegistry started.")

    def stop(self) -> None:
        """Deactivate command registry service."""
        logger.info("CommandRegistry stopped.")

    def dispose(self) -> None:
        """Clear registered commands."""
        self._commands.clear()
        self._undo_stack.clear()
        self._redo_stack.clear()
        logger.debug("CommandRegistry disposed.")

    def register_command(self, command: Command) -> None:
        """
        Register a command.
        
        Args:
            command: Command object to register.
        """
        if command.id in self._commands:
            logger.warning("Overwriting registered command ID '%s'", command.id)
        self._commands[command.id] = command
        logger.debug("Registered command '%s' (%s)", command.id, command.title)

    def unregister_command(self, command_id: str) -> None:
        """Unregister a command by ID."""
        if command_id in self._commands:
            del self._commands[command_id]
            logger.debug("Unregistered command ID '%s'", command_id)

    def get_command(self, command_id: str) -> Optional[Command]:
        """Retrieve a registered command by ID."""
        return self._commands.get(command_id)

    def list_commands(self, category: Optional[str] = None) -> List[Command]:
        """List registered commands, optionally filtered by category."""
        if category is None:
            return list(self._commands.values())
        return [cmd for cmd in self._commands.values() if cmd.category.lower() == category.lower()]

    def execute_command(self, command_id: str, *args: Any, **kwargs: Any) -> Any:
        """
        Execute a registered command by ID.
        
        Args:
            command_id: Command ID to execute.
            *args: Positional arguments for command handler.
            **kwargs: Keyword arguments for command handler.
            
        Returns:
            Result returned by the command handler.
        """
        cmd = self.get_command(command_id)
        if cmd is None:
            raise KeyError(f"Command not registered: '{command_id}'")
        if not cmd.enabled:
            logger.warning("Attempted to execute disabled command '%s'", command_id)
            return None

        logger.info("Executing command '%s' (%s)", cmd.id, cmd.title)
        result = None
        if cmd.handler is not None:
            result = cmd.handler(*args, **kwargs)

        self._undo_stack.append(command_id)
        self._redo_stack.clear()

        if self._event_bus is not None:
            self._event_bus.publish(
                Event(
                    topic="command.executed",
                    payload={"command_id": command_id, "title": cmd.title, "result": str(result)},
                    sender="CommandRegistry",
                )
            )

        return result

    def undo(self) -> bool:
        """
        Placeholder for global Undo action.
        """
        if not self._undo_stack:
            logger.info("Undo stack empty.")
            return False
        last_cmd = self._undo_stack.pop()
        self._redo_stack.append(last_cmd)
        logger.info("Undo executed for command '%s' (Placeholder)", last_cmd)

        if self._event_bus is not None:
            self._event_bus.publish(
                Event(
                    topic="command.undo",
                    payload={"command_id": last_cmd},
                    sender="CommandRegistry",
                )
            )
        return True

    def redo(self) -> bool:
        """
        Placeholder for global Redo action.
        """
        if not self._redo_stack:
            logger.info("Redo stack empty.")
            return False
        cmd = self._redo_stack.pop()
        self._undo_stack.append(cmd)
        logger.info("Redo executed for command '%s' (Placeholder)", cmd)

        if self._event_bus is not None:
            self._event_bus.publish(
                Event(
                    topic="command.redo",
                    payload={"command_id": cmd},
                    sender="CommandRegistry",
                )
            )
        return True
