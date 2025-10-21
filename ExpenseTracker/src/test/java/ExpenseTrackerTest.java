package test.java;

import org.junit.jupiter.api.*;
import java.io.*;
import java.nio.file.*;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.*;

class ExpenseTrackerTest {
    private static final String TEST_DATA_FILE = "test_expenses.json";
    private static final String ORIGINAL_DATA_FILE = "expenses.json";
    
    @BeforeEach
    void setUp() throws IOException {
        // Point to test data file
        System.setProperty("expense.data.file", TEST_DATA_FILE);
        // Delete test file if it exists
        Files.deleteIfExists(Paths.get(TEST_DATA_FILE));
    }

    @AfterEach
    void tearDown() throws IOException {
        // Clean up test file
        Files.deleteIfExists(Paths.get(TEST_DATA_FILE));
        System.clearProperty("expense.data.file");
    }

    // Helper method to set DATA_FILE for testing
    private void useTestFile() throws NoSuchFieldException, IllegalAccessException {
        java.lang.reflect.Field field = ExpenseTracker.class.getDeclaredField("DATA_FILE");
        field.setAccessible(true);
        // Note: In a real scenario, DATA_FILE should be non-final for testing
    }

    @Test
    void testLoadExpensesNewFile() {
        ExpenseTracker.ExpenseData data = ExpenseTracker.loadExpenses();
        assertNotNull(data);
        assertTrue(data.expenses.isEmpty());
        assertTrue(data.budgets.isEmpty());
    }

    @Test
    void testSaveAndLoadExpenses() {
        ExpenseTracker.ExpenseData data = new ExpenseTracker.ExpenseData();
        ExpenseTracker.Expense expense = new ExpenseTracker.Expense(
                1, "2024-01-01", "Test", 10.0, "Test");
        data.expenses.add(expense);
        data.budgets.put("2024-01", 100.0);
        
        ExpenseTracker.saveExpenses(data);
        ExpenseTracker.ExpenseData loaded = ExpenseTracker.loadExpenses();
        
        assertEquals(1, loaded.expenses.size());
        assertEquals("Test", loaded.expenses.get(0).description);
        assertEquals(10.0, loaded.expenses.get(0).amount);
        assertEquals(100.0, loaded.budgets.get("2024-01"));
    }

    @Test
    void testAddExpense() {
        ExpenseTracker.addExpense("Lunch", 20.0, "Food");
        ExpenseTracker.ExpenseData data = ExpenseTracker.loadExpenses();
        
        assertEquals(1, data.expenses.size());
        ExpenseTracker.Expense expense = data.expenses.get(0);
        assertEquals("Lunch", expense.description);
        assertEquals(20.0, expense.amount);
        assertEquals("Food", expense.category);
        assertEquals(1, expense.id);
        assertNotNull(expense.date);
    }

    @Test
    void testAddExpenseDefaultCategory() {
        ExpenseTracker.addExpense("Lunch", 20.0, null);
        ExpenseTracker.ExpenseData data = ExpenseTracker.loadExpenses();
        
        assertEquals("Uncategorized", data.expenses.get(0).category);
    }

    @Test
    void testAddExpenseInvalidAmount() {
        ByteArrayOutputStream outContent = new ByteArrayOutputStream();
        System.setOut(new PrintStream(outContent));
        
        ExpenseTracker.addExpense("Invalid", -5.0, "Test");
        ExpenseTracker.ExpenseData data = ExpenseTracker.loadExpenses();
        
        assertTrue(outContent.toString().contains("Error: Amount must be positive"));
        assertTrue(data.expenses.isEmpty());
        
        System.setOut(System.out);
    }

    @Test
    void testAddExpenseZeroAmount() {
        ByteArrayOutputStream outContent = new ByteArrayOutputStream();
        System.setOut(new PrintStream(outContent));
        
        ExpenseTracker.addExpense("Zero", 0.0, "Test");
        ExpenseTracker.ExpenseData data = ExpenseTracker.loadExpenses();
        
        assertTrue(outContent.toString().contains("Error: Amount must be positive"));
        assertTrue(data.expenses.isEmpty());
        
        System.setOut(System.out);
    }

    @Test
    void testUpdateExpense() {
        ExpenseTracker.addExpense("Lunch", 20.0, "Food");
        ExpenseTracker.updateExpense(1, "Dinner", 15.0, "Meal");
        ExpenseTracker.ExpenseData data = ExpenseTracker.loadExpenses();
        
        ExpenseTracker.Expense expense = data.expenses.get(0);
        assertEquals("Dinner", expense.description);
        assertEquals(15.0, expense.amount);
        assertEquals("Meal", expense.category);
    }

    @Test
    void testUpdateExpensePartial() {
        ExpenseTracker.addExpense("Lunch", 20.0, "Food");
        ExpenseTracker.updateExpense(1, "Lunch Updated", null, null);
        ExpenseTracker.ExpenseData data = ExpenseTracker.loadExpenses();
        
        ExpenseTracker.Expense expense = data.expenses.get(0);
        assertEquals("Lunch Updated", expense.description);
        assertEquals(20.0, expense.amount);
        assertEquals("Food", expense.category);
    }

