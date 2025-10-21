#!/usr/bin/env python3
import pytest
import json
import os
import sys
from datetime import datetime
from unittest.mock import patch, mock_open
from io import StringIO

# Import the task tracker module
import task_tracker

# Use a test file instead of the default
TEST_TASKS_FILE = "test_tasks.json"

@pytest.fixture
def setup_teardown():
    """Setup and teardown for each test."""
    task_tracker.TASKS_FILE = TEST_TASKS_FILE
    yield
    if os.path.exists(TEST_TASKS_FILE):
        os.remove(TEST_TASKS_FILE)

# ============================================================================
# LOAD AND SAVE TASKS TESTS
# ============================================================================

class TestLoadTasks:
    """Tests for loading tasks from JSON file."""
    
    def test_load_tasks_file_does_not_exist(self, setup_teardown):
        """Should return empty list when tasks file doesn't exist."""
        assert task_tracker.load_tasks() == []
    
    def test_load_tasks_empty_file(self, setup_teardown):
        """Should return empty list from empty JSON file."""
        with open(TEST_TASKS_FILE, 'w') as f:
            json.dump([], f)
        assert task_tracker.load_tasks() == []
    
    def test_load_tasks_with_tasks(self, setup_teardown):
        """Should load tasks from JSON file correctly."""
        sample_tasks = [
            {'id': 1, 'description': 'Task 1', 'status': 'todo', 'createdAt': '2025-01-01T10:00:00', 'updatedAt': '2025-01-01T10:00:00'}
        ]
        with open(TEST_TASKS_FILE, 'w') as f:
            json.dump(sample_tasks, f)
        
        loaded = task_tracker.load_tasks()
        assert len(loaded) == 1
        assert loaded[0]['id'] == 1
        assert loaded[0]['description'] == 'Task 1'
    
    def test_load_tasks_corrupted_json(self, setup_teardown):
        """Should return empty list if JSON is corrupted."""
        with open(TEST_TASKS_FILE, 'w') as f:
            f.write("invalid json {")
        assert task_tracker.load_tasks() == []
    
    def test_load_tasks_permission_error(self, setup_teardown):
        """Should return empty list if file cannot be read."""
        with open(TEST_TASKS_FILE, 'w') as f:
            json.dump([], f)
        os.chmod(TEST_TASKS_FILE, 0o000)
        try:
            assert task_tracker.load_tasks() == []
        finally:
            os.chmod(TEST_TASKS_FILE, 0o644)


class TestSaveTasks:
    """Tests for saving tasks to JSON file."""
    
    def test_save_tasks_creates_file(self, setup_teardown):
        """Should create tasks file if it doesn't exist."""
        tasks = [{'id': 1, 'description': 'Test', 'status': 'todo', 'createdAt': '2025-01-01T10:00:00', 'updatedAt': '2025-01-01T10:00:00'}]
        task_tracker.save_tasks(tasks)
        
        assert os.path.exists(TEST_TASKS_FILE)
        with open(TEST_TASKS_FILE) as f:
            saved = json.load(f)
        assert saved == tasks
    
    def test_save_tasks_overwrites_existing(self, setup_teardown):
        """Should overwrite existing tasks file."""
        old_tasks = [{'id': 1, 'description': 'Old', 'status': 'todo', 'createdAt': '2025-01-01T10:00:00', 'updatedAt': '2025-01-01T10:00:00'}]
        with open(TEST_TASKS_FILE, 'w') as f:
            json.dump(old_tasks, f)
        
        new_tasks = [{'id': 2, 'description': 'New', 'status': 'done', 'createdAt': '2025-01-02T10:00:00', 'updatedAt': '2025-01-02T10:00:00'}]
        task_tracker.save_tasks(new_tasks)
        
        with open(TEST_TASKS_FILE) as f:
            saved = json.load(f)
        assert saved == new_tasks
    
    def test_save_tasks_empty_list(self, setup_teardown):
        """Should save empty list correctly."""
        task_tracker.save_tasks([])
        with open(TEST_TASKS_FILE) as f:
            saved = json.load(f)
        assert saved == []
    
    def test_save_tasks_maintains_formatting(self, setup_teardown):
        """Should save tasks with proper JSON formatting."""
        tasks = [{'id': 1, 'description': 'Test', 'status': 'todo', 'createdAt': '2025-01-01T10:00:00', 'updatedAt': '2025-01-01T10:00:00'}]
        task_tracker.save_tasks(tasks)
        
        with open(TEST_TASKS_FILE) as f:
            content = f.read()
        assert '\n' in content  # Should be indented


