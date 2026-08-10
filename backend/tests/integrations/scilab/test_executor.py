import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from app.integrations.scilab.executor import ScilabExecutor
from app.integrations.scilab.models import ExecutionStatus
from app.integrations.scilab.parser import ScilabOutputParser
from app.integrations.scilab.session import ScilabSession


@pytest.mark.asyncio
async def test_command_execution_success():
    session = MagicMock(spec=ScilabSession)
    session.can_execute.return_value = True
    session.set_executing = AsyncMock()
    session.set_finished_executing = AsyncMock()
    session.process_manager = MagicMock()
    session.process_manager.send = AsyncMock(return_value=True)

    mock_proc = MagicMock()
    mock_stdout = AsyncMock()
    mock_stdout.readline.side_effect = [b"ans =  42.0\n", b"-->\n", b""]
    mock_proc.stdout = mock_stdout
    session.process_manager.process = mock_proc

    res = await ScilabExecutor.execute_command("21 * 2", session, timeout=5.0)

    assert res.success is True
    assert res.status == ExecutionStatus.COMPLETED
    assert "42.0" in res.stdout


@pytest.mark.asyncio
async def test_command_execution_timeout():
    session = MagicMock(spec=ScilabSession)
    session.can_execute.return_value = True
    session.set_executing = AsyncMock()
    session.set_finished_executing = AsyncMock()
    session.process_manager = MagicMock()
    session.process_manager.send = AsyncMock(return_value=True)
    session.process_manager.terminate = AsyncMock()
    session.process_manager.kill = AsyncMock()
    session.process_manager.is_running.return_value = True

    mock_proc = MagicMock()
    mock_stdout = AsyncMock()
    async def infinite_line():
        await asyncio.sleep(10)
        return b""
    mock_stdout.readline = infinite_line
    mock_proc.stdout = mock_stdout
    session.process_manager.process = mock_proc

    res = await ScilabExecutor.execute_command("while %t do end", session, timeout=0.1)

    assert res.success is False
    assert res.status == ExecutionStatus.TIMED_OUT


def test_output_truncation():
    large_stdout = "x" * 2000000
    cleaned, _, truncated = ScilabOutputParser.parse_output(large_stdout, "", max_size=1000)
    assert truncated is True
    assert "TRUNCATED" in cleaned
