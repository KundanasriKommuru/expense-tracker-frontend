
import streamlit as st
import requests
import pandas as pd


SERVER = st.secrets["backend_server_url"]

st.title("Expense Tracker App")

menu = st.sidebar.selectbox(
    "Choose Option",
    [
        "Add Expense",
        "View Expenses",
        "Delete Expense",
        "Update Expense"
    ]
)


# Add Expense
if menu == "Add Expense":

    st.header("Add Expense")

    title = st.text_input("Expense Title")

    amount = st.number_input(
        "Expense Amount",
        min_value=1
    )

    category = st.selectbox(
        "Category",
        ["Food", "Travel", "Shopping", "Bills", "Other"]
    )

    expense_date = st.date_input("Expense Date")

    if st.button("Add Expense"):

        data = {
            "title": title,
            "amount": amount,
            "category": category,
            "expense_date": str(expense_date)
        }

        response = requests.post(
            f"{SERVER}/add_expense",
            json=data
        )

        st.success(response.json()["message"])


# View Expenses
elif menu == "View Expenses":

    st.header("All Expenses")

    response = requests.get(
        f"{SERVER}/get_expenses"
    )

    data = response.json()["expenses"] # list of dict 
    # st.write(data)
    if data:

        df = pd.DataFrame(data)

        st.dataframe(df)

        total = df["amount"].sum()

        st.subheader(f"Total Expense: ₹ {total}")

    else:
        st.warning("No Expenses Found")


# Delete Expense
elif menu == "Delete Expense":

    st.header("Delete Expense")

    expense_id = st.number_input(
        "Enter Expense ID",
        min_value=1,
        step=1
    )

    if st.button("Delete"):

        response = requests.delete(
            f"{SERVER}/delete_expense/{expense_id}"
        )

        st.success(response.json()["message"])


# Update Expense
elif menu == "Update Expense":

    st.header("Update Expense")

    expense_id = st.number_input(
        "Expense ID",
        min_value=1,
        step=1
    )

    title = st.text_input("New Title")

    amount = st.number_input(
        "New Amount",
        min_value=1
    )

    category = st.selectbox(
        "New Category",
        ["Food", "Travel", "Shopping", "Bills", "Other"]
    )

    expense_date = st.date_input("New Expense Date")

    if st.button("Update Expense"):

        data = {
            "title": title,
            "amount": amount,
            "category": category,
            "expense_date": str(expense_date)
        }

        response = requests.put(
            f"{SERVER}/update_expense/{expense_id}",
            json=data
        )

        st.success(response.json()["message"])
