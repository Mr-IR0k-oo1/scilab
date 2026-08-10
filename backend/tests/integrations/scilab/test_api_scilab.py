from unittest.mock import AsyncMock, patch
from app.integrations.scilab.models import ExecutionResult, ExecutionStatus, ScilabStatusInfo


def test_api_scilab_status(client):
    fake_info = ScilabStatusInfo(installed=True, executable="/usr/bin/scilab-cli", version="7.0.0", status="available")
    with patch("app.services.scilab_service.ScilabService.get_detector_info", return_value=fake_info):
        res = client.get("/api/v1/scilab/status")
        assert res.status_code == 200
        data = res.json()
        assert data["installed"] is True
        assert data["executable"] == "/usr/bin/scilab-cli"
        assert data["version"] == "7.0.0"


def test_api_scilab_execute(client):
    fake_result = ExecutionResult(
        id="test-exec-123",
        command="disp('Hello')",
        success=True,
        stdout="Hello",
        stderr="",
        exit_code=0,
        status=ExecutionStatus.COMPLETED,
    )
    with patch("app.services.scilab_service.ScilabService.execute_command", new_callable=AsyncMock, return_value=fake_result):
        res = client.post("/api/v1/scilab/execute", json={"command": "disp('Hello')"})
        assert res.status_code == 200
        data = res.json()
        assert data["id"] == "test-exec-123"
        assert data["success"] is True
        assert data["stdout"] == "Hello"


def test_api_scilab_start_and_stop(client):
    fake_info = ScilabStatusInfo(installed=True, executable="/usr/bin/scilab-cli", version="7.0.0", status="running")
    with patch("app.services.scilab_service.ScilabService.start_session", new_callable=AsyncMock, return_value=fake_info):
        res = client.post("/api/v1/scilab/start")
        assert res.status_code == 200

    with patch("app.services.scilab_service.ScilabService.stop_session", new_callable=AsyncMock):
        res = client.post("/api/v1/scilab/stop")
        assert res.status_code == 200
        assert res.json()["status"] == "stopped"
