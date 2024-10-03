"""
A buget tracker app that will help monitor their spending, create and update
expense categories, track income, and calculate remaining
funds based on their budget.
"""
# Imports
import sqlite3


class BudgetTracker:
    """
    Database handleling will check if its created and if not will make one
    """
    def __init__(self):
        self.conn = sqlite3.connect('buget_tracker.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Creates income and expense table
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS income (
            id INTEGER PRIMARY KEY,
            category TEXT,
            amount REAL,
            date TEXT)'''
        )
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS expense (
            id INTEGER PRIMARY KEY,
            category TEXT,
            amount REAL,
            date TEXT)'''
            )
        self.conn.commit()

    """
    Methods to add both the income and expenses in
    their respective table
    """
    def add_expense(self, category, amount, date):
        try:
            self.cursor.execute(
                'INSERT INTO expense (category ,amount, date)'
                'VALUES (?, ?, ?)',
                (category, amount, date)
            )
            self.conn.commit()
            print("Expense added succesfully")
        except Exception as e:
            print(f"Error adding expense: {e}")  # e is the error that occured

    def add_income(self, category, amount, date):
        try:
            self.cursor.execute(
                'INSERT INTO income (category ,amount, date) VALUES (?, ?, ?)',
                (category, amount, date)
            )
            self.conn.commit()
            print("Income added succesfully")
        except Exception as e:
            print(f"Error adding income: {e}")

    """
    Methods to view both the income and expenses in
    their respective table
    """

    def view_expenses(self):
        self.cursor.execute('SELECT * FROM expense')
        rows = self.cursor.fetchall()
        if rows:
            print("\nExpense records: ")
            for row in rows:
                print(row)
        else:
            print("No expenses found")

    def view_income(self):
        self.cursor.execute('SELECT * FROM income')
        rows = self.cursor.fetchall()
        if rows:
            print("\nIncome records: ")
            for row in rows:
                print(row)
        else:
            print("No income records found")

    """
    Method calculating the remaining buget
    """

    def calc_rem_budget(self):
        # Get total income
        self.cursor.execute('SELECT SUM(amount) FROM income')
        total_income = self.cursor.fetchone()[0] or 0

        # Get total expense
        self.cursor.execute('SELECT SUM(amount) FROM expense')
        total_expense = self.cursor.fetchone()[0] or 0

        # Calculate remaining budget
        rem_budget = total_income - total_expense
        print(f"\nRemaining Budget: R{rem_budget:.2f}")

    def close_db(self):
        # Closes the connection
        self.conn.close()


"""
Main menu UI and main loop that will run
"""


def main():
    tracker = BudgetTracker()

    while True:
        print(
            "\nBudget Tracker Menu: "
            "\n1. Add Expense"
            "\n2. View Expense"
            "\n3. Add income"
            "\n4. View income"
            "\n5. Calculate remaining budget"
            "\n6. Quit"
        )

        user_choice = input("Enter your choice [1-6]: ")

        if user_choice == "1":
            category = input("Enter expense category: ")
            amount = float(input("Enter amount: "))
            date = input("Enter date [YYYY-MM-DD]: ")
            tracker.add_expense(category, amount, date)
        elif user_choice == '2':
            tracker.view_expenses()
        elif user_choice == "3":
            category = input("Enter income category: ")
            amount = float(input("Enter amount: "))
            date = input("Enter date [YYYY-MM-DD]: ")
            tracker.add_income(category, amount, date)
        elif user_choice == "4":
            tracker.view_income()
        elif user_choice == "5":
            tracker.calc_rem_budget()
        elif user_choice == "6":
            tracker.close_db()
            print("\nQuitting")
            print("Enjoy your day!")
            break
        else:
            print("Invalid choice! Please try again")


if __name__ == "__main__":
    main()