# ============================================================================
# UTILITY FUNCTION TESTS
# ============================================================================

class TestGetNextId:
    """Tests for getting the next available task ID."""
    
    def test_get_next_id_empty_list(self, setup_teardown):
        """Should return 1 for empty list."""
        assert task_tracker.get_next_id([]) == 1
    
    def test_get_next_id_single_task(self, setup_teardown):
        """Should return correct ID after single task."""
        tasks = [{'id': 1}]
        assert task_tracker.get_next_id(tasks) == 2
    
    def test_get_next_id_multiple_tasks(self, setup_teardown):
        """Should return correct ID for multiple tasks."""
        tasks = [{'id': 1}, {'id': 2}, {'id': 5}]
        assert task_tracker.get_next_id(tasks) == 6
    
    def test_get_next_id_unordered_ids(self, setup_teardown):
        """Should return max ID + 1 regardless of order."""
        tasks = [{'id': 5}, {'id': 1}, {'id': 3}]
        assert task_tracker.get_next_id(tasks) == 6


# ============================================================================
# ADD TASK TESTS
# ============================================================================

class TestAddTask:
    """Tests for adding new tasks."""
    
    def test_add_task_single_word(self, setup_teardown, capsys):
        """Should add a task with single word description."""
        task_tracker.add_task("Groceries")
        
        captured = capsys.readouterr()
        assert "Task added successfully (ID: 1)" in captured.out
        
        tasks = task_tracker.load_tasks()
        assert len(tasks) == 1
        assert tasks[0]['id'] == 1
        assert tasks[0]['description'] == "Groceries"
        assert tasks[0]['status'] == 'todo'
    
    def test_add_task_multiple_words(self, setup_teardown, capsys):
        """Should add a task with multi-word description."""
        task_tracker.add_task("Buy groceries and cook dinner")
        
        tasks = task_tracker.load_tasks()
        assert tasks[0]['description'] == "Buy groceries and cook dinner"
    
    def test_add_task_with_special_characters(self, setup_teardown, capsys):
        """Should add a task with special characters."""
        desc = "Complete project #123 with @John & $500 budget!"
        task_tracker.add_task(desc)
        
        tasks = task_tracker.load_tasks()
        assert tasks[0]['description'] == desc
    
    def test_add_task_sets_timestamps(self, setup_teardown, capsys):
        """Should set createdAt and updatedAt timestamps."""
        before = datetime.now().isoformat()
        task_tracker.add_task("Test task")
        after = datetime.now().isoformat()
        
        tasks = task_tracker.load_tasks()
        assert 'createdAt' in tasks[0]
        assert 'updatedAt' in tasks[0]
        assert tasks[0]['createdAt'] == tasks[0]['updatedAt']
    
    def test_add_task_multiple_tasks(self, setup_teardown, capsys):
        """Should add multiple tasks with incremental IDs."""
        task_tracker.add_task("Task 1")
        task_tracker.add_task("Task 2")
        task_tracker.add_task("Task 3")
        
        tasks = task_tracker.load_tasks()
        assert len(tasks) == 3
        assert tasks[0]['id'] == 1
        assert tasks[1]['id'] == 2
        assert tasks[2]['id'] == 3
    
    def test_add_task_empty_description(self, setup_teardown, capsys):
        """Should add task even with empty description."""
        task_tracker.add_task("")
        
        tasks = task_tracker.load_tasks()
        assert len(tasks) == 1
        assert tasks[0]['description'] == ""
    
    def test_add_task_long_description(self, setup_teardown, capsys):
        """Should handle very long descriptions."""
        long_desc = "A" * 1000
        task_tracker.add_task(long_desc)
        
        tasks = task_tracker.load_tasks()
        assert tasks[0]['description'] == long_desc


# ============================================================================
# UPDATE TASK TESTS
# ============================================================================

