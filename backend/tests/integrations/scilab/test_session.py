from unittest.mock import AsyncMock, patch
import pytest
from app.integrations.scilab.exceptions import ScilabSessionStateError
from app.integrations.scilab.models import SessionState
from app.integrations.scilab.session import ScilabSession


@pytest.mark.asyncio
async def test_session_state_transitions():
    session = ScilabSession(executable="scilab-cli")
    assert session.state == SessionState.CREATED
    assert session.can_execute() is False

    with patch.object(session.process_manager, "start", new_callable=AsyncMock, return_value=True), \
         patch.object(session.process_manager, "is_running", return_value=True):
        await session.start()
        assert session.state == SessionState.RUNNING
        assert session.can_execute() is True

        await session.set_executing()
        assert session.state == SessionState.EXECUTING

        await session.set_finished_executing(success=True)
        assert session.state == SessionState.RUNNING

        with patch.object(session.process_manager, "stop", new_callable=AsyncMock):
            await session.stop()
            assert session.state == SessionState.STOPPED


@pytest.mark.asyncio
async def test_invalid_session_execution():
    session = ScilabSession(executable="scilab-cli")
    assert session.state == SessionState.CREATED

    with pytest.raises(ScilabSessionStateError):
        await session.set_executing()
