import sys
import json
import os
from datetime import datetime

# File where tasks are stored
TASKS_FILE = "tasks.json"

def load_tasks():
    """Load tasks from JSON file. Create file if it doesn't exist."""
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_tasks(tasks):
    """Save tasks to JSON file."""
    try:
        with open(TASKS_FILE, 'w') as f:
            json.dump(tasks, f, indent=2)
    except IOError as e:
        print(f"Error saving tasks: {e}")
        sys.exit(1)


def get_next_id(tasks):
    """Get the next available task ID."""
    return max([t['id'] for t in tasks], default=0) + 1


def add_task(description):
    """Add a new task."""
    tasks = load_tasks()
    task_id = get_next_id(tasks)
    now = datetime.now().isoformat()
    
    task = {
        'id': task_id,
        'description': description,
        'status': 'todo',
        'createdAt': now,
        'updatedAt': now
    }
    
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {task_id})")


def update_task(task_id, new_description):
    """Update a task's description."""
    tasks = load_tasks()
    
    for task in tasks:
        if task['id'] == task_id:
            task['description'] = new_description
            task['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} updated successfully")
            return
    
    print(f"Error: Task with ID {task_id} not found")
    sys.exit(1)


def delete_task(task_id):
    """Delete a task by ID."""
    tasks = load_tasks()
    
    for i, task in enumerate(tasks):
        if task['id'] == task_id:
            tasks.pop(i)
            save_tasks(tasks)
            print(f"Task {task_id} deleted successfully")
            return
    
    print(f"Error: Task with ID {task_id} not found")
    sys.exit(1)


def mark_task(task_id, status):
    """Mark a task with a specific status."""
    tasks = load_tasks()
    
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = status
            task['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
            status_text = "in progress" if status == "in-progress" else status
            print(f"Task {task_id} marked as {status_text}")
            return
    
    print(f"Error: Task with ID {task_id} not found")
    sys.exit(1)


def list_tasks(filter_status=None):
    """List tasks, optionally filtered by status."""
    tasks = load_tasks()
    
    if not tasks:
        print("No tasks found")
        return
    
    if filter_status:
        tasks = [t for t in tasks if t['status'] == filter_status]
        if not tasks:
            print(f"No tasks found with status: {filter_status}")
            return
    
    print("\n" + "─" * 80)
    print(f"{'ID':<5} {'Status':<12} {'Description':<40} {'Updated':<20}")
    print("─" * 80)
    
    for task in tasks:
        status = task['status'].replace('-', ' ').title()
        updated = datetime.fromisoformat(task['updatedAt']).strftime('%Y-%m-%d %H:%M')
        desc = task['description'][:37] + "..." if len(task['description']) > 40 else task['description']
        print(f"{task['id']:<5} {status:<12} {desc:<40} {updated:<20}")
    
    print("─" * 80 + "\n")


def print_usage():
    """Print usage information."""
    usage = """
Task Tracker CLI - Usage

Commands:
  add <description>           Add a new task
  update <id> <description>   Update a task's description
  delete <id>                 Delete a task
  mark-in-progress <id>       Mark a task as in progress
  mark-done <id>              Mark a task as done
  list [status]               List all tasks (optionally filter by status)
  list todo                   List all tasks with status 'todo'
  list in-progress            List all tasks with status 'in-progress'
  list done                   List all tasks with status 'done'

Examples:
  python task_tracker.py add "Buy groceries"
  python task_tracker.py update 1 "Buy groceries and cook dinner"
  python task_tracker.py mark-in-progress 1
  python task_tracker.py mark-done 1
  python task_tracker.py delete 1
  python task_tracker.py list
  python task_tracker.py list done
"""
    print(usage)

def main():
    """Main entry point for the CLI."""
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(0)
    
    command = sys.argv[1]
    
    try:
        if command == 'add':
            if len(sys.argv) < 3:
                print("Error: 'add' requires a description")
                sys.exit(1)
            description = ' '.join(sys.argv[2:])
            add_task(description)
        
        elif command == 'update':
            if len(sys.argv) < 4:
                print("Error: 'update' requires an ID and new description")
                sys.exit(1)
            task_id = int(sys.argv[2])
            new_description = ' '.join(sys.argv[3:])
            update_task(task_id, new_description)
        
        elif command == 'delete':
            if len(sys.argv) < 3:
                print("Error: 'delete' requires a task ID")
                sys.exit(1)
            task_id = int(sys.argv[2])
            delete_task(task_id)
        
        elif command == 'mark-in-progress':
            if len(sys.argv) < 3:
                print("Error: 'mark-in-progress' requires a task ID")
                sys.exit(1)
            task_id = int(sys.argv[2])
            mark_task(task_id, 'in-progress')
        
        elif command == 'mark-done':
            if len(sys.argv) < 3:
                print("Error: 'mark-done' requires a task ID")
                sys.exit(1)
            task_id = int(sys.argv[2])
            mark_task(task_id, 'done')
        
        elif command == 'list':
            filter_status = sys.argv[2] if len(sys.argv) > 2 else None
            list_tasks(filter_status)
        
        else:
            print(f"Error: Unknown command '{command}'")
            print_usage()
            sys.exit(1)
    
    except ValueError as e:
        print(f"Error: Invalid task ID. Task ID must be an integer")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()