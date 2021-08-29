from flask import request
from assignment_logic.assignment2.config import app,db
from assignment_logic.assignment2.model import Task
from assignment_logic.assignment2.helper import serialize_task
db.create_all()
import json

from flask_httpauth import HTTPBasicAuth
auth=HTTPBasicAuth()
USER_DATA={"admin":"secretpassword"}

@auth.verify_password
def verify(username,password):
    if not(username and password):
        return False
    return USER_DATA.get(username)==password


@app.route("/todo/api/v1.0/tasks",methods=["POST"])
@auth.login_required
def create_task():
    task_json=request.get_json()
    print("type",type(task_json))
    if type(task_json)!=dict:
        return json.dumps({"status":"send data in Json format only"})
    else:
        if task_json["title"] and task_json["description"]:
            task=Task(
                title=task_json.get('title'),
                description=task_json.get('description'),
                done=task_json.get('done')
            )
            db.session.add(task)
            db.session.commit()
            return json.dumps({"status":"task {} created successfully".format(task.id)})
        else:
            return json.dumps({"status": "title, description fields mandatory"})

@app.route("/todo/api/v1.0/tasks",methods=["GET"])
@auth.login_required
def task_list():
    Alltask=Task.query.all()
    if Alltask and len(Alltask)>0:
        tasklist=[]
        for task in Alltask:
            serializetask=serialize_task(task)
            tasklist.append(serializetask)
        return json.dumps(tasklist)
    else:
        return json.dumps("task list is empty")


@app.route("/todo/api/v1.0/tasks/<int:task_id>",methods=["GET"])
@auth.login_required
def get_task(task_id):
    task=Task.query.filter_by(id=task_id).first()
    if task:
        serializerask=serialize_task(task)
        return json.dumps({"task":serializerask})
    else:
        return json.dumps({"status": "task {} is not present".format(task_id)})

@app.route("/todo/api/v1.0/tasks/<int:task_id>",methods=["PUT"])
@auth.login_required
def update_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if task:
        task_json = request.get_json()
        if task_json:
            task.title=task_json.get("title")
            task.description=task_json.get("description",task.description)
            task.done=task_json.get("done",task.done)
            db.session.commit()
            return json.dumps({"status":"task {} updated successfully".format(task_id)})
        else:
            return json.dumps({"status": "All fields mandatory"})
    else:
        return json.dumps({"status":"task {} is not present".format(task_id)})


@app.route("/todo/api/v1.0/tasks/<int:task_id>",methods=["DELETE"])
@auth.login_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if task:
        db.session.delete(task)
        db.session.commit()
        return json.dumps({"status":"task {} deleted successfully".format(task_id)})
    else:
        return json.dumps({"status": "task {} not present".format(task_id)})


if __name__ == '__main__':
    app.run(debug=True)