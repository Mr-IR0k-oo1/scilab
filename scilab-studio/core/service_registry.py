"""
Service Registry module for Scilab Studio core foundation.

Implements the Dependency Injection container and service lifecycle contract.
Every core platform service and feature module MUST implement the IService protocol.

Architectural Rationale:
-----------------------
Direct instantiation or singleton patterns create hidden dependencies and tight
coupling between components. By registering services in a central ServiceRegistry,
components request dependencies via protocols/interfaces, making testing, mocking,
and module isolation straightforward.
"""

from enum import Enum, auto
import logging
import threading
from typing import Any, Dict, List, Optional, Protocol, Type, TypeVar, runtime_checkable

logger = logging.getLogger(__name__)


class ServiceState(Enum):
    """Lifecycle states of a registered service."""
    UNINITIALIZED = auto()
    INITIALIZED = auto()
    STARTED = auto()
    STOPPED = auto()
    DISPOSED = auto()


@runtime_checkable
class IService(Protocol):
    """
    Unified lifecycle protocol for all Scilab Studio services.
    
    Every core service and platform module must fulfill this contract to participate
    in orderly application startup and shutdown sequences.
    """

    def initialize(self) -> None:
        """Allocate resources, establish internal state, load prerequisites."""
        ...

    def start(self) -> None:
        """Activate background workers, event listeners, or network streams."""
        ...

    def stop(self) -> None:
        """Pause activity, flush buffers, stop background processing."""
        ...

    def dispose(self) -> None:
        """Release underlying system resources, handles, and memory references."""
        ...


T = TypeVar("T")


class ServiceRegistry:
    """
    Thread-safe Service Container for Dependency Injection and Lifecycle Management.
    
    Maintains registered service instances by their concrete class or abstract Protocol type.
    Manages stage transitions across all registered services in order of registration.
    """

    def __init__(self) -> None:
        self._services: Dict[Any, Any] = {}
        self._service_order: List[Any] = []
        self._states: Dict[Any, ServiceState] = {}
        self._lock = threading.RLock()

    def register(self, service: Any, interface: Optional[Type[Any]] = None) -> None:
        """
        Register a service instance under an interface protocol or concrete class type.
        
        Args:
            service: The service instance executing IService protocol.
            interface: Optional interface or protocol type key for dependency resolution.
        """
        with self._lock:
            key = interface if interface is not None else type(service)
            if key in self._services:
                logger.warning("Overwriting existing service registration for %s", key)
            self._services[key] = service
            if key not in self._service_order:
                self._service_order.append(key)
            self._states[key] = ServiceState.UNINITIALIZED
            logger.debug("Registered service: %s as %s", type(service).__name__, key)

    def get(self, interface_or_class: Type[T]) -> T:
        """
        Retrieve a registered service instance by interface or class type.
        
        Args:
            interface_or_class: The protocol or class used during registration.
            
        Returns:
            The registered service instance cast to type T.
            
        Raises:
            KeyError: If no service is registered for the specified type key.
        """
        with self._lock:
            if interface_or_class not in self._services:
                raise KeyError(
                    f"Service not found for type: {interface_or_class.__name__ if hasattr(interface_or_class, '__name__') else interface_or_class}"
                )
            return self._services[interface_or_class]

    def has(self, interface_or_class: Type[Any]) -> bool:
        """Check if a service is registered under the given interface or class type."""
        with self._lock:
            return interface_or_class in self._services

    def unregister(self, interface_or_class: Type[Any]) -> None:
        """Remove a service registration key."""
        with self._lock:
            if interface_or_class in self._services:
                del self._services[interface_or_class]
                if interface_or_class in self._service_order:
                    self._service_order.remove(interface_or_class)
                self._states.pop(interface_or_class, None)
                logger.debug("Unregistered service key: %s", interface_or_class)

    def initialize_all(self) -> None:
        """Invoke initialize() on all registered services in order of registration."""
        with self._lock:
            for key in self._service_order:
                service = self._services[key]
                if self._states[key] == ServiceState.UNINITIALIZED:
                    if isinstance(service, IService):
                        logger.info("Initializing service %s", type(service).__name__)
                        service.initialize()
                    self._states[key] = ServiceState.INITIALIZED

    def start_all(self) -> None:
        """Invoke start() on all registered services in order of registration."""
        with self._lock:
            for key in self._service_order:
                service = self._services[key]
                if self._states[key] in (ServiceState.INITIALIZED, ServiceState.STOPPED):
                    if isinstance(service, IService):
                        logger.info("Starting service %s", type(service).__name__)
                        service.start()
                    self._states[key] = ServiceState.STARTED

    def stop_all(self) -> None:
        """Invoke stop() on all registered services in reverse order of registration."""
        with self._lock:
            for key in reversed(self._service_order):
                service = self._services[key]
                if self._states[key] == ServiceState.STARTED:
                    if isinstance(service, IService):
                        logger.info("Stopping service %s", type(service).__name__)
                        service.stop()
                    self._states[key] = ServiceState.STOPPED

    def dispose_all(self) -> None:
        """Invoke dispose() on all registered services in reverse order of registration."""
        with self._lock:
            for key in reversed(self._service_order):
                service = self._services[key]
                if self._states[key] != ServiceState.DISPOSED:
                    if isinstance(service, IService):
                        logger.info("Disposing service %s", type(service).__name__)
                        service.dispose()
                    self._states[key] = ServiceState.DISPOSED

    def get_state(self, interface_or_class: Type[Any]) -> Optional[ServiceState]:
        """Return the current lifecycle state of a registered service."""
        with self._lock:
            return self._states.get(interface_or_class)
