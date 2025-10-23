from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

# In-memory storage (replace with DB later)
tasks = []

@tasks_bp.route("/upload", methods=["POST"])
def upload_task():
    if 'file' not in request.files and 'description' not in request.form:
        return jsonify({"error": "No file or description provided"}), 400

    file = request.files.get('file')
    description = request.form.get('description', '')

    filename = None
    if file:
        filename = secure_filename(file.filename)
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(upload_path)

    task = {"id": len(tasks)+1, "filename": filename, "description": description}
    tasks.append(task)

    return jsonify({"message": "Task uploaded successfully", "task": task}), 201


@tasks_bp.route("/recent", methods=["GET"])
def recent_tasks():
    return jsonify({"tasks": tasks[-10:][::-1]}), 200
