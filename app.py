from flask import Flask, request, jsonify
from models.task import Task

app = Flask(__name__)

# Banco de dados em memória
tasks = []
task_id_control = 1


@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_control
    data = request.get_json()

    if not data or 'title' not in data:
        return jsonify({"error": "O campo 'title' é obrigatório"}), 400

    new_task = Task(
        id=task_id_control,
        title=data['title'],
        description=data.get('description', ''),
    )
    task_id_control += 1
    tasks.append(new_task)

    return jsonify({
        "message": "Tarefa criada com sucesso",
        "task": new_task.to_dict()
    }), 201


@app.route('/tasks', methods=['GET'])
def get_tasks():
    task_list = [task.to_dict() for task in tasks]
    return jsonify({
        "tasks": task_list,
        "total": len(task_list)
    })


@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = next((task for task in tasks if task.id == id), None)
    if task:
        return jsonify(task.to_dict())
    return jsonify({"error": "Tarefa não encontrada"}), 404


@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Dados inválidos"}), 400

    task = next((task for task in tasks if task.id == id), None)
    if not task:
        return jsonify({"error": "Tarefa não encontrada"}), 404

    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    if 'completed' in data:
        task.completed = bool(data['completed'])

    return jsonify({
        "message": "Tarefa atualizada com sucesso",
        "task": task.to_dict()
    })


@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    global tasks
    task = next((task for task in tasks if task.id == id), None)
    if not task:
        return jsonify({"error": "Tarefa não encontrada"}), 404

    tasks = [t for t in tasks if t.id != id]
    return jsonify({"message": "Tarefa removida com sucesso"}), 200


@app.route('/')
def root():
    return 'Application is running!'


if __name__ == '__main__':
    app.run(debug=True)
