import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from app.integrations.scilab.process_manager import ProcessManager


@pytest.mark.asyncio
async def test_process_manager_lifecycle():
    pm = ProcessManager(executable="scilab-cli", working_dir="/tmp")
    assert pm.is_running() is False

    mock_proc = AsyncMock()
    mock_proc.returncode = None
    mock_proc.stdin = MagicMock()
    mock_proc.stdin.write = MagicMock()
    mock_proc.stdin.drain = AsyncMock()

    with patch("asyncio.create_subprocess_exec", return_value=mock_proc):
        success = await pm.start()
        assert success is True
        assert pm.is_running() is True

        # Send command
        sent = await pm.send("disp(1)")
        assert sent is True
        mock_proc.stdin.write.assert_called_once()

        # Stop process
        mock_proc.wait = AsyncMock(return_value=0)
        await pm.stop()
        assert pm.is_running() is False


@pytest.mark.asyncio
async def test_process_manager_start_failure():
    pm = ProcessManager(executable="/invalid/scilab")
    with patch("asyncio.create_subprocess_exec", side_effect=OSError("File not found")):
        success = await pm.start()
        assert success is False
        assert pm.is_running() is False