class TestUpdateTask:
    """Tests for updating task descriptions."""
    
    def test_update_task_valid_id(self, setup_teardown, capsys):
        """Should update task with valid ID."""
        task_tracker.add_task("Old description")
        task_tracker.update_task(1, "New description")
        
        tasks = task_tracker.load_tasks()
        assert tasks[0]['description'] == "New description"
        assert tasks[0]['id'] == 1
    
    def test_update_task_updates_timestamp(self, setup_teardown, capsys):
        """Should update the updatedAt timestamp."""
        task_tracker.add_task("Task")
        tasks_before = task_tracker.load_tasks()
        created_at = tasks_before[0]['createdAt']
        
        task_tracker.update_task(1, "Updated")
        tasks_after = task_tracker.load_tasks()
        
        assert tasks_after[0]['createdAt'] == created_at
        assert tasks_after[0]['updatedAt'] != created_at
    
    def test_update_task_preserves_status(self, setup_teardown, capsys):
        """Should preserve task status when updating."""
        task_tracker.add_task("Task")
        task_tracker.mark_task(1, 'in-progress')
        task_tracker.update_task(1, "New description")
        
        tasks = task_tracker.load_tasks()
        assert tasks[0]['status'] == 'in-progress'
    
    def test_update_task_nonexistent_id(self, setup_teardown, capsys):
        """Should exit with error for nonexistent task ID."""
        with pytest.raises(SystemExit):
            task_tracker.update_task(999, "New description")
        
        captured = capsys.readouterr()
        assert "not found" in captured.out
    
    def test_update_task_empty_description(self, setup_teardown, capsys):
        """Should allow updating to empty description."""
        task_tracker.add_task("Task")
        task_tracker.update_task(1, "")
        
        tasks = task_tracker.load_tasks()
        assert tasks[0]['description'] == ""
    
    def test_update_task_multiple_tasks(self, setup_teardown, capsys):
        """Should update correct task among multiple tasks."""
        task_tracker.add_task("Task 1")
        task_tracker.add_task("Task 2")
        task_tracker.add_task("Task 3")
        
        task_tracker.update_task(2, "Updated Task 2")
        
        tasks = task_tracker.load_tasks()
        assert tasks[0]['description'] == "Task 1"
        assert tasks[1]['description'] == "Updated Task 2"
        assert tasks[2]['description'] == "Task 3"


# ============================================================================
# DELETE TASK TESTS
# ============================================================================

class TestDeleteTask:
    """Tests for deleting tasks."""
    
    def test_delete_task_single_task(self, setup_teardown, capsys):
        """Should delete the only task."""
        task_tracker.add_task("Task")
        task_tracker.delete_task(1)
        
        tasks = task_tracker.load_tasks()
        assert len(tasks) == 0
    
    def test_delete_task_multiple_tasks(self, setup_teardown, capsys):
        """Should delete correct task among multiple."""
        task_tracker.add_task("Task 1")
        task_tracker.add_task("Task 2")
        task_tracker.add_task("Task 3")
        
        task_tracker.delete_task(2)
        
        tasks = task_tracker.load_tasks()
        assert len(tasks) == 2
        assert tasks[0]['id'] == 1
        assert tasks[1]['id'] == 3
    
    def test_delete_task_nonexistent_id(self, setup_teardown, capsys):
        """Should exit with error for nonexistent task."""
        task_tracker.add_task("Task")
        
        with pytest.raises(SystemExit):
            task_tracker.delete_task(999)
        
        captured = capsys.readouterr()
        assert "not found" in captured.out
    
    def test_delete_task_first_of_many(self, setup_teardown, capsys):
        """Should correctly delete first task."""
        task_tracker.add_task("Task 1")
        task_tracker.add_task("Task 2")
        task_tracker.add_task("Task 3")
        
        task_tracker.delete_task(1)
        
        tasks = task_tracker.load_tasks()
        assert len(tasks) == 2
        assert tasks[0]['id'] == 2
    
    def test_delete_task_last_of_many(self, setup_teardown, capsys):
        """Should correctly delete last task."""
        task_tracker.add_task("Task 1")
        task_tracker.add_task("Task 2")
        task_tracker.add_task("Task 3")
        
        task_tracker.delete_task(3)
        
        tasks = task_tracker.load_tasks()
        assert len(tasks) == 2
        assert tasks[1]['id'] == 2


# ============================================================================
# MARK TASK TESTS
# ============================================================================

