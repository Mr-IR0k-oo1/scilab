"""
Unit tests for CommandRegistry service.
"""

import unittest
from core.event_bus import EventBus
from core.command import Command, CommandRegistry


class TestCommandRegistry(unittest.TestCase):

    def test_command_registration_and_execution(self):
        bus = EventBus()
        bus.initialize()
        bus.start()

        cmd_reg = CommandRegistry(event_bus=bus)
        cmd_reg.initialize()
        cmd_reg.start()

        executed = []

        def handler(a, b):
            executed.append(a + b)
            return a + b

        cmd = Command(
            id="math.add",
            title="Add Numbers",
            handler=handler,
        )

        cmd_reg.register_command(cmd)
        self.assertIsNotNone(cmd_reg.get_command("math.add"))

        res = cmd_reg.execute_command("math.add", 10, 20)
        self.assertEqual(res, 30)
        self.assertEqual(executed, [30])

        # Test Undo & Redo
        self.assertTrue(cmd_reg.undo())
        self.assertTrue(cmd_reg.redo())

        cmd_reg.stop()
        cmd_reg.dispose()
        bus.stop()
        bus.dispose()


if __name__ == "__main__":
    unittest.main()
