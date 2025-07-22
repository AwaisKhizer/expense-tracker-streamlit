import streamlit as st
from utils import add_expense, get_expenses, update_expense, delete_expense
import pandas as pd

st.set_page_config(page_title="💰 Expense Tracker", layout="centered")

# 🔐 Admin login (for now, dummy)
st.sidebar.title("🔐 Admin Login")
password = st.sidebar.text_input("Enter Password", type="password")
if password != "admin123":
    st.warning("Enter password to access the expense tracker.")
    st.stop()

st.title("💸 Expense Tracker (Full CRUD)")

# ➕ Add new expense
st.subheader("➕ Add New Expense")
with st.form("add_expense_form"):
    amount = st.number_input("Amount", min_value=0.0)
    category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Utilities", "Other"])
    note = st.text_input("Note")
    submit_btn = st.form_submit_button("Add Expense")
    if submit_btn:
        res = add_expense(amount, category, note)
        if res.data:
            st.success("✅ Expense added!")

# 📋 View all expenses
st.subheader("📋 All Expenses")
expenses = get_expenses()

if expenses:
    df = pd.DataFrame(expenses)
    df['date'] = pd.to_datetime(df['date'])
    st.dataframe(df[['id', 'amount', 'category', 'note', 'date']])

    # ✏️ Edit or 🗑️ Delete Section
    st.subheader("✏️ Update / 🗑️ Delete Expense")
    ids = df['id'].tolist()
    selected_id = st.selectbox("Select Expense ID to Edit or Delete", ids)

    selected_row = df[df['id'] == selected_id].iloc[0]

    with st.form("update_form"):
        new_amount = st.number_input("New Amount", value=selected_row['amount'])
        new_category = st.selectbox("New Category", ["Food", "Transport", "Shopping", "Utilities", "Other"], index=["Food", "Transport", "Shopping", "Utilities", "Other"].index(selected_row['category']))
        new_note = st.text_input("New Note", value=selected_row['note'])

        update_btn = st.form_submit_button("Update Expense")
        if update_btn:
            res = update_expense(selected_id, new_amount, new_category, new_note)
            if res.data:
                st.success("✅ Expense updated!")

    if st.button("🗑️ Delete This Expense"):
        res = delete_expense(selected_id)
        if res.data:
            st.warning(f"❌ Expense ID {selected_id} deleted!")

else:
    st.info("No expenses to show.")