class TestMarkTask:
    """Tests for marking tasks with different statuses."""
    
    def test_mark_task_in_progress(self, setup_teardown, capsys):
        """Should mark task as in-progress."""
        task_tracker.add_task("Task")
        task_tracker.mark_task(1, 'in-progress')
        
        tasks = task_tracker.load_tasks()
        assert tasks[0]['status'] == 'in-progress'
    
    def test_mark_task_done(self, setup_teardown, capsys):
        """Should mark task as done."""
        task_tracker.add_task("Task")
        task_tracker.mark_task(1, 'done')
        
        tasks = task_tracker.load_tasks()
        assert tasks[0]['status'] == 'done'
    
    def test_mark_task_back_to_todo(self, setup_teardown, capsys):
        """Should be able to mark task back to todo."""
        task_tracker.add_task("Task")
        task_tracker.mark_task(1, 'in-progress')
        task_tracker.mark_task(1, 'todo')
        
        tasks = task_tracker.load_tasks()
        assert tasks[0]['status'] == 'todo'
    
    def test_mark_task_updates_timestamp(self, setup_teardown, capsys):
        """Should update updatedAt when marking task."""
        task_tracker.add_task("Task")
        tasks_before = task_tracker.load_tasks()
        updated_before = tasks_before[0]['updatedAt']
        
        task_tracker.mark_task(1, 'done')
        tasks_after = task_tracker.load_tasks()
        updated_after = tasks_after[0]['updatedAt']
        
        assert updated_after != updated_before
    
    def test_mark_task_nonexistent_id(self, setup_teardown, capsys):
        """Should exit with error for nonexistent task."""
        with pytest.raises(SystemExit):
            task_tracker.mark_task(999, 'done')
        
        captured = capsys.readouterr()
        assert "not found" in captured.out
    
    def test_mark_task_preserves_description(self, setup_teardown, capsys):
        """Should preserve description when marking."""
        task_tracker.add_task("Important task")
        task_tracker.mark_task(1, 'done')
        
        tasks = task_tracker.load_tasks()
        assert tasks[0]['description'] == "Important task"
    
    def test_mark_task_status_transitions(self, setup_teardown, capsys):
        """Should allow status transitions in any order."""
        task_tracker.add_task("Task")
        
        task_tracker.mark_task(1, 'in-progress')
        assert task_tracker.load_tasks()[0]['status'] == 'in-progress'
        
        task_tracker.mark_task(1, 'done')
        assert task_tracker.load_tasks()[0]['status'] == 'done'
        
        task_tracker.mark_task(1, 'todo')
        assert task_tracker.load_tasks()[0]['status'] == 'todo'


# ============================================================================
# LIST TASKS TESTS
# ============================================================================

