import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

# ---------------- DB Connection ----------------
def get_db():
    conn = sqlite3.connect("bank_system.db")
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

# ---------------- DB Operations ----------------
def login(username, password):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT Role FROM Login_Info WHERE Username=? AND Password=?", (username, password))
    data = cur.fetchone()
    conn.close()
    return data[0] if data else None

def create_account(branch_no, name, gender, dob, address, phone, email, balance):
    conn = get_db()
    conn.execute("""
        INSERT INTO Account_Info (Branch_No, Name, Gender, DOB, Address, Phone, Email, Balance)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (branch_no, name, gender, dob, address, phone, email, balance))
    conn.commit()
    conn.close()

def get_accounts():
    conn = get_db()
    df = pd.read_sql_query("SELECT * FROM Account_Info", conn)
    conn.close()
    return df

def search_account(acc_no):
    conn = get_db()
    df = pd.read_sql_query("SELECT * FROM Account_Info WHERE Account_No = ?", conn, params=(acc_no,))
    conn.close()
    return df

def deposit(account_no, amount):
    conn = get_db()
    conn.execute("INSERT INTO Deposit_Info (Account_No, Amount) VALUES (?, ?)", (account_no, amount))
    conn.execute("UPDATE Account_Info SET Balance = Balance + ? WHERE Account_No = ?", (amount, account_no))
    conn.commit()
    conn.close()

def withdraw(account_no, amount):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT Balance FROM Account_Info WHERE Account_No = ?", (account_no,))
    bal = cur.fetchone()
    if not bal:
        st.error("Account not found.")
        return
    if bal[0] < amount:
        st.error("Insufficient balance.")
        return
    conn.execute("INSERT INTO Withdrawal_Info (Account_No, Amount) VALUES (?, ?)", (account_no, amount))
    conn.execute("UPDATE Account_Info SET Balance = Balance - ? WHERE Account_No = ?", (amount, account_no))
    conn.commit()
    conn.close()

def get_transaction_history(account_no):
    conn = get_db()
    dep = pd.read_sql_query("SELECT Amount, Deposit_Date AS Date, 'Deposit' AS Type FROM Deposit_Info WHERE Account_No=?", conn, params=(account_no,))
    wit = pd.read_sql_query("SELECT Amount, Withdrawal_Date AS Date, 'Withdrawal' AS Type FROM Withdrawal_Info WHERE Account_No=?", conn, params=(account_no,))
    conn.close()
    return pd.concat([dep, wit]).sort_values(by="Date", ascending=False)

# ---------------- Streamlit Setup ----------------
st.set_page_config(page_title="Bank Management System", layout="wide")

# Persistent login state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None
if "username" not in st.session_state:
    st.session_state.username = None

# ---------------- LOGIN PAGE ----------------
if not st.session_state.logged_in:
    st.title("🏦 Secure Bank Management System")
    st.markdown("### 🔐 Admin / Staff Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        role = login(user, pwd)
        if role:
            st.session_state.logged_in = True
            st.session_state.role = role
            st.session_state.username = user
            st.success(f"✅ Welcome, {user} ({role})")
            st.rerun()
        else:
            st.error("Invalid username or password")

# ---------------- MAIN DASHBOARD ----------------
else:
    st.sidebar.title(f"Welcome, {st.session_state.username}")
    st.sidebar.write(f"**Role:** {st.session_state.role}")

    menu = [
        "🏠 Dashboard",
        "➕ Create Account",
        "💰 Deposit",
        "💸 Withdraw",
        "🔍 Search Account",
        "📜 Transaction History",
        "📊 View All Accounts",
        "🚪 Logout"
    ]
    choice = st.sidebar.radio("Navigate", menu)

    st.markdown("<hr>", unsafe_allow_html=True)

    # -------- DASHBOARD --------
    if choice == "🏠 Dashboard":
        st.title("📋 Bank Dashboard")
        df = get_accounts()
        total_balance = df["Balance"].sum() if not df.empty else 0
        col1, col2 = st.columns(2)
        col1.metric(label="Total Accounts", value=len(df))
        col2.metric(label="Total Deposits (₹)", value=f"{total_balance:,.2f}")
        st.markdown("---")
        st.info("Use the sidebar to perform operations like creating accounts, deposits, withdrawals, or searching customer details.")

    # -------- CREATE ACCOUNT --------
    elif choice == "➕ Create Account":
        st.header("🧾 Open New Account")
        col1, col2 = st.columns(2)
        with col1:
            branch_no = st.text_input("Branch No", "B001")
            name = st.text_input("Full Name")
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            dob = st.date_input("Date of Birth", date(2000, 1, 1))
        with col2:
            address = st.text_area("Address")
            phone = st.text_input("Phone")
            email = st.text_input("Email")
            balance = st.number_input("Opening Balance", min_value=0.0, value=0.0, step=100.0)

        if st.button("Create Account"):
            if name and branch_no:
                create_account(branch_no, name, gender, dob, address, phone, email, balance)
                st.success(f"✅ Account created successfully for {name}!")
            else:
                st.error("Please fill in all required fields.")

    # -------- DEPOSIT --------
    elif choice == "💰 Deposit":
        st.header("Deposit Money")
        account_no = st.number_input("Account No", min_value=1, step=1)
        amount = st.number_input("Amount", min_value=0.0, step=100.0)
        if st.button("Deposit"):
            deposit(account_no, amount)
            st.success(f"✅ Deposited ₹{amount:.2f} to Account #{account_no}")

    # -------- WITHDRAW --------
    elif choice == "💸 Withdraw":
        st.header("Withdraw Money")
        account_no = st.number_input("Account No", min_value=1, step=1)
        amount = st.number_input("Amount", min_value=0.0, step=100.0)
        if st.button("Withdraw"):
            withdraw(account_no, amount)
            st.success(f"✅ Withdrawn ₹{amount:.2f} from Account #{account_no}")

    # -------- SEARCH ACCOUNT --------
    elif choice == "🔍 Search Account":
        st.header("Search Customer Account")
        acc_no = st.number_input("Enter Account Number", min_value=1, step=1)
        if st.button("Search"):
            df = search_account(acc_no)
            if df.empty:
                st.warning("No account found with that number.")
            else:
                st.dataframe(df)

    # -------- TRANSACTION HISTORY --------
    elif choice == "📜 Transaction History":
        st.header("Transaction History")
        account_no = st.number_input("Enter Account Number", min_value=1, step=1)
        if st.button("View History"):
            df = get_transaction_history(account_no)
            if df.empty:
                st.warning("No transactions found for this account.")
            else:
                st.dataframe(df)

    # -------- VIEW ALL ACCOUNTS --------
    elif choice == "📊 View All Accounts":
        st.header("All Customer Accounts")
        df = get_accounts()
        st.dataframe(df)

    # -------- LOGOUT --------
    elif choice == "🚪 Logout":
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.role = None
        st.success("Logged out successfully.")
        st.rerun()
