def test_create_and_list_workspace(client):
    # Initial list should be valid
    res = client.get("/api/v1/workspaces")
    assert res.status_code == 200
    assert "workspaces" in res.json()

    # Create workspace
    payload = {
        "name": "Test Engineering Workspace",
        "description": "Workspace for Pytest testing",
        "path": "/tmp/test_workspace"
    }
    create_res = client.post("/api/v1/workspaces", json=payload)
    assert create_res.status_code == 201
    created_data = create_res.json()
    assert created_data["name"] == payload["name"]
    assert "id" in created_data

    # List again and verify created workspace is included
    list_res = client.get("/api/v1/workspaces")
    assert list_res.status_code == 200
    workspaces = list_res.json()["workspaces"]
    assert any(w["id"] == created_data["id"] for w in workspaces)
