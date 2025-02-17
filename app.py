from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Load tasks from JSON file
TASKS_FILE = "tasks.json"

def load_tasks():
    try:
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/tasks", methods=["GET", "POST"])
def tasks():
    tasks = load_tasks()

    if request.method == "POST":
        data = request.get_json()
        tasks.append({"id": len(tasks) + 1, "task": data["task"], "completed": False})
        save_tasks(tasks)
        return jsonify({"message": "Task added", "tasks": tasks})

    return jsonify(tasks)

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task["id"] != task_id]
    save_tasks(tasks)
    return jsonify({"message": "Task deleted", "tasks": tasks})

@app.route("/tasks/<int:task_id>/complete", methods=["PUT"])
def complete_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
    save_tasks(tasks)
    return jsonify({"message": "Task marked as completed", "tasks": tasks})

if __name__ == "__main__":
    app.run(debug=True)
