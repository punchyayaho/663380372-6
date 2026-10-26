# my-task-manager/src/task_data.py
"""Data Access Layer: loading and saving tasks to data/tasks.json."""
import json
import os

TASKS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'tasks.json')


def load_tasks():
    """Loads tasks from the JSON file. Returns an empty list if the file is missing or corrupted."""
    if not os.path.exists(TASKS_FILE):
        os.makedirs(os.path.dirname(TASKS_FILE), exist_ok=True)  # Ensure the data directory exists
        return []
    try:
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            tasks = json.load(f)
        if not isinstance(tasks, list):
            raise ValueError("tasks.json must contain a list")
        # Older files may not have 'priority' - give them a default
        for task in tasks:
            task.setdefault("priority", "Medium")
        return tasks
    except (json.JSONDecodeError, ValueError):
        print("Warning: tasks.json is empty or corrupted. Starting with an empty task list.")
        return []
    except FileNotFoundError:
        return []
    except OSError as e:
        print(f"Warning: could not read tasks.json ({e}). Starting with an empty task list.")
        return []


def save_tasks(tasks):
    """Saves tasks to the JSON file."""
    try:
        os.makedirs(os.path.dirname(TASKS_FILE), exist_ok=True)  # Ensure directory exists
        with open(TASKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, indent=4, ensure_ascii=False)  # indent for pretty printing
        return True
    except OSError as e:
        print(f"Error: could not save tasks ({e}).")
        return False
