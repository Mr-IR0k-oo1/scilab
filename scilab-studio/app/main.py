"""
Main Entry Point for Scilab Studio.

Executes bootstrap sequence, launches PySide6 desktop application, displays
MainWindow shell, and enters Qt event loop.
"""

import os
from pathlib import Path
import sys

# Ensure repository root is on sys.path for direct script executions
REPO_ROOT = Path(__file__).parent.parent.resolve()
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from app.bootstrap import Bootstrap
from app.application import ScilabStudioApplication
from ui.main_window import MainWindow


def main() -> int:
    """Main execution function."""
    # Step 1: Bootstrap core services
    runtime_context = Bootstrap.setup()

    # Step 2: Initialize PySide6 Qt Application
    app = ScilabStudioApplication(sys.argv, runtime_context)

    # Step 3: Instantiate and show MainWindow
    main_window = MainWindow(runtime_context)
    main_window.show()

    # Step 4: Enter Qt Event Loop
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
