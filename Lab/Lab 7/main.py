# my-task-manager/main.py
"""Presentation Layer: CLI menu and defensive user input."""
import os
import sys

# Add the 'src' directory to the Python path so the modules can be imported directly
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

import task_data   # noqa: E402
import task_logic  # noqa: E402


def display_menu():
    """Displays the main menu options to the user."""
    print("\n" + "=" * 34)
    print(f"{'TASK MANAGER CLI':^34}")
    print("=" * 34)
    print("  1. Add New Task")
    print("  2. List All Tasks")
    print("  3. List Pending Tasks")
    print("  4. List Completed Tasks")
    print("  5. Search Tasks by Keyword")
    print("  6. Mark Task as Completed")
    print("  7. Delete Task")
    print("  8. Save and Exit")
    print("=" * 34)


def ask_task_id(prompt):
    """Asks for a task ID; returns an int or None if the input is not a number."""
    task_id_str = input(prompt).strip()
    try:
        return int(task_id_str)
    except ValueError:
        print("Invalid input. Please enter a number for Task ID.")
        return None


def ask_priority():
    """Asks for a priority; defaults to Medium on empty/invalid input."""
    choice = input("Priority (1=High, 2=Medium, 3=Low) [2]: ").strip()
    return {"1": "High", "2": "Medium", "3": "Low"}.get(choice, "Medium")


def main():
    """Main function to run the Task Manager application."""
    tasks = task_data.load_tasks()  # Load tasks at startup
    try:
        while True:
            display_menu()
            choice = input("Enter choice (1-8): ").strip()

            if choice == '1':
                description = input("Enter task description: ").strip()
                if description:
                    tasks = task_logic.add_task(tasks, description, ask_priority())
                    task_data.save_tasks(tasks)  # auto-save
                else:
                    print("Task description cannot be empty.")
            elif choice == '2':
                task_logic.list_tasks(tasks)
            elif choice == '3':
                task_logic.list_tasks(tasks, "pending")
            elif choice == '4':
                task_logic.list_tasks(tasks, "completed")
            elif choice == '5':
                keyword = input("Enter keyword: ").strip()
                if keyword:
                    task_logic.search_tasks(tasks, keyword)
                else:
                    print("Keyword cannot be empty.")
            elif choice == '6':
                task_id = ask_task_id("Enter ID of task to complete: ")
                if task_id is not None:
                    tasks = task_logic.complete_task(tasks, task_id)
                    task_data.save_tasks(tasks)
            elif choice == '7':
                task_id = ask_task_id("Enter ID of task to delete: ")
                if task_id is not None:
                    tasks = task_logic.delete_task(tasks, task_id)
                    task_data.save_tasks(tasks)
            elif choice == '8':
                task_data.save_tasks(tasks)  # Save tasks before exiting
                print("Saving tasks and exiting. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 8.")
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C / Ctrl+Z: save before leaving so nothing is lost
        task_data.save_tasks(tasks)
        print("\nInterrupted. Tasks saved. Goodbye!")


if __name__ == "__main__":
    main()
