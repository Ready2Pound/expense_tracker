from collections import defaultdict
import datetime
import json
import os

# -----------------------------------------------------------
# NOTES
# ask user for amount
# ask user for category
# ask for note. optional 

# use datetime.datetime.now().isoformat() to create timestamp
# ------------------------------------------CODE STARTS BELOW------------------------

# -------------------------------------------
# saves added expenses to file
# -------------------------------------------
def save_expense(new_entry):
	# load existing expenses
	if os.path.exists("expenses.json"):
		with open("expenses.json", "r") as file:
			try:
				expenses = json.load(file)
			except json.JSONDecodeError:
				expenses = []
	else:
		expenses = []

	# add new entry
	expenses.append(new_entry)

	# write back to file
	with open("expenses.json", "w") as file:
		json.dump(expenses, file, indent=4)

# ------------------------------------------------------
# saves entire list after modification
# ------------------------------------------------------
def save_expenses(expenses_list):
	with open("expenses.json", "w") as file:
		json.dump(expenses_list, file, indent=4)


# ----------------------------------------------
# gathers, formats, and displays each expense
# ----------------------------------------------

def view_all_expenses():
	if not os.path.exists("expenses.json"):
		print("No expenses found.")
		return

	with open("expenses.json", "r") as file:
		try:
			expenses = json.load(file)
		except json.JSONDecodeError:
			print("Could not read expenses.")
			return

	if not expenses:
		print("No expenses found.")
		return

	print("\n--- All Expenses ---")
	for expense in expenses:
		timestamp = expense.get("timestamp", "")
		amount_value = expense.get("amount", 0)
		try:
    			amount = float(amount_value)
		except (TypeError, ValueError):
    			amount = 0.0

		category = expense.get("category", "N/A")
		note = expense.get("note", "")

	for idx, expense in enumerate(expenses, start=1):
		amount_str = expense['amount']
		amount_num = float(amount_str)
		print(f"{idx}. ${amount_num:.2f} - {expense['category'].capitalize()} on {expense['timestamp']} Note: {expense['note']}")

		#print(f"{timestamp[:10]} | {(' $' + f'{amount:.2f}'):>8} | {category.ljust(12).capitalize()} | {note}")

# ----------------------
# main loop 
# ---------------------- 

def main():
	while True:
		print("\n==== Smart Expense Tracker ====")
		print("1. Add a new expense")
		print("2. View all expenses")
		print("3. View totals by category")
		print("4. Filter expenses by date range")
		print("5. Delete expenses")
		print("6. Quit")

		choice = input("\nEnter your choice (1-5): ")

		if choice == "1":
			add_expense_flow()
		elif choice == "2":
			view_all_expenses()
		elif choice == "3":
			view_totals_by_category()
		elif choice == "4":
			view_expenses_by_date_range()
		elif choice == "5":
			delete_expenses()
		elif choice == "6":
			print("Goodbye.")
			exit()
		else:
			print("Invalid choice. Please choose a number from the menu.")
			return()

# -------------------------
# views totals by category	
# -------------------------

def view_totals_by_category():
	if not os.path.exists("expenses.json"):
		print("No expenses found.")
		return

	with open("expenses.json", "r") as file:
		try:
			expenses = json.load(file)
		except json.JSONDecodeError:
			print("Could not read expenses.")
			return

	category_totals = defaultdict(float)
	
	for expense in expenses:
		amount_value = expense.get("amount", 0)
		try:
    			amount = float(amount_value)
		except (TypeError, ValueError):
    			amount = 0.0

		category = expense.get("category", "Uncategorized")

		category_totals[category] += amount

	print("\n--- Totals by Category ---")
	for category, total in category_totals.items():
		print(f"{category.ljust(15)} : ${total:.2f}")

