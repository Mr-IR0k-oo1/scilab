def test_create_get_delete_project(client):
    # 1. Create project
    payload = {
        "name": "Scilab GUI Demo Project",
        "description": "Engineering project for GUI design",
    }
    create_res = client.post("/api/v1/projects", json=payload)
    assert create_res.status_code == 201
    project = create_res.json()
    project_id = project["id"]
    assert project["name"] == payload["name"]
    assert project["status"] == "active"
    assert "path" in project

    # 2. Get project by ID
    get_res = client.get(f"/api/v1/projects/{project_id}")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == project_id

    # 3. Delete project
    del_res = client.delete(f"/api/v1/projects/{project_id}")
    assert del_res.status_code == 204

    # 4. Get deleted project should return 404 with structured error
    not_found_res = client.get(f"/api/v1/projects/{project_id}")
    assert not_found_res.status_code == 404
    error_data = not_found_res.json()
    assert "error" in error_data
    assert error_data["error"]["code"] == "PROJECT_NOT_FOUND"


def test_invalid_project_creation(client):
    # Missing required field 'name'
    res = client.post("/api/v1/projects", json={"description": "No name project"})
    assert res.status_code == 422
