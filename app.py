# app.py
import streamlit as st
import pandas as pd
from datetime import datetime

from data import (
    add_expense, add_income, load_data, load_income_data,
    get_summary_stats, get_monthly_breakdown, get_monthly_income_breakdown,
    plot_monthly_trend, plot_pie_chart, get_monthly_spending
)

st.set_page_config(page_title="Expense Tracker", layout="wide")

# Sidebar
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>NairaGhibli</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Track with Naija flavor & Giribli calm</p>", unsafe_allow_html=True)
    st.markdown("---")
    navigation_option = st.radio("Navigation", ["Dashboard", "Add Expense", "Analytics", "Savings Health", "Budgets"])
    st.markdown("---")
    st.markdown("<p style='font-style: italic; text-align: center;'>\"Small daily savings grow like the badbab free.\" - Nigerian Proverb</p>", unsafe_allow_html=True)

    st.subheader("Monthly Income")
    with st.form("income_form"):
        income_month = st.text_input("Month (YYYY-MM)")
        income_amt = st.number_input("Income Amount", min_value=0.0)
        income_submitted = st.form_submit_button("Save Income")
        if income_submitted:
            success, msg = add_income(income_month, income_amt)
            st.success(msg) if success else st.error(msg)

# Main Area
st.markdown("<h1 style='text-align: center;'>Financial Dashboard</h1>", unsafe_allow_html=True)

if navigation_option == "Dashboard":
    # Display Summary
    st.subheader("Summary Statistics")
    summary = get_summary_stats()
    if summary:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Spent", f"₦{summary['total_spent']:.2f}")
        col2.metric("Average Spending", f"₦{summary['average_spending']:.2f}")
        col3.metric("Daily Average", f"₦{summary['daily_average']:.2f}")
        col4.metric("Top Category", max(summary['category_counts'], key=summary['category_counts'].get))
    else:
        st.info("No expenses yet. Add some to view stats.")

    st.markdown("---")

    # Monthly Overview
    st.subheader("Monthly Overview")
    col_exp_mo, col_inc_mo = st.columns(2)
    with col_exp_mo:
        st.markdown("### Expenses")
        expense_df = pd.DataFrame.from_dict(get_monthly_breakdown(), orient='index', columns=["Total Spent"])
        st.bar_chart(expense_df)

    with col_inc_mo:
        st.markdown("### Income")
        income_df = pd.DataFrame.from_dict(get_monthly_income_breakdown(), orient='index', columns=["Total Income"])
        st.bar_chart(income_df)

    st.markdown("---")

    # Transaction History
    st.subheader("All Transactions")
    data = load_data()
    if not data.empty:
        st.dataframe(data)
    else:
        st.info("No expense data found.")

elif navigation_option == "Add Expense":
    st.subheader("Add New Expense")
    with st.form("expense_form_main"):
        amount = st.number_input("Amount", min_value=0.01, step=0.01)
        category = st.text_input("Category")
        note = st.text_input("Note (optional)")
        date = st.date_input("Date")
        description = st.text_input("Description")  # Added description input
        submitted = st.form_submit_button("Add Expense")
        if submitted:
            success, msg = add_expense(amount, category, note, date.strftime("%Y-%m-%d"), description)
            st.success(msg) if success else st.error(msg)

elif navigation_option == "Analytics":
    st.subheader("Expense Breakdown")

    st.subheader("Monthly Expenses")
    monthly_breakdown = get_monthly_breakdown()
    if monthly_breakdown:
        expense_df_analytics = pd.DataFrame.from_dict(monthly_breakdown, orient='index', columns=["Total Spent"])
        st.bar_chart(expense_df_analytics)
    else:
        st.info("No expense data available for monthly breakdown.")

    st.subheader("Spending by Category")
    plot_pie_chart()

elif navigation_option == "Savings Health":
    st.subheader("Savings Health")
    st.write("Content for Savings Health will go here.")

elif navigation_option == "Budgets":
    st.subheader("Budgets")
    st.write("Content for Budgets will go here.")