from workflows_cdk import Response, Request
from flask import request as flask_request
from main import router

@router.route("/execute", methods=["GET", "POST"])
def execute():
    request = Request(flask_request)

    data = request.data

    first_name = data.get("first_name")
    last_name = data.get("last_name")
    time = data.get("time")
    message = data.get("message")
    output = f"Dear {first_name} {last_name}, the current time is {time}. \nHere is your message: {message}\n\nHere are your tasks:\n"

    for task in data.get("tasks", []):
        output += f"- {task.get('name')}: {task.get('description')}\n"

    # Your logic here

    return Response(data={"message": output}, metadata={"message": "Hello, World!"})