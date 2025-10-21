import com.google.gson.*;
import java.io.*;
import java.nio.file.*;
import java.time.LocalDate;
import java.time.YearMonth;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.stream.Collectors;

public class ExpenseTracker {
    private static final String DATA_FILE = "expenses.json";
    private static final DateTimeFormatter dateFormatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
    private static final Gson gson = new GsonBuilder().setPrettyPrinting().create();

    static class Expense {
        int id;
        String date;
        String description;
        double amount;
        String category;

        Expense(int id, String date, String description, double amount, String category) {
            this.id = id;
            this.date = date;
            this.description = description;
            this.amount = amount;
            this.category = category;
        }
    }

    static class ExpenseData {
        List<Expense> expenses;
        Map<String, Double> budgets;

        ExpenseData() {
            this.expenses = new ArrayList<>();
            this.budgets = new HashMap<>();
        }
    }

    public static ExpenseData loadExpenses() {
        try {
            Path path = Paths.get(DATA_FILE);
            if (Files.exists(path)) {
                String content = new String(Files.readAllBytes(path));
                return gson.fromJson(content, ExpenseData.class);
            }
            return new ExpenseData();
        } catch (JsonSyntaxException e) {
            System.out.println("Error: Corrupted data file. Starting with empty data.");
            return new ExpenseData();
        } catch (IOException e) {
            return new ExpenseData();
        }
    }

    public static void saveExpenses(ExpenseData data) {
        try {
            Files.write(Paths.get(DATA_FILE), gson.toJson(data).getBytes());
        } catch (IOException e) {
            System.out.println("Error: Unable to save expenses - " + e.getMessage());
        }
    }

