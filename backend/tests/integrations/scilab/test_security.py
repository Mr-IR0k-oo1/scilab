import os
import pytest
from app.integrations.scilab.exceptions import ScilabSecurityException
from app.integrations.scilab.executor import ScilabExecutor


def test_path_traversal_blocked():
    with pytest.raises(ScilabSecurityException) as exc_info:
        ScilabExecutor.validate_script_path("../../../etc/passwd")
    assert "Path traversal" in str(exc_info.value) or "prohibited" in str(exc_info.value)


def test_invalid_extension_blocked(tmp_path):
    invalid_file = tmp_path / "script.py"
    invalid_file.write_text("print('hello')")
    with pytest.raises(ScilabSecurityException) as exc_info:
        ScilabExecutor.validate_script_path(str(invalid_file))
    assert "extension" in str(exc_info.value)


def test_nonexistent_script_blocked():
    with pytest.raises(ScilabSecurityException) as exc_info:
        ScilabExecutor.validate_script_path("/tmp/nonexistent_script_xyz.sci")
    assert "file does not exist" in str(exc_info.value)


def test_outside_allowed_workspace_boundary_blocked(tmp_path):
    allowed_dir = tmp_path / "workspace"
    allowed_dir.mkdir()
    script_file = tmp_path / "outside.sci"
    script_file.write_text("disp(1);")

    with pytest.raises(ScilabSecurityException) as exc_info:
        ScilabExecutor.validate_script_path(str(script_file), allowed_base_dirs=[str(allowed_dir)])
    assert "forbidden outside approved workspace" in str(exc_info.value)
