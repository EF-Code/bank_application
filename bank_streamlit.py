import streamlit as st
from bank import SavingsAccount, CurrentAccount

if "account" not in st.session_state:
    st.session_state.account_type = None
    st.session_state.account = None

st.sidebar.title("🏦 World Bank")
menu = st.sidebar.radio("Select Action", ["Create Account", "Deposit", "Withdraw", "View Balance"])

st.title("💳 World Bank!")

if menu == "Create Account":
    st.subheader("Create New Account")
    name = st.text_input("Account Holder Name")
    acc_number = st.text_input("Account Number")
    acc_type = st.selectbox("Account Type", ["Savings", "Current"])
    initial_balance = st.number_input("Initial Deposit", min_value=0)

    if st.button("Create Account"):
        if acc_type == "Savings":
            st.session_state.account = SavingsAccount(acc_number, name, initial_balance)
        else:
            st.session_state.account = CurrentAccount(acc_number, name, initial_balance)
        st.session_state.account_type = acc_type
        st.success(f"{acc_type} Account created for {name} with balance {initial_balance}.")
