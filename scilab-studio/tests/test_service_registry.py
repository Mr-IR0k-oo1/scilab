"""
Unit tests for ServiceRegistry container and lifecycle transitions.
"""

from typing import Protocol
import unittest

from core.service_registry import IService, ServiceRegistry, ServiceState


class ITestService(IService, Protocol):
    def value(self) -> int:
        ...


class DummyService:
    def __init__(self) -> None:
        self.initialized = False
        self.started = False
        self.stopped = False
        self.disposed = False

    def value(self) -> int:
        return 42

    def initialize(self) -> None:
        self.initialized = True

    def start(self) -> None:
        self.started = True

    def stop(self) -> None:
        self.stopped = True

    def dispose(self) -> None:
        self.disposed = True


class TestServiceRegistry(unittest.TestCase):

    def test_service_registration_and_lookup(self):
        registry = ServiceRegistry()
        service = DummyService()

        registry.register(service, interface=ITestService)

        self.assertTrue(registry.has(ITestService))
        resolved = registry.get(ITestService)
        self.assertIs(resolved, service)
        self.assertEqual(resolved.value(), 42)

    def test_service_not_found(self):
        registry = ServiceRegistry()
        with self.assertRaises(KeyError):
            registry.get(ITestService)

    def test_service_lifecycle_transitions(self):
        registry = ServiceRegistry()
        service = DummyService()
        registry.register(service)

        self.assertEqual(registry.get_state(DummyService), ServiceState.UNINITIALIZED)

        registry.initialize_all()
        self.assertTrue(service.initialized)
        self.assertEqual(registry.get_state(DummyService), ServiceState.INITIALIZED)

        registry.start_all()
        self.assertTrue(service.started)
        self.assertEqual(registry.get_state(DummyService), ServiceState.STARTED)

        registry.stop_all()
        self.assertTrue(service.stopped)
        self.assertEqual(registry.get_state(DummyService), ServiceState.STOPPED)

        registry.dispose_all()
        self.assertTrue(service.disposed)
        self.assertEqual(registry.get_state(DummyService), ServiceState.DISPOSED)


if __name__ == "__main__":
    unittest.main()
