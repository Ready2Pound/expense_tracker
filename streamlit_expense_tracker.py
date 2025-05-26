import streamlit as st
import json
import os 
import datetime
from collections import defaultdict

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
menu = st.sidebar.radio("Navigate", ["Add Expense", "View All Expenses", "Totals by Category", "Filter by Date"]) 
st.write("Welcome to your upgraded tracker!")

# ----------------
# Add expense section
# ----------------

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

# -----------------------
# View expenses section
# -----------------------

if menu == "View All Expenses":
    st.header("All Expenses")

    expenses = load_expenses()

    if not expenses:
        st.info("No expenses found.")
    else:
        for idx, e in enumerate(expenses, start=1):
            st.markdown(f"""
                **{idx}. ${float(e['amount']):.2f} - {e['category'].capitalize()}**
                - {e['timestamp'][:10]}
                - {e['note']}
                ---
            """)

# ----------------------------
# Totals by category section
# ----------------------------

if menu == "Totals by Category":
        
    st.header("Totals by Category")
    if os.path.exists("expenses.json"):
        with open("expenses.json", "r") as file:
            try:
                expenses = json.load(file)
            except json.JSONDecodeError:
                st.error("Could not read expenses.")
                expenses = []
    else:
        st.warning("No expenses file found.")
        expenses = []

    if not expenses:
        st.info("No expenses to summarize.")
    else:
        # Use defaultdict to automatically sum values
        category_totals = defaultdict(float)
        for expense in expenses:
            try:
                amount = float(expense["amount"])
                category = expense["category"].capitalize()
                category_totals[category] += amount
            except (TypeError, ValueError):
                continue
        
        # Display totals as text
        for category, total in category_totals.items():
                st.write(f"**{category}**: ${total:.2f}")

        # Display as bar chart
        #df = pd.DataFrame(category_totals.items(), columns=["Category", "Total"])
        #df = df.set_index("Category")
        #st.subheader("Category Breakdown")
        #st.bar_chart(df)

# ----------------------------
# Filter by date section
# ----------------------------
        
if menu == "Filter by Date":
    st.header("Filter by Date")

    if os.path.exists("expenses.json"):
        with open("expenses.json", "r") as file:
            try:
                expenses = json.load(file)
                st.write("Able to read expenses successfully")
            except json.JsonDecodeError:
                st.write("Could not read expenses")
                expenses = []

    else:
            st.warning("No expenses found.")
            expenses = []

    if not expenses
        st.info("No expenses to summarize")
    else:
        #prompt user to pick a start date in a specific format
        #prompt user to pick an end date in a specific format
        #gather all entries between those dates
        #print all those entries