class TestListTasks:
    """Tests for listing tasks with various filters."""
    
    def test_list_tasks_empty(self, setup_teardown, capsys):
        """Should display message when no tasks exist."""
        task_tracker.list_tasks()
        
        captured = capsys.readouterr()
        assert "No tasks found" in captured.out
    
    def test_list_tasks_single_task(self, setup_teardown, capsys):
        """Should display single task."""
        task_tracker.add_task("Task 1")
        task_tracker.list_tasks()
        
        captured = capsys.readouterr()
        assert "Task 1" in captured.out
        assert "Todo" in captured.out
    
    def test_list_tasks_multiple_tasks(self, setup_teardown, capsys):
        """Should display all tasks."""
        task_tracker.add_task("Task 1")
        task_tracker.add_task("Task 2")
        task_tracker.add_task("Task 3")
        task_tracker.list_tasks()
        
        captured = capsys.readouterr()
        assert "Task 1" in captured.out
        assert "Task 2" in captured.out
        assert "Task 3" in captured.out
    
    def test_list_tasks_filter_todo(self, setup_teardown, capsys):
        """Should filter tasks by todo status."""
        task_tracker.add_task("Todo task")
        task_tracker.add_task("Done task")
        task_tracker.mark_task(2, 'done')
        
        task_tracker.list_tasks('todo')
        
        captured = capsys.readouterr()
        assert "Todo task" in captured.out
        assert "Done task" not in captured.out
    
    def test_list_tasks_filter_done(self, setup_teardown, capsys):
        """Should filter tasks by done status."""
        task_tracker.add_task("Task 1")
        task_tracker.add_task("Task 2")
        task_tracker.mark_task(1, 'done')
        task_tracker.mark_task(2, 'done')
        
        task_tracker.list_tasks('done')
        
        captured = capsys.readouterr()
        assert "Task 1" in captured.out
        assert "Task 2" in captured.out
        assert captured.out.count("Done") >= 2
    
    def test_list_tasks_filter_in_progress(self, setup_teardown, capsys):
        """Should filter tasks by in-progress status."""
        task_tracker.add_task("Task 1")
        task_tracker.add_task("Task 2")
        task_tracker.mark_task(1, 'in-progress')
        
        task_tracker.list_tasks('in-progress')
        
        captured = capsys.readouterr()
        assert "Task 1" in captured.out
        assert "Task 2" not in captured.out
    
    def test_list_tasks_filter_no_matches(self, setup_teardown, capsys):
        """Should show message when filter returns no results."""
        task_tracker.add_task("Task")
        task_tracker.list_tasks('done')
        
        captured = capsys.readouterr()
        assert "No tasks found" in captured.out
    
    def test_list_tasks_displays_correct_statuses(self, setup_teardown, capsys):
        """Should display correct status formatting."""
        task_tracker.add_task("Task 1")
        task_tracker.mark_task(1, 'in-progress')
        task_tracker.list_tasks()
        
        captured = capsys.readouterr()
        assert "In Progress" in captured.out or "In-Progress" in captured.out.replace(" ", "")
    
    def test_list_tasks_truncates_long_descriptions(self, setup_teardown, capsys):
        """Should truncate very long descriptions."""
        long_desc = "A" * 100
        task_tracker.add_task(long_desc)
        task_tracker.list_tasks()
        
        captured = capsys.readouterr()
        assert "..." in captured.out


# ============================================================================
# MAIN FUNCTION TESTS
# ============================================================================

class TestMainFunction:
    """Tests for the main CLI entry point."""
    
    def test_main_no_arguments(self, setup_teardown, capsys):
        """Should print usage when no arguments provided."""
        with patch.object(sys, 'argv', ['task_tracker.py']):
            with pytest.raises(SystemExit):
                task_tracker.main()
        
        captured = capsys.readouterr()
        assert "Commands:" in captured.out or "Usage" in captured.out
    
    def test_main_add_command(self, setup_teardown, capsys):
        """Should handle add command from main."""
        with patch.object(sys, 'argv', ['task_tracker.py', 'add', 'Test', 'task']):
            task_tracker.main()
        
        tasks = task_tracker.load_tasks()
        assert len(tasks) == 1
        assert "Test task" in tasks[0]['description']
    
    def test_main_update_command(self, setup_teardown, capsys):
        """Should handle update command from main."""
        task_tracker.add_task("Original")
        
        with patch.object(sys, 'argv', ['task_tracker.py', 'update', '1', 'Updated']):
            task_tracker.main()
        
        tasks = task_tracker.load_tasks()
        assert tasks[0]['description'] == "Updated"
    
    def test_main_delete_command(self, setup_teardown, capsys):
        """Should handle delete command from main."""
        task_tracker.add_task("Task")
        
        with patch.object(sys, 'argv', ['task_tracker.py', 'delete', '1']):
            task_tracker.main()
        
        tasks = task_tracker.load_tasks()
        assert len(tasks) == 0
    
    def test_main_mark_done_command(self, setup_teardown, capsys):
        """Should handle mark-done command from main."""
        task_tracker.add_task("Task")
        
        with patch.object(sys, 'argv', ['task_tracker.py', 'mark-done', '1']):
            task_tracker.main()
        
        tasks = task_tracker.load_tasks()
        assert tasks[0]['status'] == 'done'
    
    def test_main_mark_in_progress_command(self, setup_teardown, capsys):
        """Should handle mark-in-progress command from main."""
        task_tracker.add_task("Task")
        
        with patch.object(sys, 'argv', ['task_tracker.py', 'mark-in-progress', '1']):
            task_tracker.main()
        
        tasks = task_tracker.load_tasks()
        assert tasks[0]['status'] == 'in-progress'
    
    def test_main_list_command(self, setup_teardown, capsys):
        """Should handle list command from main."""
        task_tracker.add_task("Task 1")
        task_tracker.add_task("Task 2")
        
        with patch.object(sys, 'argv', ['task_tracker.py', 'list']):
            task_tracker.main()
        
        captured = capsys.readouterr()
        assert "Task 1" in captured.out
        assert "Task 2" in captured.out
    
    def test_main_list_with_filter(self, setup_teardown, capsys):
        """Should handle list command with status filter."""
        task_tracker.add_task("Task")
        task_tracker.mark_task(1, 'done')
        
        with patch.object(sys, 'argv', ['task_tracker.py', 'list', 'done']):
            task_tracker.main()
        
        captured = capsys.readouterr()
        assert "Task" in captured.out
    
    def test_main_invalid_command(self, setup_teardown, capsys):
        """Should handle invalid command gracefully."""
        with patch.object(sys, 'argv', ['task_tracker.py', 'invalid']):
            with pytest.raises(SystemExit):
                task_tracker.main()
        
        captured = capsys.readouterr()
        assert "Unknown command" in captured.out
    
    def test_main_add_missing_description(self, setup_teardown, capsys):
        """Should exit if add command has no description."""
        with patch.object(sys, 'argv', ['task_tracker.py', 'add']):
            with pytest.raises(SystemExit):
                task_tracker.main()
        
        captured = capsys.readouterr()
        assert "requires a description" in captured.out
    
    def test_main_invalid_task_id(self, setup_teardown, capsys):
        """Should handle non-integer task IDs."""
        with patch.object(sys, 'argv', ['task_tracker.py', 'delete', 'invalid']):
            with pytest.raises(SystemExit):
                task_tracker.main()
        
        captured = capsys.readouterr()
        assert "integer" in captured.out


