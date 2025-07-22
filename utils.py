from supabase_client import supabase
from datetime import datetime

# ➕ Add new expense
def add_expense(amount, category, note=""):
    data = {
        "amount": amount,
        "category": category,
        "note": note,
        "date": datetime.now().isoformat()
    }
    return supabase.table("expenses").insert(data).execute()

# 📋 Read all expenses
def get_expenses():
    res = supabase.table("expenses").select("*").order("date", desc=True).execute()
    return res.data

# ✏️ Update existing expense
def update_expense(expense_id, amount, category, note):
    return supabase.table("expenses").update({
        "amount": amount,
        "category": category,
        "note": note
    }).eq("id", expense_id).execute()

# 🗑️ Delete an expense
def delete_expense(expense_id):
    return supabase.table("expenses").delete().eq("id", expense_id).execute()