# ---------------------------------
# filter by date range
# ---------------------------------
def view_expenses_by_date_range():
	start_input = input("Enter a start date (YYYY-MM-DD): ")
	end_input = input("Enter an end date (YYYY-MM-DD): ")

	try:
		start_date = datetime.datetime.strptime(start_input, "%Y-%m-%d").date()
		end_date = datetime.datetime.strptime(end_input, "%Y-%m-%d").date()
	except json.JSONDecodeError:
		print("Invalid date format.")
		return

	if not os.path.exists("expenses.json"):
		print("No expenses found.")
		return

	with open("expenses.json", "r") as file:
		try:
			expenses = json.load(file)
		except json.JSONDecodeError:
			print("Could not read expenses.")
			return

	print(f"\n--- Expenses from {start_date} to {end_date} ---")
	filtered = []

	for expense in expenses:
		try:
			timestamp = expense.get("timestamp", "")
			expense_date = datetime.datetime.fromisoformat(timestamp).date()
		except ValueError:
			continue

		if start_date <= expense_date <= end_date:
			filtered.append(expense)

		if not filtered:
			print("No expenses in that date range.")
			return

		for expense in filtered:
			date = expense["timestamp"][:10]
			try:
    				amount_value = expense['amount']
    				amount_num = float(amount_value)
			except (TypeError, ValueError):
				amount_num = 0.0
			amount = f"${amount_num:.2f}".rjust(8)
			category = expense["category"].ljust(12)
			note = expense.get("note", "")
			print(f"{date} | {amount} | {category} | {note}")

# -------------------------
# delete expenses
# -------------------------
def delete_expenses():
	if not os.path.exists("expenses.json"):
		print("No expenses found.")
		return

	with open("expenses.json", "r") as file:
		try:
			expenses = json.load(file)
		except json.JSONDecodeError:
			print("Could not read expenses.")
			return

	if not expenses:
		print("No expenses found.")
		return

	# display all expenses in numbered list
	print("\nExpenses:")
	
	for idx, expense in enumerate(expenses, start=1):
		amount_str = expense['amount']
		amount_num = float(amount_str)
		print(f"{idx}. ${amount_num:.2f} - {expense['category']} on {expense['timestamp']} Note: {expense['note']}")

	# prompt user to select a choice
	while True:
		try:
			choice = int(input("\nPlease choose an expense to delete from the numbered options above: "))
			if choice < 1 or choice > len(expenses):
				print("Invalid choice. Please choose an option from the list.")
			else:
				break 		#valid choice, exit loop
		except ValueError: 		#this line catches cases like pressing Enter or entering a non integer value
			print("Invalid input. Please enter a number from the choices above.")
	
	# display choice selection
	delete_choice = expenses[choice - 1]
	print(f"\nYou selected:")
	print(f"Amount: ${delete_choice['amount']:.2f}")
	print(f"Category: {delete_choice['category'].capitalize()}")
	print(f"Note: {delete_choice['note']}")
	print(f"Timestamp: {delete_choice['timestamp']}") 	
	
	# confirm expense deletion and normalization
	confirm = input(f"\nAre you sure you want to delete this expense? Yes or no? ").lower()
	if confirm in ("yes", "y"):
		expenses.pop(choice - 1)
		save_expenses(expenses)
		print("Expense deleted successfully")
	else:
		print("\nDeletion cancelled.")

	# delete the expense
	 

# ----------------------------------------
# collect user input and write to file
# ----------------------------------------
def add_expense_flow():
	amount_input = input("Enter the amount spent: ")
	category_input = input("Enter the category (e.g., food, transport, etc.): ")
	note_input = input("Enter a note. (Optional): ")

	# normalize category input to lowercase
	category_input = category_input.strip().lower()

	# set default note value if none added
	if not note_input.strip():
		note_input = "N/A"

	# try to convert amount to float
	try:
		amount = float(amount_input)
	except ValueError:
		print("Invalid amount. Please enter a number.")
		exit()

	# create the dictionary entry
	new_expense = {
		"amount": amount,
		"category": category_input,
		"note": note_input,
		"timestamp": datetime.datetime.now().isoformat()
	}

	save_expense(new_expense)
	print("Expense saved successfully")

if __name__ == "__main__":
	main()
