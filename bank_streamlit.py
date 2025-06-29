import streamlit as st
from bank import SavingsAccount, CurrentAccount
import pandas as pd
from datetime import datetime
import altair as alt

if "account" not in st.session_state:
    st.session_state.account_type = None
    st.session_state.account = None
    st.session_state.transactions = []

def add_transaction(action, amount):
    st.session_state.transactions.append({
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Action": action,
        "Amount (₦)": amount,
        "Balance (₦)": st.session_state.account.balance
    })

st.set_page_config(page_title="World Bank 💰", page_icon="🏦")
st.sidebar.title("🏦 World Bank")
menu = st.sidebar.radio("📋 Menu", ["🏁 Create Account", "📊 Dashboard", "💸 Deposit", "🏧 Withdraw", "📈 History", "🚪 Logout"])

st.title("💳 World Bank!")

if menu == "🚪 Logout":
    st.session_state.account = None
    st.session_state.transactions = []
    st.session_state.account_type = None
    st.success("You have been logged out.")

if menu == "🏁 Create Account":
    st.subheader("🆕 Open New Account")
    name = st.text_input("Full Name")
    acc_number = st.text_input("Account Number")
    acc_type = st.selectbox("Account Type", ["Savings", "Current"])
    initial_balance = st.number_input("Initial Deposit (₦)", min_value=0)

    if st.button("Create Account"):
        if acc_type == "Savings":
            st.session_state.account = SavingsAccount(acc_number, name, initial_balance)
        else:
            st.session_state.account = CurrentAccount(acc_number, name, initial_balance)
        st.session_state.account_type = acc_type
        add_transaction("Initial Deposit", initial_balance)
        st.success(f"{acc_type} Account created for {name} with ₦{initial_balance:.2f}.")

elif menu == "📊 Dashboard":
    if st.session_state.account:
        acc = st.session_state.account
        st.subheader("👤 Account Summary")
        st.markdown(f"**Name:** {acc.holder_name}")
        st.markdown(f"**Account No:** {acc.account_number}")
        st.markdown(f"**Account Type:** {st.session_state.account_type}")
        st.markdown(f"**Current Balance:** ₦{acc.balance:.2f}")
    else:
        st.warning("Please create or log into an account.")

elif menu == "💸 Deposit":
    if st.session_state.account:
        st.subheader("💰 Make a Deposit")
        amount = st.number_input("Amount to deposit (₦)", min_value=1)
        if st.button("Deposit"):
            result = st.session_state.account.deposit(amount)
            add_transaction("Deposit", amount)
            st.success(result)
    else:
        st.warning("Please create or log into an account.")


elif menu == "🏧 Withdraw":
    if st.session_state.account:
        st.subheader("💳 Withdraw Funds")
        amount = st.number_input("Amount to withdraw (₦)", min_value=1)
        if st.button("Withdraw"):
            result = st.session_state.account.withdraw(amount)
            if "Withdrew" in result:
                add_transaction("Withdraw", amount)
            st.success(result)
    else:
        st.warning("Please create or log into an account.")


elif menu == "📈 History":
    if st.session_state.account:
        st.subheader("📜 Transaction History")

        if len(st.session_state.transactions) > 0:
            df = pd.DataFrame(st.session_state.transactions)

            st.dataframe(df, use_container_width=True)

            chart = alt.Chart(df).mark_line(point=True).encode(
                x='Time',
                y='Balance (₦)',
                color=alt.value("#008000")
            ).properties(title="Balance Over Time")
            st.altair_chart(chart, use_container_width=True)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Export CSV", csv, "transaction_history.csv", "text/csv", key='download-csv')

        else:
            st.info("No transaction history yet.")
    else:
        st.warning("Please create or log into an account.")
