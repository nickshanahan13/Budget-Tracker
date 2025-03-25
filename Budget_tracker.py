#!/usr/bin/env python3

import sys


class BudgetManager:
    def __init__(self, amount):
        self.available = amount
        self.budgets = {}
        self.expenditure = {}

    def add_budget(self, name, amount):
        if name in self.budgets:
            raise ValueError("Budget exists")
        if amount > self.available:
            raise ValueError("Insufficient funds")
        self.budgets[name] = amount
        self.available -= amount
        self.expenditure[name] = []
        return self.available
    

    def change_budget(self, name, new_amount):
        if name not in self.budgets:
            raise ValueError("Budget does not exist")
        old_amount = self.budgets[name]
        if new_amount > old_amount + self.available:
            raise ValueError("Insufficient funds")
        self.budgets[name] = new_amount
        self.available -= new_amount - old_amount
        return self.available
    
    def spend(self, name, amount):
        if name not in self.expenditure:
            raise ValueError("No such budget")
        self.expenditure[name].append(amount)
        budgeted = self.budgets[name]
        spent = sum(self.expenditure[name])
        return budgeted - spent

    def print_summary(self):
        print("Budget           Budgeted    Spent    Remaining")
        print("--------------- ---------- ---------- ----------")
        total_budgeted = 0
        total_spent = 0
        total_remaining = 0
        for name in self.budgets:
            budgeted = self.budgets[name]
            spent = sum(self.expenditure[name])
            remaining = budgeted - spent
            print(f"{name:15s} {budgeted:10.2f} {spent:10.2f} {remaining:10.2f}")
            total_budgeted += budgeted
            total_spent += spent
            total_remaining += remaining
        print("--------------- ---------- ---------- ----------")
        print(f'{"Total":15s} {total_budgeted: 10.2f} {total_spent:10.2f} '
                f'{total_budgeted - total_spent: 10.2f}')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: budget_manager.py <initial_amount> [command] [arguments]")
        sys.exit(1)

    try:
        initial_amount = float(sys.argv[1])
        budget_manager = BudgetManager(initial_amount)

        if len(sys.argv) > 2:
            command = sys.argv[2]
            args = sys.argv[3:]

            if command == "add":
                if len(args) != 2:
                    print("Usage: budget_manager.py <initial_amount> add <name> <amount>")
                else:
                    name = args[0]
                    amount = float(args[1])
                    try:
                        remaining = budget_manager.add_budget(name, amount)
                        print(f"Budget '{name}' added. Remaining funds: {remaining:.2f}")
                    except ValueError as e:
                        print(f"Error: {e}")

            elif command == "change":
                if len(args) != 2:
                    print("Usage: budget_manager.py <initial_amount> change <name> <new_amount>")
                else:
                    name = args[0]
                    new_amount = float(args[1])
                    try:
                        remaining = budget_manager.change_budget(name, new_amount)
                        print(f"Budget '{name}' changed. Remaining funds: {remaining:.2f}")
                    except ValueError as e:
                        print(f"Error: {e}")

            elif command == "spend":
                if len(args) != 2:
                    print("Usage: budget_manager.py <initial_amount> spend <name> <amount>")
                else:
                    name = args[0]
                    amount = float(args[1])
                    try:
                        remaining = budget_manager.spend(name, amount)
                        print(f"Spent {amount:.2f} on '{name}'. Remaining budget: {remaining:.2f}")
                    except ValueError as e:
                        print(f"Error: {e}")

            elif command == "summary":
                budget_manager.print_summary()

            else:
                print("Invalid command. Available commands: add, change, spend, summary")

        else:
            print("Initial budget manager created.")
            budget_manager.print_summary() #Prints the summary of the initialized budget.

    except ValueError:
        print("Error: Invalid number format for initial amount or command arguments.")
        sys.exit(1)