"""
Logging service for Scilab Studio core foundation.

Provides structured logging across standard output, log files, and an EventBus bridge.
Log events are published to 'logger.entry' so the UI Console dock can stream
real-time system and runtime logs.
"""

from dataclasses import dataclass, field
import logging
import os
from pathlib import Path
import sys
import time
from typing import Optional

from .service_registry import IService
from .event_bus import Event, EventBus

logger = logging.getLogger("scilab_studio")


@dataclass
class LogEntry:
    """Log record DTO for UI streaming."""
    level: str
    message: str
    logger_name: str
    timestamp: float = field(default_factory=time.time)


class EventBusLogHandler(logging.Handler):
    """Custom Logging Handler broadcasting log entries onto EventBus."""

    def __init__(self, event_bus: Optional[EventBus] = None) -> None:
        super().__init__()
        self.event_bus = event_bus
        self._emitting = False

    def emit(self, record: logging.LogRecord) -> None:
        if self.event_bus is None or self._emitting:
            return
        if record.name.startswith("core.event_bus"):
            return
        try:
            self._emitting = True
            msg = self.format(record)
            entry = LogEntry(
                level=record.levelname,
                message=msg,
                logger_name=record.name,
                timestamp=record.created,
            )
            self.event_bus.publish(
                Event(
                    topic="logger.entry",
                    payload={"level": entry.level, "message": entry.message, "logger_name": entry.logger_name, "timestamp": entry.timestamp},
                    sender="AppLogger",
                ),
                async_gui=True,
            )
        finally:
            self._emitting = False



class AppLogger(IService):
    """
    Central logging service managing console, file, and EventBus logging targets.
    """

    def __init__(self, log_dir: Optional[str] = None, event_bus: Optional[EventBus] = None) -> None:
        if log_dir is None:
            log_dir = str(Path.home() / ".scilab_studio" / "logs")
        self._log_dir = Path(log_dir)
        self._event_bus = event_bus
        self._bus_handler: Optional[EventBusLogHandler] = None
        self._file_handler: Optional[logging.FileHandler] = None
        self._console_handler: Optional[logging.StreamHandler] = None

    def set_event_bus(self, event_bus: EventBus) -> None:
        """Inject or update EventBus instance."""
        self._event_bus = event_bus
        if self._bus_handler is not None:
            self._bus_handler.event_bus = event_bus

    def initialize(self) -> None:
        """Create log directories and configure logging handlers."""
        self._log_dir.mkdir(parents=True, exist_ok=True)
        log_file = self._log_dir / "scilab_studio.log"

        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)

        # Console Handler
        self._console_handler = logging.StreamHandler(sys.stdout)
        self._console_handler.setLevel(logging.INFO)
        self._console_handler.setFormatter(formatter)
        root_logger.addHandler(self._console_handler)

        # File Handler
        self._file_handler = logging.FileHandler(str(log_file), encoding="utf-8")
        self._file_handler.setLevel(logging.DEBUG)
        self._file_handler.setFormatter(formatter)
        root_logger.addHandler(self._file_handler)

        # EventBus Handler
        self._bus_handler = EventBusLogHandler(self._event_bus)
        self._bus_handler.setLevel(logging.INFO)
        self._bus_handler.setFormatter(formatter)
        root_logger.addHandler(self._bus_handler)

        logger.info("Logging service initialized. Log file: %s", log_file)

    def start(self) -> None:
        """Activate logging service."""
        logger.info("AppLogger started.")

    def stop(self) -> None:
        """Flush log handlers."""
        logger.info("AppLogger stopping. Flushing handlers.")
        if self._file_handler:
            self._file_handler.flush()
        if self._console_handler:
            self._console_handler.flush()

    def dispose(self) -> None:
        """Remove logging handlers."""
        root_logger = logging.getLogger()
        if self._console_handler:
            root_logger.removeHandler(self._console_handler)
        if self._file_handler:
            root_logger.removeHandler(self._file_handler)
        if self._bus_handler:
            root_logger.removeHandler(self._bus_handler)
        logger.debug("AppLogger disposed.")
