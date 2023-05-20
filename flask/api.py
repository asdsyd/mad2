from flask import Flask
from flask_restful import Resource, Api, reqparse, abort

app = Flask(__name__)
api = Api(app)

todos = {
    1:{'task': 'Write hello world progarm', 'summary': 'write the calls using python'},
    2:{'task': 'Task 2', 'summary': 'writing task two'},
    3:{'task': 'Task 3', 'summary': 'writing task three'}
}

task_post_args = reqparse.RequestParser()
task_post_args.add_argument("task", type=str, help="Task is required.", required=True)
task_post_args.add_argument("summary", type=str, help="Summary is required.", required=True)

class ToDo(Resource):
    def get(self, todo_id):
        return todos[todo_id]

    def post(self, todo_id):
        args = task_post_args.parse_args()
        if todo_id in todos:
            abort(409, "Task ID already exisits")
        todos[todo_id] = {"task": args["task"], "summary": args["summary"]}
        return todos[todo_id]

class ToDoList(Resource):
    def get(self):
        return todos

api.add_resource(ToDo, '/todos/<int:todo_id>')
api.add_resource(ToDoList, '/todos')

if __name__ == '__main__':
    app.run(port=8000,debug=True)