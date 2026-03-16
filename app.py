from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='static')
CORS(app)

# ── In-memory data store ──────────────────────────────────────────────────────
tasks = [
    {
        "id": 1,
        "title": "Complete Data Structures Assignment",
        "description": "Solve linked list problems from chapter 4.",
        "due_date": "2026-03-20",
        "priority": "High",
        "status": "pending"
    },
    {
        "id": 2,
        "title": "Prepare for DBMS Lab",
        "description": "Revise SQL queries and normalization concepts.",
        "due_date": "2026-03-18",
        "priority": "Medium",
        "status": "pending"
    },
    {
        "id": 3,
        "title": "Submit Mini Project Report",
        "description": "Write the introduction and methodology sections.",
        "due_date": "2026-03-25",
        "priority": "High",
        "status": "pending"
    },
    {
        "id": 4,
        "title": "Read Operating Systems Chapter 5",
        "description": "Topics: process scheduling and deadlocks.",
        "due_date": "2026-03-19",
        "priority": "Low",
        "status": "completed"
    }
]

next_id = 5

# ── Serve frontend ────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

# ── POST /api/login ───────────────────────────────────────────────────────────
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if data.get('username') == 'student' and data.get('password') == 'pass123':
        return jsonify({"success": True, "username": data['username']})
    return jsonify({"success": False, "message": "Invalid username or password"}), 401

# ── GET /api/tasks ────────────────────────────────────────────────────────────
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    total = len(tasks)
    completed = sum(1 for t in tasks if t['status'] == 'completed')
    pending = total - completed
    return jsonify({
        "tasks": tasks,
        "summary": {
            "total": total,
            "completed": completed,
            "pending": pending
        }
    })

# ── POST /api/tasks ───────────────────────────────────────────────────────────
@app.route('/api/tasks', methods=['POST'])
def add_task():
    global next_id
    data = request.get_json()
    if not data.get('title'):
        return jsonify({"success": False, "message": "Title is required"}), 400
    new_task = {
        "id": next_id,
        "title": data.get('title'),
        "description": data.get('description', ''),
        "due_date": data.get('due_date', ''),
        "priority": data.get('priority', 'Medium'),
        "status": "pending"
    }
    tasks.append(new_task)
    next_id += 1
    return jsonify({"success": True, "task": new_task}), 201

# ── POST /api/tasks/<id>/complete ─────────────────────────────────────────────
@app.route('/api/tasks/<int:task_id>/complete', methods=['POST'])
def complete_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = 'completed'
            return jsonify({"success": True, "task": task})
    return jsonify({"success": False, "message": "Task not found"}), 404

# ── DELETE /api/tasks/<id> ────────────────────────────────────────────────────
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    original_count = len(tasks)
    tasks = [t for t in tasks if t['id'] != task_id]
    if len(tasks) < original_count:
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Task not found"}), 404

# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
