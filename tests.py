import pytest
import requests

BASE_URL = 'http://127.0.0.1:5000'


def test_create_task():
    new_task = {
        "title": "Test Task",
        "description": "This is a test task"
    }

    response = requests.post(f'{BASE_URL}/tasks', json=new_task)

    assert response.status_code == 201, f"Status esperado 201, recebido {response.status_code}"

    data = response.json()

    assert 'task' in data, "Resposta não contém o campo 'task'"
    task = data['task']

    assert task['id'] == 1, f"ID esperado 1, recebido {task['id']}"
    assert task['title'] == new_task['title']
    assert task['description'] == new_task['description']
    assert task['completed'] is False