    @Test
    void testUpdateExpenseNotFound() {
        ByteArrayOutputStream outContent = new ByteArrayOutputStream();
        System.setOut(new PrintStream(outContent));
        
        ExpenseTracker.updateExpense(999, "Test", null, null);
        
        assertTrue(outContent.toString().contains("Error: Expense with ID 999 not found"));
        System.setOut(System.out);
    }

    @Test
    void testUpdateExpenseInvalidAmount() {
        ExpenseTracker.addExpense("Lunch", 20.0, null);
        ByteArrayOutputStream outContent = new ByteArrayOutputStream();
        System.setOut(new PrintStream(outContent));
        
        ExpenseTracker.updateExpense(1, null, -10.0, null);
        ExpenseTracker.ExpenseData data = ExpenseTracker.loadExpenses();
        
        assertTrue(outContent.toString().contains("Error: Amount must be positive"));
        assertEquals(20.0, data.expenses.get(0).amount);
        System.setOut(System.out);
    }

    @Test
    void testDeleteExpense() {
        ExpenseTracker.addExpense("Lunch", 20.0, null);
        ExpenseTracker.deleteExpense(1);
        ExpenseTracker.ExpenseData data = ExpenseTracker.loadExpenses();
        
        assertTrue(data.expenses.isEmpty());
    }

    @Test
    void testDeleteExpenseNotFound() {
        ByteArrayOutputStream outContent = new ByteArrayOutputStream();
        System.setOut(new PrintStream(outContent));
        
        ExpenseTracker.deleteExpense(999);
        
        assertTrue(outContent.toString().contains("Error: Expense with ID 999 not found"));
        System.setOut(System.out);
    }

    @Test
    void testListExpensesAll() {
        ExpenseTracker.addExpense("Lunch", 20.0, "Food");
        ExpenseTracker.addExpense("Bus", 5.0, "Transport");
        
        List<ExpenseTracker.Expense> expenses = ExpenseTracker.listExpenses(null);
        
        assertEquals(2, expenses.size());
        assertEquals("Lunch", expenses.get(0).description);
        assertEquals("Bus", expenses.get(1).description);
    }

    @Test
    void testListExpensesByCategory() {
        ExpenseTracker.addExpense("Lunch", 20.0, "Food");
        ExpenseTracker.addExpense("Bus", 5.0, "Transport");
        
        List<ExpenseTracker.Expense> expenses = ExpenseTracker.listExpenses("Food");
        
        assertEquals(1, expenses.size());
        assertEquals("Lunch", expenses.get(0).description);
    }

    @Test
    void testListExpensesCategoryInsensitive() {
        ExpenseTracker.addExpense("Lunch", 20.0, "Food");
        
        List<ExpenseTracker.Expense> expenses = ExpenseTracker.listExpenses("FOOD");
        
        assertEquals(1, expenses.size());
    }

    @Test
    void testListExpensesNone() {
        List<ExpenseTracker.Expense> expenses = ExpenseTracker.listExpenses(null);
        
        assertTrue(expenses.isEmpty());
    }

    @Test
    void testSummaryTotal() {
        ExpenseTracker.addExpense("Lunch", 20.0, null);
        ExpenseTracker.addExpense("Dinner", 10.0, null);
        
        ByteArrayOutputStream outContent = new ByteArrayOutputStream();
        System.setOut(new PrintStream(outContent));
        
        ExpenseTracker.summary(null);
        
        assertTrue(outContent.toString().contains("Total expenses: $30.00"));
        System.setOut(System.out);
    }

    @Test
    void testSummaryMonthly() {
        ExpenseTracker.addExpense("Lunch", 20.0, null);
        
        int currentMonth = LocalDate.now().getMonth().getValue();
        
        ByteArrayOutputStream outContent = new ByteArrayOutputStream();
        System.setOut(new PrintStream(outContent));
        
        ExpenseTracker.summary(currentMonth);
        
        String output = outContent.toString();
        assertTrue(output.contains("Total expenses for"));
        assertTrue(output.contains("$20.00"));
        System.setOut(System.out);
    }

    @Test
    void testSummaryMonthlyInvalid() {
        ByteArrayOutputStream outContent = new ByteArrayOutputStream();
        System.setOut(new PrintStream(outContent));
        
        ExpenseTracker.summary(13);
        
        assertTrue(outContent.toString().contains("Error: Month must be between 1 and 12"));
        System.setOut(System.out);
    }

    @Test
    void testSummaryMonthlyZero() {
        ByteArrayOutputStream outContent = new ByteArrayOutputStream();
        System.setOut(new PrintStream(outContent));
        
        ExpenseTracker.summary(0);
        
        assertTrue(outContent.toString().contains("Error: Month must be between 1 and 12"));
        System.setOut(System.out);
    }

