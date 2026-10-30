def test_create_task(client):
    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Learn pytest",
            "description": "Write automated tests for ATLAS",
            "priority": "high",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Learn pytest"
    assert data["description"] == "Write automated tests for ATLAS"
    assert data["status"] == "pending"
    assert data["priority"] == "high"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_list_tasks(client):
    client.post(
        "/api/v1/tasks",
        json={"title": "Task one"},
    )

    client.post(
        "/api/v1/tasks",
        json={"title": "Task two"},
    )

    response = client.get("/api/v1/tasks")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_task(client):
    create_response = client.post(
        "/api/v1/tasks",
        json={"title": "Test retrieval"},
    )

    task_id = create_response.json()["id"]

    response = client.get(f"/api/v1/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["title"] == "Test retrieval"


def test_update_task(client):
    create_response = client.post(
        "/api/v1/tasks",
        json={"title": "Original title"},
    )

    task_id = create_response.json()["id"]

    response = client.patch(
        f"/api/v1/tasks/{task_id}",
        json={"status": "completed"},
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Original title"
    assert response.json()["status"] == "completed"


def test_delete_task(client):
    create_response = client.post(
        "/api/v1/tasks",
        json={"title": "Task to delete"},
    )

    task_id = create_response.json()["id"]

    response = client.delete(f"/api/v1/tasks/{task_id}")

    assert response.status_code == 204

    get_response = client.get(f"/api/v1/tasks/{task_id}")

    assert get_response.status_code == 404