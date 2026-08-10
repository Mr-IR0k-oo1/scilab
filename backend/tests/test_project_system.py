import os
import tempfile
from unittest.mock import AsyncMock, patch
import pytest
from app.integrations.scilab.models import ExecutionResult, ExecutionStatus


def test_project_creation_and_validation(client):
    res = client.post("/api/v1/projects", json={"name": "Solar Analysis Project", "description": "Solar engineering research"})
    assert res.status_code == 201
    p_data = res.json()
    project_id = p_data["id"]

    # Verify project tree
    tree_res = client.get(f"/api/v1/projects/{project_id}/tree")
    assert tree_res.status_code == 200
    tree_nodes = tree_res.json()["tree"]
    node_names = [node["name"] for node in tree_nodes]
    assert "project.json" in node_names
    assert "scripts" in node_names
    assert "datasets" in node_names


def test_project_file_crud_and_security(client):
    p_res = client.post("/api/v1/projects", json={"name": "File Test Project"})
    p_id = p_res.json()["id"]

    # 1. Create file inside scripts/
    c_res = client.post(f"/api/v1/projects/{p_id}/files?relative_path=scripts/test_script.sce", json={"content": "x = 10;\ndisp(x);"})
    assert c_res.status_code == 200

    # 2. Read file
    r_res = client.get(f"/api/v1/projects/{p_id}/files/scripts/test_script.sce")
    assert r_res.status_code == 200
    assert "disp(x)" in r_res.json()["content"]

    # 3. Update file
    u_res = client.put(f"/api/v1/projects/{p_id}/files/scripts/test_script.sce", json={"content": "x = 20;\ndisp(x);"})
    assert u_res.status_code == 200

    # 4. Path traversal attempt blocked
    t_res = client.get(f"/api/v1/projects/{p_id}/files/..%2F..%2Fetc%2Fpasswd")
    assert t_res.status_code in [400, 403, 404]

    # 5. Delete file
    d_res = client.delete(f"/api/v1/projects/{p_id}/files/scripts/test_script.sce")
    assert d_res.status_code == 204


def test_dataset_upload_and_metadata(client):
    p_res = client.post("/api/v1/projects", json={"name": "Dataset Test Project"})
    p_id = p_res.json()["id"]

    csv_content = b"col1,col2,col3\n1,2,3\n4,5,6\n7,8,9\n"
    files = {"file": ("test_data.csv", csv_content, "text/csv")}

    up_res = client.post(f"/api/v1/projects/{p_id}/datasets", files=files)
    assert up_res.status_code == 201
    meta = up_res.json()
    assert meta["filename"] == "test_data.csv"
    assert meta["row_count"] == 4
    assert meta["column_count"] == 3

    list_res = client.get(f"/api/v1/projects/{p_id}/datasets")
    assert list_res.status_code == 200
    assert len(list_res.json()) == 1


def test_experiment_creation_and_execution_history(client):
    p_res = client.post("/api/v1/projects", json={"name": "Experiment Test Project"})
    p_id = p_res.json()["id"]

    # Create experiment
    exp_payload = {
        "name": "Solar Efficiency Analysis",
        "description": "Calculate solar efficiency factor",
        "script_path": "scripts/main.sce"
    }
    e_res = client.post(f"/api/v1/projects/{p_id}/experiments", json=exp_payload)
    assert e_res.status_code == 201
    exp_id = e_res.json()["id"]

    # Mock Scilab runtime execution
    fake_result = ExecutionResult(
        id="exec-run-456",
        command="exec('.../scripts/main.sce', -1);",
        success=True,
        stdout="Solar Efficiency = 88.5%",
        stderr="",
        exit_code=0,
        status=ExecutionStatus.COMPLETED,
        duration_ms=120.0
    )

    with patch("app.services.scilab_service.ScilabService.execute_script", new_callable=AsyncMock, return_value=fake_result):
        run_res = client.post(f"/api/v1/projects/{p_id}/experiments/{exp_id}/run")
        assert run_res.status_code == 200
        run_data = run_res.json()
        assert run_data["execution_id"] == "exec-run-456"
        assert run_data["stdout"] == "Solar Efficiency = 88.5%"

    # Check execution history
    hist_res = client.get(f"/api/v1/projects/{p_id}/executions")
    assert hist_res.status_code == 200
    records = hist_res.json()
    assert len(records) >= 1
    assert records[0]["execution_id"] == "exec-run-456"
