import argparse
import json
import os
from datetime import datetime
import csv

DATA_FILE = "expenses.json"

def load_expenses():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        return {"expenses": [], "budgets": {}}
    except json.JSONDecodeError:
        print("Error: Corrupted data file. Starting with empty data.")
        return {"expenses": [], "budgets": {}}

def save_expenses(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def add_expense(description, amount, category=None):
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Amount must be positive")
    except ValueError as e:
        print(f"Error: {e}")
        return

    data = load_expenses()
    expense_id = max([e.get("id", 0) for e in data["expenses"]], default=0) + 1
    date = datetime.now().strftime("%Y-%m-%d")
    expense = {
        "id": expense_id,
        "date": date,
        "description": description,
        "amount": amount,
        "category": category or "Uncategorized"
    }
    data["expenses"].append(expense)
    save_expenses(data)
    print(f"Expense added successfully (ID: {expense_id})")

def update_expense(id, description=None, amount=None, category=None):
    try:
        id = int(id)
    except ValueError:
        print("Error: Invalid expense ID")
        return

    data = load_expenses()
    for expense in data["expenses"]:
        if expense["id"] == id:
            if description:
                expense["description"] = description
            if amount:
                try:
                    amount = float(amount)
                    if amount <= 0:
                        raise ValueError("Amount must be positive")
                    expense["amount"] = amount
                except ValueError as e:
                    print(f"Error: {e}")
                    return
            if category:
                expense["category"] = category
            save_expenses(data)
            print(f"Expense updated successfully (ID: {id})")
            return
    print(f"Error: Expense with ID {id} not found")

def delete_expense(id):
    try:
        id = int(id)
    except ValueError:
        print("Error: Invalid expense ID")
        return

    data = load_expenses()
    initial_len = len(data["expenses"])
    data["expenses"] = [e for e in data["expenses"] if e["id"] != id]
    if len(data["expenses"]) < initial_len:
        save_expenses(data)
        print("Expense deleted successfully")
    else:
        print(f"Error: Expense with ID {id} not found")

def list_expenses(category=None):
    data = load_expenses()
    expenses = data["expenses"]
    if category:
        expenses = [e for e in expenses if e["category"].lower() == category.lower()]
    
    if not expenses:
        print("No expenses found")
        return
    
    print("ID  Date       Description  Amount  Category")
    for e in expenses:
        print(f"{e['id']:<4}{e['date']:<11}{e['description']:<13}${e['amount']:<7.2f}{e['category']}")

def summary(month=None):
    data = load_expenses()
    expenses = data["expenses"]
    
    if month:
        try:
            month = int(month)
            if not 1 <= month <= 12:
                raise ValueError("Month must be between 1 and 12")
            year = datetime.now().year
            expenses = [e for e in expenses if e["date"].startswith(f"{year}-{month:02d}")]
            total = sum(e["amount"] for e in expenses)
            print(f"Total expenses for {datetime(year, month, 1).strftime('%B')}: ${total:.2f}")
            
            # Check budget
            budget = data.get("budgets", {}).get(f"{year}-{month:02d}", float('inf'))
            if total > budget:
                print(f"Warning: Budget of ${budget:.2f} exceeded!")
        except ValueError as e:
            print(f"Error: {e}")
            return
    else:
        total = sum(e["amount"] for e in expenses)
        print(f"Total expenses: ${total:.2f}")

def set_budget(month, amount):
    try:
        month = int(month)
        amount = float(amount)
        if not 1 <= month <= 12:
            raise ValueError("Month must be between 1 and 12")
        if amount < 0:
            raise ValueError("Budget amount must be non-negative")
    except ValueError as e:
        print(f"Error: {e}")
        return
    
    data = load_expenses()
    year = datetime.now().year
    data["budgets"][f"{year}-{month:02d}"] = amount
    save_expenses(data)
    print(f"Budget set for {datetime(year, month, 1).strftime('%B')}: ${amount:.2f}")

def export_to_csv():
    data = load_expenses()
    expenses = data["expenses"]
    if not expenses:
        print("No expenses to export")
        return
    
    output_file = f"expenses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Date", "Description", "Amount", "Category"])
        for e in expenses:
            writer.writerow([e["id"], e["date"], e["description"], e["amount"], e["category"]])
    print(f"Expenses exported to {output_file}")

def print_usage():
    """Print usage information."""
    usage = """
Task Tracker CLI - Usage

Commands:
  add --description <description> --amount <amount> --category <category>        Add an expense with a description, amount and category
  list                                                                           List all expenses
  summary                                                                        Summary of expenses
  delete --id <id>
  summary --month <month>
  set-budget --month <month> --amount <amount>
  export                                                                         Export expenses to a CSV file

Examples:
    python expense_tracker.py add --description "Lunch" --amount 20 --category "Food"
    python expense_tracker.py add --description "Dinner" --amount 10 --category "Food"
    python expense_tracker.py list
    python expense_tracker.py summary
    python expense_tracker.py delete --id 2
    python expense_tracker.py summary --month 8
    python expense_tracker.py set-budget --month 8 --amount 100
    python expense_tracker.py export
"""
    print(usage)

def main():
    parser = argparse.ArgumentParser(description="Expense Tracker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add expense
    add_parser = subparsers.add_parser("add", help="Add a new expense")
    add_parser.add_argument("--description", required=True, help="Expense description")
    add_parser.add_argument("--amount", type=float, required=True, help="Expense amount")
    add_parser.add_argument("--category", help="Expense category")

    # Update expense
    update_parser = subparsers.add_parser("update", help="Update an existing expense")
    update_parser.add_argument("--id", required=True, help="Expense ID")
    update_parser.add_argument("--description", help="New description")
    update_parser.add_argument("--amount", type=float, help="New amount")
    update_parser.add_argument("--category", help="New category")

    # Delete expense
    delete_parser = subparsers.add_parser("delete", help="Delete an expense")
    delete_parser.add_argument("--id", required=True, help="Expense ID")

    # List expenses
    list_parser = subparsers.add_parser("list", help="List all expenses")
    list_parser.add_argument("--category", help="Filter by category")

    # Summary
    summary_parser = subparsers.add_parser("summary", help="Show expense summary")
    summary_parser.add_argument("--month", type=int, help="Month number (1-12)")

    # Set budget
    budget_parser = subparsers.add_parser("set-budget", help="Set monthly budget")
    budget_parser.add_argument("--month", type=int, required=True, help="Month number (1-12)")
    budget_parser.add_argument("--amount", type=float, required=True, help="Budget amount")

    # Export to CSV
    subparsers.add_parser("export", help="Export expenses to CSV")

    args = parser.parse_args()

    if args.command == "add":
        add_expense(args.description, args.amount, args.category)
    elif args.command == "update":
        update_expense(args.id, args.description, args.amount, args.category)
    elif args.command == "delete":
        delete_expense(args.id)
    elif args.command == "list":
        list_expenses(args.category)
    elif args.command == "summary":
        summary(args.month)
    elif args.command == "set-budget":
        set_budget(args.month, args.amount)
    elif args.command == "export":
        export_to_csv()
    else:
        print_usage()

if __name__ == "__main__":
    main()