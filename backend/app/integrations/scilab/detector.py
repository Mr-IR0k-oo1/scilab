import glob
import os
import platform
import shutil
import subprocess
from typing import Optional
from app.integrations.scilab.configuration import scilab_config
from app.integrations.scilab.models import ScilabStatusInfo


class ScilabDetector:
    @staticmethod
    def detect() -> ScilabStatusInfo:
        candidates = []

        # Priority 1: Env var
        env_exe = os.getenv("SCILAB_EXECUTABLE")
        if env_exe:
            candidates.append(env_exe)

        # Priority 2: User configuration
        if scilab_config.executable and scilab_config.executable not in candidates:
            candidates.append(scilab_config.executable)

        # Priority 3: System PATH
        for binary_name in ["scilab-cli", "scilab-adv-cli", "scilab"]:
            found = shutil.which(binary_name)
            if found and found not in candidates:
                candidates.append(found)

        # Priority 4: Platform-specific common locations
        system = platform.system().lower()
        if "windows" in system:
            for pattern in [
                r"C:\Program Files\scilab-*\bin\scilab-cli.exe",
                r"C:\Program Files\scilab-*\bin\scilab-adv-cli.exe",
                r"C:\Program Files (x86)\scilab-*\bin\scilab-cli.exe",
            ]:
                for match in glob.glob(pattern):
                    if match not in candidates:
                        candidates.append(match)
        elif "darwin" in system:  # macOS
            for pattern in [
                "/Applications/Scilab-*.app/Contents/bin/scilab-cli",
                "/Applications/Scilab-*.app/Contents/bin/scilab",
            ]:
                for match in glob.glob(pattern):
                    if match not in candidates:
                        candidates.append(match)
        else:  # Linux / Unix
            for path in ["/usr/bin/scilab-cli", "/usr/local/bin/scilab-cli", "/usr/bin/scilab"]:
                if os.path.exists(path) and path not in candidates:
                    candidates.append(path)

        # Validate candidates
        for candidate in candidates:
            version = ScilabDetector.validate_and_get_version(candidate)
            if version is not None:
                return ScilabStatusInfo(
                    installed=True,
                    executable=candidate,
                    version=version,
                    status="available",
                )

        return ScilabStatusInfo(
            installed=False,
            executable=None,
            version=None,
            status="unavailable",
        )

    @staticmethod
    def validate_and_get_version(executable_path: str) -> Optional[str]:
        if not executable_path or not os.path.exists(executable_path):
            # Check if it's executable via PATH check
            if not shutil.which(executable_path):
                return None

        try:
            # Run `scilab-cli -version` or `scilab-cli -e "disp(getversion()); quit;"`
            res = subprocess.run(
                [executable_path, "-version"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if res.returncode == 0 and res.stdout:
                lines = [l.strip() for l in res.stdout.splitlines() if l.strip()]
                if lines:
                    return lines[0]
            return "7.0.0"  # Default assumed compatible version if binary runs cleanly
        except Exception:
            return None
