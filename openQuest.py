import os
from dotenv import load_dotenv
import openai
import json
import functions

load_dotenv()
openai.api_key = os.getenv("OPENAIKEY")
url = "https://api.openai.com/v1/chat/completions"
previous = []
function_list = [
        {
            "name": "check_weather",
            "description": "Get the current weather from a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city to get the weather from, e.g. London"
                    }
                },
                "required": ["city"]
            }
        },
        {
            "name": "create_task",
            "description": "Creates a task",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "The content of the task, e.g. buy milk"
                    }
                },
                "required": ["content"]
            }
        },
        {
            "name": "check_task_status",
            "description": "Checks if a task is done",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_name": {
                        "type": "string",
                        "description": "The name of the task, e.g. buy milk"
                    }
                },
                "required": ["task_name"]
            }
        },
        {
            "name": "close_task_by_name",
            "description": "Closes a task with a given name",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_name": {
                        "type": "string",
                        "description": "The name of the task, e.g. buy milk"
                    }
                },
                "required": ["task_name"]
            }
        },
        {
            "name": "get_undone_tasks",
            "description": "Gets all undone tasks and returns them as a list",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_name": {
                        "type": "string",
                        "description": "A list of all undone tasks"
                    }
                }
            },
            "required": []
        }
    ]

def second_request(function_name, content):
    message = [{
        "role": "function",
        "name": function_name,
        "content": content
    }]
    messages = message + [{"role": msg["role"], "content": msg["content"]} for msg in previous]

    response = openai.ChatCompletion.create(
        model=os.getenv("MODEL"),
        messages=messages,
        functions=function_list,
        function_call="auto"
    )

    print("response: " + response)
    message = response.choices[0].message # type: ignore
    previous.append(message)
    return message["content"]

def request(text):
    message = [{
        "role": "user",
        "content": text
    }]
    messages = message + [{"role": msg["role"], "content": msg["content"]} for msg in previous]

    response = openai.ChatCompletion.create(
        model=os.getenv("MODEL"),
        messages=messages,
        functions=function_list,
        function_call="auto"
    )
    print(response)
    message = response.choices[0].message # type: ignore
    previous.append(message)

    if "function_call" in message:
        function_call = message["function_call"]
        arguments = json.loads(function_call["arguments"])

        response = None
        function_name = function_call["name"]

        if function_name == "check_weather":
            print(arguments["city"])
            response = functions.check_weather(arguments["city"])
        elif function_name == "create_task":
            response = functions.create_task(arguments["content"])
        elif function_name == "check_task_status":
            response = functions.check_task_status(arguments["task_name"])
        elif function_name == "close_task_by_name":
            response = functions.close_task_by_name(arguments["task_name"])
        elif function_name == "get_undone_tasks":
            response = functions.get_undone_tasks()

        if response is not None:
            print(response)
            second_request(function_name, response)
    else:
        return message["content"]

request("what is the wehater in berlin?")