# ============================================================================
# EDGE CASES AND INTEGRATION TESTS
# ============================================================================

class TestEdgeCases:
    """Tests for edge cases and special scenarios."""
    
    def test_tasks_with_unicode_characters(self, setup_teardown, capsys):
        """Should handle unicode characters in descriptions."""
        task_tracker.add_task("Buy 🍎 and 🍌 from market")
        
        tasks = task_tracker.load_tasks()
        assert "🍎" in tasks[0]['description']
        assert "🍌" in tasks[0]['description']
    
    def test_tasks_with_quotes_and_escape_chars(self, setup_teardown, capsys):
        """Should handle quotes and special escape characters."""
        task_tracker.add_task('Task with "quotes" and \\backslash')
        
        tasks = task_tracker.load_tasks()
        assert '"quotes"' in tasks[0]['description']
    
    def test_tasks_with_newlines(self, setup_teardown, capsys):
        """Should handle newline characters."""
        task_tracker.add_task("Line 1\nLine 2\nLine 3")
        
        tasks = task_tracker.load_tasks()
        assert "\n" in tasks[0]['description']
    
    def test_rapid_add_delete_operations(self, setup_teardown, capsys):
        """Should handle rapid add and delete operations."""
        for i in range(10):
            task_tracker.add_task(f"Task {i}")
        
        for i in range(1, 11):
            task_tracker.delete_task(i)
        
        tasks = task_tracker.load_tasks()
        assert len(tasks) == 0
    
    def test_status_case_sensitivity(self, setup_teardown, capsys):
        """Should handle exact status values."""
        task_tracker.add_task("Task")
        task_tracker.mark_task(1, 'in-progress')
        
        tasks = task_tracker.load_tasks()
        assert tasks[0]['status'] == 'in-progress'
    
    def test_very_large_number_of_tasks(self, setup_teardown, capsys):
        """Should handle adding many tasks."""
        for i in range(100):
            task_tracker.add_task(f"Task {i}")
        
        tasks = task_tracker.load_tasks()
        assert len(tasks) == 100
        assert tasks[0]['id'] == 1
        assert tasks[99]['id'] == 100
    
    def test_id_persistence_across_deletions(self, setup_teardown, capsys):
        """Should maintain ID sequence even after deletions."""
        task_tracker.add_task("Task 1")
        task_tracker.add_task("Task 2")
        task_tracker.add_task("Task 3")
        
        task_tracker.delete_task(2)
        task_tracker.add_task("Task 4")
        
        tasks = task_tracker.load_tasks()
        ids = [t['id'] for t in tasks]
        assert 4 in ids
        assert 2 not in ids