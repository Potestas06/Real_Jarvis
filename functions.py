import requests
import os
from dotenv import load_dotenv

load_dotenv()
base_todo_url = "https://api.todoist.com/rest/v2/tasks"

# gets the wheater by city
def check_weather(city):
    api_key = os.getenv("WHEATERKEY")
    base_wehater_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    try:
        response = requests.get(base_wehater_url, params=params)
        data = response.json()
        if data["cod"] == 200:
            weather_description = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            result = f"The weather in {city} is {weather_description}. "
            result += f"The temperature is {temperature}°C and the humidity is {humidity}%."
        else:
            result = "Sorry, I couldn't retrieve the weather information."
    except requests.exceptions.RequestException as e:
        result = "An error occurred while fetching the weather data."
    return result


# creates a todo task
def create_task(content):
    base_todo_url = "https://api.todoist.com/rest/v2/tasks"

    headers = {
        "Authorization": f"Bearer {os.getenv('TODOAPI')}",
        "Content-Type": "application/json"
    }

    data = {
        "content": content
    }

    try:
        response = requests.post(base_todo_url, headers=headers, json=data)
        if response.status_code == 200:
            result = "Task created successfully!"
        else:
            result = "Failed to create task." + response.text
    except requests.exceptions.RequestException as e:
        result = "An error occurred while creating the task."

    return result



# closes a todo task by name
def close_task_by_name(task_name):
    base_todo_url = "https://api.todoist.com/rest/v2/tasks"
    headers = {
        "Authorization": f"Bearer {os.getenv('TODOAPI')}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(base_todo_url, headers=headers)
        if response.status_code == 200:
            tasks = response.json()
            for task in tasks:
                if task["content"] == task_name:
                    task_id = task["id"]
                    close_response = requests.post(f"{base_todo_url}/{task_id}/close", headers=headers)
                    if close_response.status_code == 204:
                        return "Task closed successfully!"
                    else:
                        return "Failed to close task."
            return "Task not found."
        else:
            return "Failed to fetch tasks."
    except requests.exceptions.RequestException as e:
        return "An error occurred while closing the task."


def check_task_status(task_name):
    base_url = "https://api.todoist.com/rest/v2/tasks"

    headers = {
        "Authorization": f"Bearer {os.getenv('TODOAPI')}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(base_url, headers=headers)
        if response.status_code == 200:
            tasks = response.json()

            for task in tasks:
                if task["content"] == task_name:
                    task_id = task["id"]
                    return task["is_completed"]

            return "Task not found."
        else:
            return "Failed to fetch tasks."
    except requests.exceptions.RequestException as e:
        return "An error occurred while checking the task."



def get_undone_tasks():
    base_url = "https://api.todoist.com/rest/v2/tasks"

    headers = {
        "Authorization": f"Bearer {os.getenv('TODOAPI')}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(base_url, headers=headers)
        if response.status_code == 200:
            tasks = response.json()
            undone_tasks = []

            for task in tasks:
                if not task["is_completed"]:
                    undone_tasks.append(task["content"])

            return undone_tasks
        else:
            return "Failed to fetch tasks."
    except requests.exceptions.RequestException as e:
        return "An error occurred while retrieving undone tasks."