    @Test
    void testSetBudget() {
        ExpenseTracker.setBudget(1, 100.0);
        ExpenseTracker.ExpenseData data = ExpenseTracker.loadExpenses();
        int year = LocalDate.now().getYear();
        
        assertEquals(100.0, data.budgets.get(year + "-01"));
    }

    @Test
    void testSetBudgetInvalidMonth() {
        ByteArrayOutputStream outContent = new ByteArrayOutputStream();
        System.setOut(new PrintStream(outContent));
        
        ExpenseTracker.setBudget(13, 100.0);
        
        assertTrue(outContent.toString().contains("Error: Month must be between 1 and 12"));
        System.setOut(System.out);
    }

    @Test
    void testSetBudgetNegativeAmount() {
        ByteArrayOutputStream outContent = new ByteArrayOutputStream();
        System.setOut(new PrintStream(outContent));
        
        ExpenseTracker.setBudget(1, -50.0);
        
        assertTrue(outContent.toString().contains("Error: Budget amount must be non-negative"));
        System.setOut(System.out);
    }

    @Test
    void testSetBudgetZeroAmount() {
        ExpenseTracker.setBudget(1, 0.0);
        ExpenseTracker.ExpenseData data = ExpenseTracker.loadExpenses();
        int year = LocalDate.now().getYear();
        
        assertEquals(0.0, data.budgets.get(year + "-01"));
    }

    @Test
    void testSummaryWithBudgetWarning() {
        int currentMonth = LocalDate.now().getMonth().getValue();
        ExpenseTracker.setBudget(currentMonth, 25.0);
        ExpenseTracker.addExpense("Lunch", 20.0, null);
        ExpenseTracker.addExpense("Dinner", 10.0, null);
        
        ByteArrayOutputStream outContent = new ByteArrayOutputStream();
        System.setOut(new PrintStream(outContent));
        
        ExpenseTracker.summary(currentMonth);
        
        String output = outContent.toString();
        assertTrue(output.contains("Total expenses for"));
        assertTrue(output.contains("$30.00"));
        assertTrue(output.contains("Warning: Budget of $25.00 exceeded!"));
        System.setOut(System.out);
    }

    @Test
    void testSummaryWithinBudget() {
        int currentMonth = LocalDate.now().getMonth().getValue();
        ExpenseTracker.setBudget(currentMonth, 100.0);
        ExpenseTracker.addExpense("Lunch", 20.0, null);
        
        ByteArrayOutputStream outContent = new ByteArrayOutputStream();
        System.setOut(new PrintStream(outContent));
        
        ExpenseTracker.summary(currentMonth);
        
        String output = outContent.toString();
        assertFalse(output.contains("Warning"));
        System.setOut(System.out);
    }

    @Test
    void testExportToCsv() throws IOException {
        ExpenseTracker.addExpense("Lunch", 20.0, "Food");
        
        ByteArrayOutputStream outContent = new ByteArrayOutputStream();
        System.setOut(new PrintStream(outContent));
        
        ExpenseTracker.exportToCsv();
        
        String output = outContent.toString();
        assertTrue(output.contains("Expenses exported to"));
        
        String exportedFile = output.split("to ")[1].trim();
        assertTrue(Files.exists(Paths.get(exportedFile)));
        
        String content = new String(Files.readAllBytes(Paths.get(exportedFile)));
        assertTrue(content.contains("ID,Date,Description,Amount,Category"));
        assertTrue(content.contains("Lunch"));
        
        Files.deleteIfExists(Paths.get(exportedFile));
        System.setOut(System.out);
    }

    @Test
    void testExportToCsvEmpty() {
        ByteArrayOutputStream outContent = new ByteArrayOutputStream();
        System.setOut(new PrintStream(outContent));
        
        ExpenseTracker.exportToCsv();
        
        assertTrue(outContent.toString().contains("No expenses to export"));
        System.setOut(System.out);
    }

    @Test
    void testMultipleExpensesWithIncrementingIds() {
        ExpenseTracker.addExpense("Lunch", 20.0, "Food");
        ExpenseTracker.addExpense("Bus", 5.0, "Transport");
        ExpenseTracker.addExpense("Coffee", 3.0, "Food");
        
        ExpenseTracker.ExpenseData data = ExpenseTracker.loadExpenses();
        assertEquals(3, data.expenses.size());
        assertEquals(1, data.expenses.get(0).id);
        assertEquals(2, data.expenses.get(1).id);
        assertEquals(3, data.expenses.get(2).id);
    }

    @Test
    void testDeleteAndAddNewExpense() {
        ExpenseTracker.addExpense("Lunch", 20.0, null);
        ExpenseTracker.deleteExpense(1);
        ExpenseTracker.addExpense("Dinner", 15.0, null);
        
        ExpenseTracker.ExpenseData data = ExpenseTracker.loadExpenses();
        assertEquals(1, data.expenses.size());
        assertEquals(2, data.expenses.get(0).id);
        assertEquals("Dinner", data.expenses.get(0).description);
    }
}
