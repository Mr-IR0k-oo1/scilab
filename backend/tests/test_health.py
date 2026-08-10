def test_health_check(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "app_name" in data
    assert "version" in data


def test_system_info(client):
    response = client.get("/api/v1/system/info")
    assert response.status_code == 200
    data = response.json()
    assert "python_version" in data
    assert "platform" in data
    assert data["database_status"] == "connected"
