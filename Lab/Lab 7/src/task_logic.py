# my-task-manager/src/task_logic.py
"""Business Logic Layer: add, list, complete, delete and search tasks."""

PRIORITIES = ("High", "Medium", "Low")
LINE = "=" * 64
DIVIDER = "-" * 64


def get_next_task_id(tasks):
    """Generates a unique ID for a new task."""
    if not tasks:
        return 1
    return max(task['id'] for task in tasks) + 1


def add_task(tasks, description, priority="Medium"):
    """Adds a new task to the list."""
    if priority not in PRIORITIES:
        priority = "Medium"
    task_id = get_next_task_id(tasks)
    tasks.append({
        "id": task_id,
        "description": description,
        "priority": priority,
        "completed": False,
    })
    print(f"Task '{description}' added with ID {task_id} (Priority: {priority}).")
    return tasks


def _print_table(tasks):
    print("\n" + LINE)
    print(f"{'ID':<6}| {'Status':<12}| {'Priority':<10}| Description")
    print(DIVIDER)
    for task in tasks:
        status = "[DONE]" if task['completed'] else "[PENDING]"
        print(f"{'#' + str(task['id']):<6}| {status:<12}| {task.get('priority', 'Medium'):<10}| {task['description']}")
    print(LINE)


def list_tasks(tasks, status_filter=None):
    """
    Lists tasks in a table.
    status_filter: None = all tasks, "pending" = only pending, "completed" = only completed.
    """
    if status_filter == "pending":
        shown = [t for t in tasks if not t['completed']]
    elif status_filter == "completed":
        shown = [t for t in tasks if t['completed']]
    else:
        shown = tasks
    if not shown:
        print("No tasks found.")
        return
    _print_table(shown)
    done = sum(1 for t in tasks if t['completed'])
    print(f"Summary: {done}/{len(tasks)} task(s) completed.")


def search_tasks(tasks, keyword):
    """Shows tasks whose description contains the keyword (case-insensitive)."""
    results = [t for t in tasks if keyword.lower() in t['description'].lower()]
    if not results:
        print(f"No tasks match '{keyword}'.")
        return []
    _print_table(results)
    print(f"Found {len(results)} task(s) matching '{keyword}'.")
    return results


def complete_task(tasks, task_id):
    """Marks a task as completed."""
    for task in tasks:
        if task['id'] == task_id:
            if task['completed']:
                print(f"Task ID {task_id} is already completed.")
            else:
                task['completed'] = True
                print(f"Task ID {task_id} marked as completed.")
            return tasks
    print(f"Error: Task with ID {task_id} not found.")
    return tasks


def delete_task(tasks, task_id):
    """Deletes a task from the list."""
    original_len = len(tasks)
    tasks[:] = [task for task in tasks if task['id'] != task_id]  # Reassigns list in-place
    if len(tasks) < original_len:
        print(f"Task ID {task_id} deleted successfully.")
    else:
        print(f"Error: Task with ID {task_id} not found.")
    return tasks
