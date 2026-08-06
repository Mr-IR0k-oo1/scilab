"""
Scilab Studio Modules Package.

Provides abstract base class definitions for modular extensions.
Enforces modular design principles: zero direct cross-module coupling,
dependency resolution exclusively via ServiceRegistry, and communication
exclusively via EventBus.
"""

from .base_module import BaseModule

__all__ = ["BaseModule"]
