import pytest
import requests

BASE_URL = 'http://127.0.0.1:5000'


created_task_ids = []

def test_create_task():
    """Testa a criação de uma nova tarefa"""
    new_task = {
        "title": "Test Task",
        "description": "This is a test task"
    }
    
    response = requests.post(f'{BASE_URL}/tasks', json=new_task)
    assert response.status_code == 201, f"Status esperado 201, recebido {response.status_code}"
    
    data = response.json()
    assert 'task' in data, "Resposta não contém o campo 'task'"
    
    task = data['task']
    assert 'id' in task, "Task não contém o campo 'id'"
    assert task['title'] == new_task['title']
    assert task['description'] == new_task['description']
    assert task['completed'] is False
    

    created_task_ids.append(task['id'])

def test_get_tasks():
    """Testa a listagem de todas as tarefas"""
    response = requests.get(f'{BASE_URL}/tasks')
    assert response.status_code == 200, f"Status esperado 200, recebido {response.status_code}"
    
    data = response.json()
    assert 'tasks' in data, "Resposta não contém o campo 'tasks'"
    assert 'total' in data, "Resposta não contém o campo 'total'"
    assert data['total'] == len(data['tasks']), "'total' deve ser igual ao tamanho da lista 'tasks'"

def test_get_task():
    """Testa a busca de uma tarefa específica"""

    new_task = {
        "title": "Task for Get Test",
        "description": "Task created for testing get endpoint"
    }
    
    create_response = requests.post(f'{BASE_URL}/tasks', json=new_task)
    assert create_response.status_code == 201
    
    task_id = create_response.json()['task']['id']
    created_task_ids.append(task_id)
    

    response = requests.get(f'{BASE_URL}/tasks/{task_id}')
    assert response.status_code == 200, f"Status esperado 200, recebido {response.status_code}"
    
    data = response.json()
    assert 'id' in data, "Resposta não contém o campo 'id'"
    assert data['id'] == task_id, f"ID esperado {task_id}, recebido {data['id']}"
    assert 'title' in data, "Resposta não contém o campo 'title'"
    assert 'description' in data, "Resposta não contém o campo 'description'"
    assert 'completed' in data, "Resposta não contém o campo 'completed'"

def test_get_nonexistent_task():
    """Testa a busca de uma tarefa que não existe"""
    response = requests.get(f'{BASE_URL}/tasks/99999')
    assert response.status_code == 404, f"Status esperado 404, recebido {response.status_code}"

def test_update_task():
    """Testa a atualização de uma tarefa"""

    new_task = {
        "title": "Task to Update",
        "description": "This task will be updated"
    }
    
    create_response = requests.post(f'{BASE_URL}/tasks', json=new_task)
    assert create_response.status_code == 201
    
    task_id = create_response.json()['task']['id']
    created_task_ids.append(task_id)
    

    payload = {
        "completed": True,
        "description": "Nova descrição",
        "title": "Título atualizado"
    }
    
    response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=payload)
    assert response.status_code == 200, f"Status esperado 200, recebido {response.status_code}"
    
    response_json = response.json()
    assert "message" in response_json, "Resposta não contém o campo 'message'"
    

    get_response = requests.get(f"{BASE_URL}/tasks/{task_id}")
    assert get_response.status_code == 200
    
    updated_task = get_response.json()
    assert updated_task["title"] == payload["title"]
    assert updated_task["description"] == payload["description"]
    assert updated_task["completed"] == payload["completed"]

def test_update_nonexistent_task():
    """Testa a atualização de uma tarefa que não existe"""
    payload = {
        "title": "Updated Title",
        "description": "Updated Description"
    }
    
    response = requests.put(f"{BASE_URL}/tasks/99999", json=payload)
    assert response.status_code == 404, f"Status esperado 404, recebido {response.status_code}"

def test_delete_task():
    """Testa a remoção de uma tarefa"""
    new_task = {
        "title": "Task to Delete",
        "description": "This task will be deleted"
    }
    
    create_response = requests.post(f'{BASE_URL}/tasks', json=new_task)
    assert create_response.status_code == 201
    
    task_id = create_response.json()['task']['id']
    

    response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
    assert response.status_code == 200, f"Status esperado 200, recebido {response.status_code}"
    

    get_response = requests.get(f"{BASE_URL}/tasks/{task_id}")
    assert get_response.status_code == 404, f"Status esperado 404, recebido {get_response.status_code}"

def test_delete_nonexistent_task():
    """Testa a remoção de uma tarefa que não existe"""
    response = requests.delete(f"{BASE_URL}/tasks/99999")
    assert response.status_code == 404, f"Status esperado 404, recebido {response.status_code}"

def test_create_task_without_title():
    """Testa a criação de tarefa sem título (deve falhar)"""
    new_task = {
        "description": "Task without title"
    }
    
    response = requests.post(f'{BASE_URL}/tasks', json=new_task)
    assert response.status_code == 400, f"Status esperado 400, recebido {response.status_code}"

def test_create_task_with_empty_payload():
    """Testa a criação de tarefa com payload vazio (deve falhar)"""
    response = requests.post(f'{BASE_URL}/tasks', json={})
    assert response.status_code == 400, f"Status esperado 400, recebido {response.status_code}"


def test_cleanup():
    """Remove todas as tarefas criadas durante os testes"""
    for task_id in created_task_ids:
        try:
            requests.delete(f"{BASE_URL}/tasks/{task_id}")
        except:
            pass 