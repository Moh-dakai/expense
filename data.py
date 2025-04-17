import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt
import streamlit as st

# File paths
EXPENSES_FILE = "expenses.csv"
INCOME_FILE = "income.csv"

# Load expense data
def load_data():
    if os.path.exists(EXPENSES_FILE):
        return pd.read_csv(EXPENSES_FILE)
    return pd.DataFrame(columns=["Amount", "Category", "Note", "Date", "Description"])

# Load income data
def load_income_data():
    if os.path.exists(INCOME_FILE):
        return pd.read_csv(INCOME_FILE)
    return pd.DataFrame(columns=["Month", "Income"])

# Save expense data
def save_data(df):
    df.to_csv(EXPENSES_FILE, index=False)

# Save income data
def save_income_data(df):
    df.to_csv(INCOME_FILE, index=False)

# Validate input before adding
def validate_expense(amount, category, description, date):
    if amount <= 0 or not category or not date:
        return False
    return True

# Add new expense
def add_expense(amount, category, note="", date=None, description=""):
    date = date or datetime.now().strftime("%Y-%m-%d")
    if not validate_expense(amount, category, description, date):
        return False, "Validation failed. Please check input values."

    try:
        df = load_data()
        new_row = pd.DataFrame([{
            "Amount": float(amount),
            "Category": category,
            "Note": note,
            "Date": date,
            "Description": description
        }])
        df = pd.concat([df, new_row], ignore_index=True)
        save_data(df)
        return True, "Expense added successfully!"
    except Exception as e:
        return False, f"Error adding expense: {e}"

# Add or update monthly income
def add_income(month, income):
    try:
        df = load_income_data()
        month = str(month)
        income = float(income)
        if month in df["Month"].values:
            df.loc[df["Month"] == month, "Income"] = income
        else:
            new_row = pd.DataFrame([{"Month": month, "Income": income}])
            df = pd.concat([df, new_row], ignore_index=True)
        save_income_data(df)
        return True, "Income added successfully!"
    except Exception as e:
        return False, f"Error adding income: {e}"

# Summary statistics
def get_summary_stats():
    df = load_data()
    if df.empty:
        return None
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    total_spent = df["Amount"].sum()
    average_spending = df["Amount"].mean()
    daily_average = df.groupby(df["Date"].dt.date)["Amount"].sum().mean()
    category_counts = df["Category"].value_counts().to_dict()

    return {
        "total_spent": total_spent,
        "average_spending": average_spending,
        "daily_average": daily_average,
        "category_counts": category_counts,
    }

# Monthly breakdown
def get_monthly_breakdown():
    df = load_data()
    if df.empty:
        return {}
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    monthly_totals = df.groupby("Month")["Amount"].sum().to_dict()
    return monthly_totals

# Monthly income breakdown
def get_monthly_income_breakdown():
    df = load_income_data()
    if df.empty:
        return {}
    df["Income"] = pd.to_numeric(df["Income"], errors="coerce")
    monthly_income = df.set_index("Month")["Income"].to_dict()
    return monthly_income

# Trend line chart
def plot_monthly_trend():
    expenses = get_monthly_breakdown()
    income = get_monthly_income_breakdown()

    all_months = sorted(set(expenses.keys()).union(income.keys()))
    expense_vals = [expenses.get(m, 0) for m in all_months]
    income_vals = [income.get(m, 0) for m in all_months]

    fig, ax = plt.subplots()
    ax.plot(all_months, income_vals, marker='o', label="Income", color="green")
    ax.plot(all_months, expense_vals, marker='o', label="Expenses", color="red")
    ax.set_title("Monthly Income vs Expenses")
    ax.set_xlabel("Month")
    ax.set_ylabel("Amount")
    ax.legend()
    st.pyplot(fig)

# Pie chart by category
def plot_pie_chart():
    df = load_data()
    if df.empty:
        st.info("No data to display pie chart.")
        return
    pie_data = df.groupby("Category")["Amount"].sum()
    fig, ax = plt.subplots()
    ax.pie(pie_data, labels=pie_data.index, autopct="%1.1f%%", startangle=90)
    ax.set_title("Spending by Category")
    ax.axis("equal")
    st.pyplot(fig)

# Function to get spending for the current month
def get_monthly_spending(year, month):
    df = load_data()
    if df.empty:
        return 0
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    monthly_df = df[(df["Date"].dt.year == year) & (df["Date"].dt.month == month)]
    return monthly_df["Amount"].sum()