from abc import ABC
from typing import Optional
from app.sdk.context import PluginContext


class Plugin(ABC):
    def __init__(self):
        self.context: Optional[PluginContext] = None

    def initialize(self, context: PluginContext) -> None:
        self.context = context

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def dispose(self) -> None:
        pass
