from flask import Flask, request, jsonify
from models.task import Task

app = Flask(__name__)




tasks = []
task_id_control = 1


@app.post("/tasks")
def create_task():
    data = request.get_json()
    global task_id_control
    new_task = Task(id=task_id_control,title=data['title'], description=data.get("description", ""))
    task_id_control +=1
    tasks.append(new_task)
    print(tasks)
    return jsonify({"message": "New task created!"})

@app.get("/tasks")
def get_all_tasks():
    task_list = [task.to_dict() for task in tasks ]
    output = {
            "tasks": task_list,
            "total_tasks": len(task_list)
            }
    return jsonify(output)

@app.get("/tasks/<int:id>")
def get_task_by_id(id):
    #task = None
    for t in tasks:
        if t.id == id:
            return jsonify(t.to_dict())
        
    return jsonify({"Message": "Task not found"}), 404


@app.put("/tasks/<int:id>")
def update_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t

    if task == None:
        return jsonify({"Message" : "task not found"}), 404
    
    data = request.get_json()
    task.title = data['title']
    task.description = data['description']
    task.completed = data['completed']

@app.delete("/tasks/<int:id>")
def delete_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break

    if not task:
        return jsonify({"Message" : "task not found"}), 404
    
    tasks.remove(task)
    return jsonify({"Message" : "task deleted"})

if __name__ == '__main__':
    app.run(debug=True, port=8080)