    public static void addExpense(String description, double amount, String category) {
        try {
            if (amount <= 0) {
                throw new IllegalArgumentException("Amount must be positive");
            }

            ExpenseData data = loadExpenses();
            int expenseId = data.expenses.stream()
                    .mapToInt(e -> e.id)
                    .max()
                    .orElse(0) + 1;

            String date = LocalDate.now().format(dateFormatter);
            Expense expense = new Expense(expenseId, date, description, amount, 
                    category != null ? category : "Uncategorized");
            data.expenses.add(expense);
            saveExpenses(data);
            System.out.println("Expense added successfully (ID: " + expenseId + ")");
        } catch (IllegalArgumentException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    public static void updateExpense(int id, String description, Double amount, String category) {
        ExpenseData data = loadExpenses();
        
        for (Expense expense : data.expenses) {
            if (expense.id == id) {
                if (description != null) {
                    expense.description = description;
                }
                if (amount != null) {
                    if (amount <= 0) {
                        System.out.println("Error: Amount must be positive");
                        return;
                    }
                    expense.amount = amount;
                }
                if (category != null) {
                    expense.category = category;
                }
                saveExpenses(data);
                System.out.println("Expense updated successfully (ID: " + id + ")");
                return;
            }
        }
        System.out.println("Error: Expense with ID " + id + " not found");
    }

    public static void deleteExpense(int id) {
        ExpenseData data = loadExpenses();
        int initialSize = data.expenses.size();
        
        data.expenses = data.expenses.stream()
                .filter(e -> e.id != id)
                .collect(Collectors.toList());
        
        if (data.expenses.size() < initialSize) {
            saveExpenses(data);
            System.out.println("Expense deleted successfully");
        } else {
            System.out.println("Error: Expense with ID " + id + " not found");
        }
    }

    public static List<Expense> listExpenses(String category) {
        ExpenseData data = loadExpenses();
        List<Expense> expenses = data.expenses;
        
        if (category != null) {
            expenses = expenses.stream()
                    .filter(e -> e.category.equalsIgnoreCase(category))
                    .collect(Collectors.toList());
        }
        
        return expenses;
    }

    public static void printExpenses(List<Expense> expenses) {
        if (expenses.isEmpty()) {
            System.out.println("No expenses found");
            return;
        }
        
        System.out.printf("%-4s%-11s%-13s%-8s%s%n", "ID", "Date", "Description", "Amount", "Category");
        for (Expense e : expenses) {
            System.out.printf("%-4d%-11s%-13s$%-7.2f%s%n", e.id, e.date, e.description, e.amount, e.category);
        }
    }

    public static void summary(Integer month) {
        ExpenseData data = loadExpenses();
        List<Expense> expenses = data.expenses;
        
        if (month != null) {
            if (month < 1 || month > 12) {
                System.out.println("Error: Month must be between 1 and 12");
                return;
            }
            
            int year = LocalDate.now().getYear();
            String monthStr = String.format("%d-%02d", year, month);
            
            expenses = expenses.stream()
                    .filter(e -> e.date.startsWith(monthStr))
                    .collect(Collectors.toList());
            
            double total = expenses.stream().mapToDouble(e -> e.amount).sum();
            String monthName = YearMonth.of(year, month).getMonth().toString();
            System.out.printf("Total expenses for %s: $%.2f%n", monthName, total);
            
            Double budget = data.budgets.get(monthStr);
            if (budget != null && total > budget) {
                System.out.printf("Warning: Budget of $%.2f exceeded!%n", budget);
            }
        } else {
            double total = expenses.stream().mapToDouble(e -> e.amount).sum();
            System.out.printf("Total expenses: $%.2f%n", total);
        }
    }

    public static void setBudget(int month, double amount) {
        if (month < 1 || month > 12) {
            System.out.println("Error: Month must be between 1 and 12");
            return;
        }
        if (amount < 0) {
            System.out.println("Error: Budget amount must be non-negative");
            return;
        }
        
        ExpenseData data = loadExpenses();
        int year = LocalDate.now().getYear();
        String monthStr = String.format("%d-%02d", year, month);
        data.budgets.put(monthStr, amount);
        saveExpenses(data);
        
        String monthName = YearMonth.of(year, month).getMonth().toString();
        System.out.printf("Budget set for %s: $%.2f%n", monthName, amount);
    }

    public static void exportToCsv() {
        ExpenseData data = loadExpenses();
        
        if (data.expenses.isEmpty()) {
            System.out.println("No expenses to export");
            return;
        }
        
        String timestamp = LocalDate.now().format(DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss"));
        String outputFile = "expenses_" + timestamp + ".csv";
        
        try (FileWriter writer = new FileWriter(outputFile)) {
            writer.append("ID,Date,Description,Amount,Category\n");
            for (Expense e : data.expenses) {
                writer.append(String.format("%d,%s,%s,%.2f,%s%n", 
                        e.id, e.date, e.description, e.amount, e.category));
            }
            System.out.println("Expenses exported to " + outputFile);
        } catch (IOException e) {
            System.out.println("Error: Unable to export expenses - " + e.getMessage());
        }
    }

    public static void printUsage() {
        String usage = """
            Expense Tracker CLI - Usage
            
            Commands:
              add --description <description> --amount <amount> --category <category>
              list [--category <category>]
              summary [--month <month>]
              update --id <id> [--description <description>] [--amount <amount>] [--category <category>]
              delete --id <id>
              set-budget --month <month> --amount <amount>
              export
            
            Examples:
              java ExpenseTracker add --description "Lunch" --amount 20 --category "Food"
              java ExpenseTracker list
              java ExpenseTracker summary
              java ExpenseTracker summary --month 8
              java ExpenseTracker delete --id 1
              java ExpenseTracker export
            """;
        System.out.println(usage);
    }

    public static void main(String[] args) {
        if (args.length == 0) {
            printUsage();
            return;
        }

        String command = args[0];

        try {
            switch (command) {
                case "add":
                    String description = getArgument(args, "--description");
                    double amount = Double.parseDouble(getArgument(args, "--amount"));
                    String category = getArgument(args, "--category");
                    addExpense(description, amount, category);
                    break;

                case "list":
                    String filterCategory = getArgument(args, "--category");
                    printExpenses(listExpenses(filterCategory));
                    break;

                case "summary":
                    String monthStr = getArgument(args, "--month");
                    Integer month = monthStr != null ? Integer.parseInt(monthStr) : null;
                    summary(month);
                    break;

                case "update":
                    int id = Integer.parseInt(getArgument(args, "--id"));
                    String newDesc = getArgument(args, "--description");
                    String amountStr = getArgument(args, "--amount");
                    Double newAmount = amountStr != null ? Double.parseDouble(amountStr) : null;
                    String newCategory = getArgument(args, "--category");
                    updateExpense(id, newDesc, newAmount, newCategory);
                    break;

                case "delete":
                    int delId = Integer.parseInt(getArgument(args, "--id"));
                    deleteExpense(delId);
                    break;

                case "set-budget":
                    int budgetMonth = Integer.parseInt(getArgument(args, "--month"));
                    double budgetAmount = Double.parseDouble(getArgument(args, "--amount"));
                    setBudget(budgetMonth, budgetAmount);
                    break;

                case "export":
                    exportToCsv();
                    break;

                default:
                    printUsage();
            }
        } catch (NumberFormatException e) {
            System.out.println("Error: Invalid number format - " + e.getMessage());
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    private static String getArgument(String[] args, String flag) {
        for (int i = 0; i < args.length - 1; i++) {
            if (args[i].equals(flag)) {
                return args[i + 1];
            }
        }
        return null;
    }
}