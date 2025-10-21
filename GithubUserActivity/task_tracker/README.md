# Task Tracker CLI App
The [task-tracker](https://roadmap.sh/projects/task-tracker) challenge from [roadmap.sh](https://roadmap.sh/).

Task Tracker CLI is a simple command-line interface application to help you track and manage your tasks. This tool allows you to add, update, delete, and list tasks, as well as mark them as in-progress or done. Tasks are stored in a JSON file, making it easy to persist and manage your to-do list.

## Features 🔥

- **Add Tasks**: Quickly add new tasks with a description.
- **Update Tasks**: Modify the description of existing tasks.
- **Delete Tasks**: Remove tasks that are no longer needed.
- **Mark as In Progress**: Mark tasks that you are currently working on.
- **Mark as Done**: Mark tasks as completed.
- **List Tasks**: View all tasks or filter by status (`todo`, `in-progress`, `done`).

## Installation 📦

1. Clone the repository:
    ```bash
    git clone https://github.com/hoa2000kxpt/python_dev_roadmap_TaskTrackerCLI.git
    cd task-tracker-cli
    ```

2. Ensure you have Python installed on your system.

3. No external libraries are required, so you're ready to go!

## Usage 🚀

Run the script with the following commands:

```bash
# Add new task
python task-cli.py add "Buy groceries"

# Update and delete tasks
python task-cli.py update 2 "Buy groceries and cook dinner"
python task-cli.py delete 2

# Mark a task as in progress or done
python task-cli.py mark-in-progress 2
python task-cli.py mark-done 2

# List all tasks
python task-cli.py list

# List tasks by status
python task-cli.py list done
python task-cli.py list todo
python task-cli.py list in-progress
```
