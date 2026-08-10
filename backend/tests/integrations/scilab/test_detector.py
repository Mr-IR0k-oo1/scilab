from unittest.mock import patch
from app.integrations.scilab.detector import ScilabDetector
from app.integrations.scilab.models import ScilabStatusInfo


def test_detector_when_not_found():
    with patch("shutil.which", return_value=None), \
         patch("glob.glob", return_value=[]), \
         patch("os.getenv", return_value=None):
        info = ScilabDetector.detect()
        assert isinstance(info, ScilabStatusInfo)
        assert info.installed is False
        assert info.executable is None
        assert info.status == "unavailable"


def test_detector_when_found():
    fake_exe = "/usr/bin/scilab-cli"
    with patch("shutil.which", return_value=fake_exe), \
         patch("app.integrations.scilab.detector.ScilabDetector.validate_and_get_version", return_value="7.0.0"):
        info = ScilabDetector.detect()
        assert info.installed is True
        assert info.executable == fake_exe
        assert info.version == "7.0.0"
        assert info.status == "available"


def test_invalid_executable_validation():
    result = ScilabDetector.validate_and_get_version("/invalid/path/to/nonexistent/scilab")
    assert result is None
