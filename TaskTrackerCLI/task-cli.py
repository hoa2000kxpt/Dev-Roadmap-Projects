import sys
import json
import os
from datetime import datetime

# File where tasks are stored
TASKS_FILE = "tasks.json"


# Initialize the tasks list if the task doesn't exist, or it is empty
def initialize_tasks_file():
    if not os.path.exists(TASKS_FILE) or os.path.getsize(TASKS_FILE) == 0:
        with open(TASKS_FILE, "w") as f:
            json.dump([], f)


# Load tasks from the JSON file
def load_tasks():
    with open(TASKS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


# Save tasks to the JSON file
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)


# Generate a unique ID for a new task
def generate_task_id(tasks):
    if not tasks:
        return 1
    else:
        return max(task["id"] for task in tasks) + 1


# Add a new task
def add_task(description):
    tasks = load_tasks()
    task_id = generate_task_id(tasks)
    task = {
        "id": task_id,
        "description": description,
        "status": "todo",
        "createdAt": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "updatedAt": datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {task_id})")


# Update an existing task
def update_task(task_id, new_description):
    tasks = load_tasks()
    # print(tasks)
    for task in tasks:
        if int(task["id"]) == int(task_id):
            task["description"] = new_description
            task["updatedAt"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            save_tasks(tasks)
            print(f"Task {task_id} updated successfully.")
            return

    print(f"Task {task_id} not found.")


# Delete a task
def delete_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            save_tasks(tasks)
            print(f"Task {task_id} deleted successfully.")
            return
    print(f"Task {task_id} not found.")


def update_task_status(task_id, new_status):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = new_status
            task["updatedAt"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            save_tasks(tasks)
            print(f"Task ID {task_id} marked as {new_status}")
            return
    print(f"Task ID {task_id} not found")


# Mark a task as in-progress
def mark_in_progress(task_id):
    update_task_status(task_id, "in-progress")


# Mark a task as in-progress
def mark_done(task_id):
    update_task_status(task_id, "done")


# List tasks with options to filter by status
def list_tasks(filter_status=None):
    tasks = load_tasks()
    if filter_status:
        tasks = [task for task in tasks if task["status"] == filter_status]
    if not tasks:
        print("No tasks found.")
    for task in tasks:
        print(
            f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']}, Created At: {task['createdAt']}, Updated At: {task['updatedAt']}")


# Main function to parse commands
def main():
    initialize_tasks_file()
    if len(sys.argv) < 2:
        print("Usage: task-cli.py <command> [arguments]")
        return

    command = sys.argv[1].lower()

    if command == "add" and len(sys.argv) == 3:
        add_task(sys.argv[2])
    elif command == "update" and len(sys.argv) == 4:
        # print(type(int(sys.argv[2])))
        update_task(int(sys.argv[2]), sys.argv[3])
    elif command == "delete" and len(sys.argv) == 3:
        delete_task(int(sys.argv[2]))
    elif command == "mark-in-progress" and len(sys.argv) == 3:
        mark_in_progress(int(sys.argv[2]))
    elif command == "mark-done" and len(sys.argv) == 3:
        mark_done(int(sys.argv[2]))
    elif command == "list":
        if len(sys.argv) == 3:
            list_tasks(sys.argv[2])
        else:
            list_tasks()
    else:
        print("Invalid command or missing arguments.")
        print("Available commands: add, update, delete, mark-in-progress, mark-done, list")


if __name__ == "__main__":
    main()
