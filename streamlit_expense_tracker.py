import streamlit as st
import json
import os 
import datetime

# -----------------------------------
# Load existing expenses
# -----------------------------------

def load_expenses():
	if os.path.exists("expenses.json"):
		with open("expenses.json", "r") as f:
			try:
				return json.load(f)
			except json.JSONDecodeError:
				return []
	return []

# --------------------------------
# Save expenses to file
# --------------------------------

def save_expenses(expenses):
	with open("expenses.json", "w") as f:
		json.dump(expenses, f, indent=4)

# ---------------------------------------
# Streamlit app starts here
# ---------------------------------------

st.title("Smart Expense Tracker")
menu = st.sidebar.radio("Navigate", ["Add Expense", "View All Expenses"]) 
st.write("Welcome to your upgraded tracker!")

if menu == "Add Expense":
	st.header("Add an expense")
	
	amount = st.number_input("Amount Spent", min_value=0.01, step=0.01)
	category = st.text_input("Category (e.g., food, transport)")
	note = st.text_area("Note (optional)")
	submit = st.button("Save Expense")

	if submit:
		new_expense = {
			"amount": amount,
			"category": category.strip().lower(),
			"note": note.strip() if note else "N/A",
			"timestamp": datetime.datetime.now().isoformat()
		}

		expenses = load_expenses()
		expenses.append(new_expense)
		save_expenses(expenses)
	
		st.success("Expense saved successfully!")