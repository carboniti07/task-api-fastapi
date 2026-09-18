def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Task API funcionando"}


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_tasks_starts_empty(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == {"tasks": []}


def test_create_task(client):
    response = client.post(
        "/tasks",
        json={"title": "Estudar Docker", "completed": False},
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Estudar Docker"
    assert data["completed"] is False
    assert data["priority"] == "medium"
    assert isinstance(data["id"], int)


def test_create_task_trims_title(client):
    response = client.post(
        "/tasks",
        json={"title": "  Estudar Python  ", "completed": False},
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Estudar Python"


def test_reject_empty_title(client):
    response = client.post(
        "/tasks",
        json={"title": "   ", "completed": False},
    )

    assert response.status_code == 422


def test_create_and_get_task(client):
    created = client.post(
        "/tasks",
        json={"title": "Estudar Makefile", "completed": False},
    ).json()

    response = client.get(f"/tasks/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created


def test_get_task_not_found(client):
    response = client.get("/tasks/9999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Tarefa não encontrada"}


def test_update_task(client):
    created = client.post(
        "/tasks",
        json={
            "title": "Estudar FastAPI",
            "completed": False,
            "priority": "medium",
        },
    ).json()

    response = client.put(
        f"/tasks/{created['id']}",
        json={
            "title": "Estudar FastAPI avançado",
            "completed": True,
            "priority": "high",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == created["id"]
    assert data["title"] == "Estudar FastAPI avançado"
    assert data["completed"] is True
    assert data["priority"] == "high"


def test_delete_task(client):
    created = client.post(
        "/tasks",
        json={"title": "Tarefa para excluir", "completed": False},
    ).json()

    delete_response = client.delete(f"/tasks/{created['id']}")

    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "Tarefa removida com sucesso"}

    get_response = client.get(f"/tasks/{created['id']}")

    assert get_response.status_code == 404


def test_create_task_with_priority(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Estudar CI",
            "completed": False,
            "priority": "high",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Estudar CI"
    assert data["completed"] is False
    assert data["priority"] == "high"


def test_create_task_uses_medium_priority_by_default(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Estudar Docker",
            "completed": False,
        },
    )

    assert response.status_code == 201
    assert response.json()["priority"] == "medium"


def test_reject_invalid_priority(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Estudar FastAPI",
            "completed": False,
            "priority": "urgent",
        },
    )

    assert response.status_code == 422


def test_filter_tasks_by_completed(client):
    client.post(
        "/tasks",
        json={
            "title": "Tarefa concluída",
            "completed": True,
            "priority": "medium",
        },
    )

    client.post(
        "/tasks",
        json={
            "title": "Tarefa pendente",
            "completed": False,
            "priority": "medium",
        },
    )

    response = client.get("/tasks?completed=true")

    assert response.status_code == 200

    data = response.json()["tasks"]

    assert len(data) == 1
    assert data[0]["title"] == "Tarefa concluída"
    assert data[0]["completed"] is True


def test_filter_tasks_by_priority(client):
    client.post(
        "/tasks",
        json={
            "title": "Tarefa alta",
            "completed": False,
            "priority": "high",
        },
    )

    client.post(
        "/tasks",
        json={
            "title": "Tarefa baixa",
            "completed": False,
            "priority": "low",
        },
    )

    response = client.get("/tasks?priority=high")

    assert response.status_code == 200

    data = response.json()["tasks"]

    assert len(data) == 1
    assert data[0]["title"] == "Tarefa alta"
    assert data[0]["priority"] == "high"


def test_filter_tasks_by_completed_and_priority(client):
    client.post(
        "/tasks",
        json={
            "title": "Alta concluída",
            "completed": True,
            "priority": "high",
        },
    )

    client.post(
        "/tasks",
        json={
            "title": "Alta pendente",
            "completed": False,
            "priority": "high",
        },
    )

    response = client.get("/tasks?completed=true&priority=high")

    assert response.status_code == 200

    data = response.json()["tasks"]

    assert len(data) == 1
    assert data[0]["title"] == "Alta concluída"

def test_list_tasks_with_limit(client):
    for index in range(5):
        client.post(
            "/tasks",
            json={
                "title": f"Tarefa {index + 1}",
                "completed": False,
                "priority": "medium",
            },
        )

    response = client.get("/tasks?limit=2")

    assert response.status_code == 200

    tasks = response.json()["tasks"]

    assert len(tasks) == 2
    assert tasks[0]["title"] == "Tarefa 1"
    assert tasks[1]["title"] == "Tarefa 2"


def test_list_tasks_with_offset(client):
    for index in range(5):
        client.post(
            "/tasks",
            json={
                "title": f"Tarefa {index + 1}",
                "completed": False,
                "priority": "medium",
            },
        )

    response = client.get("/tasks?limit=2&offset=2")

    assert response.status_code == 200

    tasks = response.json()["tasks"]

    assert len(tasks) == 2
    assert tasks[0]["title"] == "Tarefa 3"
    assert tasks[1]["title"] == "Tarefa 4"


def test_list_tasks_filters_and_pagination(client):
    client.post(
        "/tasks",
        json={
            "title": "Alta 1",
            "completed": False,
            "priority": "high",
        },
    )

    client.post(
        "/tasks",
        json={
            "title": "Baixa",
            "completed": False,
            "priority": "low",
        },
    )

    client.post(
        "/tasks",
        json={
            "title": "Alta 2",
            "completed": False,
            "priority": "high",
        },
    )

    response = client.get("/tasks?priority=high&limit=1&offset=1")

    assert response.status_code == 200

    tasks = response.json()["tasks"]

    assert len(tasks) == 1
    assert tasks[0]["title"] == "Alta 2"
