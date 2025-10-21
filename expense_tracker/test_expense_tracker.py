import pytest
import os
import json
from datetime import datetime
import csv
from io import StringIO
from contextlib import redirect_stdout
from expense_tracker import (
    load_expenses, save_expenses, add_expense, update_expense, delete_expense,
    list_expenses, summary, set_budget, export_to_csv, DATA_FILE
)

@pytest.fixture
def temp_data_file(tmp_path, monkeypatch):
    temp_file = tmp_path / "expenses.json"
    # Use monkeypatch to temporarily override DATA_FILE
    monkeypatch.setattr("expense_tracker.DATA_FILE", str(temp_file))
    yield str(temp_file)
    # No need to restore DATA_FILE manually; monkeypatch handles cleanup

def test_load_expenses_new_file(temp_data_file):
    data = load_expenses()
    assert data == {"expenses": [], "budgets": {}}

def test_save_and_load_expenses(temp_data_file):
    data = {"expenses": [{"id": 1, "date": "2024-01-01", "description": "Test", "amount": 10.0, "category": "Test"}],
            "budgets": {"2024-01": 100.0}}
    save_expenses(data)
    loaded = load_expenses()
    assert loaded == data

def test_add_expense(temp_data_file):
    add_expense("Lunch", 20.0, "Food")
    data = load_expenses()
    assert len(data["expenses"]) == 1
    expense = data["expenses"][0]
    assert expense["description"] == "Lunch"
    assert expense["amount"] == 20.0
    assert expense["category"] == "Food"
    assert "id" in expense and expense["id"] == 1
    assert "date" in expense and datetime.strptime(expense["date"], "%Y-%m-%d")

def test_add_expense_invalid_amount(temp_data_file):
    with redirect_stdout(StringIO()) as out:
        add_expense("Invalid", -5.0)
    assert "Error: Amount must be positive" in out.getvalue()
    data = load_expenses()
    assert len(data["expenses"]) == 0

def test_update_expense(temp_data_file):
    add_expense("Lunch", 20.0, "Food")
    update_expense(1, description="Dinner", amount=15.0, category="Meal")
    data = load_expenses()
    expense = data["expenses"][0]
    assert expense["description"] == "Dinner"
    assert expense["amount"] == 15.0
    assert expense["category"] == "Meal"

def test_update_expense_invalid_id(temp_data_file):
    with redirect_stdout(StringIO()) as out:
        update_expense("abc")
    assert "Error: Invalid expense ID" in out.getvalue()

def test_update_expense_not_found(temp_data_file):
    with redirect_stdout(StringIO()) as out:
        update_expense(999)
    assert "Error: Expense with ID 999 not found" in out.getvalue()

def test_update_expense_invalid_amount(temp_data_file):
    add_expense("Lunch", 20.0)
    with redirect_stdout(StringIO()) as out:
        update_expense(1, amount=-10.0)
    assert "Error: Amount must be positive" in out.getvalue()
    data = load_expenses()
    assert data["expenses"][0]["amount"] == 20.0

def test_delete_expense(temp_data_file):
    add_expense("Lunch", 20.0)
    delete_expense(1)
    data = load_expenses()
    assert len(data["expenses"]) == 0

def test_delete_expense_invalid_id(temp_data_file):
    with redirect_stdout(StringIO()) as out:
        delete_expense("abc")
    assert "Error: Invalid expense ID" in out.getvalue()

def test_delete_expense_not_found(temp_data_file):
    with redirect_stdout(StringIO()) as out:
        delete_expense(999)
    assert "Error: Expense with ID 999 not found" in out.getvalue()

def test_list_expenses(temp_data_file):
    add_expense("Lunch", 20.0, "Food")
    add_expense("Bus", 5.0, "Transport")
    with redirect_stdout(StringIO()) as out:
        list_expenses()
    output = out.getvalue()
    assert "Lunch" in output
    assert "Bus" in output
    assert "$20.00" in output
    assert "$5.00" in output

def test_list_expenses_by_category(temp_data_file):
    add_expense("Lunch", 20.0, "Food")
    add_expense("Bus", 5.0, "Transport")
    with redirect_stdout(StringIO()) as out:
        list_expenses("Food")
    output = out.getvalue()
    assert "Lunch" in output
    assert "Bus" not in output

def test_list_expenses_none(temp_data_file):
    with redirect_stdout(StringIO()) as out:
        list_expenses()
    assert "No expenses found" in out.getvalue()

def test_summary_total(temp_data_file):
    add_expense("Lunch", 20.0)
    add_expense("Dinner", 10.0)
    with redirect_stdout(StringIO()) as out:
        summary()
    assert "Total expenses: $30.00" in out.getvalue()

def test_summary_monthly(temp_data_file):
    now = datetime.now()
    current_month = now.month
    current_year = now.year
    add_expense("Lunch", 20.0)  # Current date
    data = load_expenses()
    data["expenses"].append({
        "id": 2,
        "date": f"{current_year - 1}-01-01",
        "description": "Old",
        "amount": 10.0,
        "category": "Test"
    })
    save_expenses(data)
    
    with redirect_stdout(StringIO()) as out:
        summary(current_month)
    output = out.getvalue()
    assert f"Total expenses for {now.strftime('%B')}: $20.00" in output

def test_summary_invalid_month(temp_data_file):
    with redirect_stdout(StringIO()) as out:
        summary(13)
    assert "Error: Month must be between 1 and 12" in out.getvalue()

def test_set_budget(temp_data_file):
    set_budget(1, 100.0)
    data = load_expenses()
    year = datetime.now().year
    assert data["budgets"][f"{year}-01"] == 100.0

def test_set_budget_invalid_month(temp_data_file):
    with redirect_stdout(StringIO()) as out:
        set_budget(13, 100.0)
    assert "Error: Month must be between 1 and 12" in out.getvalue()

def test_set_budget_invalid_amount(temp_data_file):
    with redirect_stdout(StringIO()) as out:
        set_budget(1, -50.0)
    assert "Error: Budget amount must be non-negative" in out.getvalue()

def test_summary_with_budget_warning(temp_data_file):
    now = datetime.now()
    month = now.month
    year = now.year
    set_budget(month, 25.0)
    add_expense("Lunch", 20.0)
    add_expense("Dinner", 10.0)
    with redirect_stdout(StringIO()) as out:
        summary(month)
    output = out.getvalue()
    assert "Total expenses for" in output
    assert "$30.00" in output
    assert "Warning: Budget of $25.00 exceeded!" in output

def test_export_to_csv(temp_data_file):
    add_expense("Lunch", 20.0, "Food")
    with redirect_stdout(StringIO()) as out:
        export_to_csv()
    output = out.getvalue()
    assert "Expenses exported to" in output
    exported_file = output.split("to ")[1].strip()
    assert os.path.exists(exported_file)
    with open(exported_file, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)
        assert rows[0] == ["ID", "Date", "Description", "Amount", "Category"]
        assert len(rows) == 2  # Header + 1 expense

def test_export_to_csv_none(temp_data_file):
    with redirect_stdout(StringIO()) as out:
        export_to_csv()
    assert "No expenses to export" in out.getvalue()

def test_corrupted_data_file(temp_data_file):
    with open(temp_data_file, 'w') as f:
        f.write("invalid json")
    with redirect_stdout(StringIO()) as out:
        data = load_expenses()
    assert "Error: Corrupted data file" in out.getvalue()
    assert data == {"expenses": [], "budgets": {}}