import logging
from typing import Any, Callable, Dict, List, Optional


class PluginLoggerProxy:
    def __init__(self, plugin_id: str):
        self._logger = logging.getLogger(f"plugin.{plugin_id}")

    def info(self, msg: str):
        self._logger.info(msg)

    def warning(self, msg: str):
        self._logger.warning(msg)

    def error(self, msg: str):
        self._logger.error(msg)

    def debug(self, msg: str):
        self._logger.debug(msg)


class PluginContext:
    def __init__(self, plugin_id: str, app_config: Optional[Dict[str, Any]] = None):
        self.plugin_id = plugin_id
        self.logger = PluginLoggerProxy(plugin_id)
        self.configuration = app_config or {}
        self._subscriptions: Dict[str, List[Callable]] = {}

    def subscribe_event(self, event_type: str, handler: Callable[[Dict[str, Any]], None]) -> None:
        if event_type not in self._subscriptions:
            self._subscriptions[event_type] = []
        self._subscriptions[event_type].append(handler)

    def publish_event(self, event_type: str, data: Dict[str, Any]) -> None:
        handlers = self._subscriptions.get(event_type, [])
        for handler in handlers:
            try:
                handler(data)
            except Exception as e:
                self.logger.error(f"Error executing event handler for '{event_type}': {e}")
