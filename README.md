
# 🏦 BANK MANAGEMENT SYSTEM (SQLite + Streamlit)

### Developer: *Gaurav Pandit (Open Book Boss)*

### Tech Stack: Python | SQLite | Streamlit | Pandas

---

## 🚀 1. Project Overview

This is a **Bank Management System** built using **Python (Streamlit)** with **SQLite** as the backend database.
It allows admin/staff users to:

* Create new bank accounts
* Deposit and withdraw money
* View all customer accounts
* Search for accounts by account number
* Check transaction history
* Securely log in and log out

It’s lightweight, professional, and perfect for mini-projects or viva demos.

---

## 🧱 2. Folder Structure

Your project folder (e.g., `C:\Users\Admin\Desktop\SQL`) should contain:

```
📂 BankSystemProject
 ├── setup_db.py          # Creates the SQLite database
 ├── bank_ui.py           # Streamlit app (frontend)
 ├── bank_system.db       # Auto-generated database file (after running setup)
 └── README.txt / guide.txt  # (optional) Documentation file
```

---

## ⚙️ 3. Installation & Setup Steps

### Step 1: Install Python

Make sure **Python 3.10+** is installed.
To check:

```bash
python --version
```

If not, download it from: [https://www.python.org/downloads](https://www.python.org/downloads)

---

### Step 2: Install Required Libraries

Open your terminal (Command Prompt / VS Code terminal) and run:

```bash
pip install streamlit pandas
```

These are the only two dependencies needed (SQLite is built into Python).

---

### Step 3: Create Database

Before running the app, initialize the database:

```bash
python setup_db.py
```

✅ Output should say:

```
✅ Database 'bank_system.db' created with all tables and sample data.
```

This creates the main database file — `bank_system.db`.

---

### Step 4: Run the Streamlit App

Now launch your app with:

```bash
streamlit run bank_ui.py
```

✅ You’ll see something like:

```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

Click the link (or open it manually in your browser).

---

## 🔐 5. Login Credentials

Default admin login:

```
Username: admin
Password: admin123
```

Optional: you can create more users manually using Python:

```python
import sqlite3
conn = sqlite3.connect("bank_system.db")
cur = conn.cursor()
cur.execute("INSERT INTO Login_Info VALUES (?, ?, ?)", ("staff1", "staff123", "Staff"))
conn.commit()
conn.close()
```

---

## 🧭 6. How to Use the App

Once you log in, you’ll see a **sidebar menu**:

| Menu                       | Description                             |
| -------------------------- | --------------------------------------- |
| 🏠 **Dashboard**           | Overview of total accounts and balance  |
| ➕ **Create Account**       | Add a new customer account              |
| 💰 **Deposit**             | Add money to an existing account        |
| 💸 **Withdraw**            | Withdraw money if balance is sufficient |
| 🔍 **Search Account**      | Find a specific account by number       |
| 📜 **Transaction History** | View deposits & withdrawals per account |
| 📊 **View All Accounts**   | List all customers in a sortable table  |
| 🚪 **Logout**              | Securely log out                        |

---

## 📊 7. Database Tables (Schema Overview)

| Table Name        | Purpose                                |
| ----------------- | -------------------------------------- |
| `Branch_Info`     | Stores branch details                  |
| `Account_Info`    | Stores customer account data           |
| `Deposit_Info`    | Records deposit transactions           |
| `Withdrawal_Info` | Records withdrawal transactions        |
| `Login_Info`      | Stores login credentials (Admin/Staff) |

---

## 🧰 8. Technical Summary

| Component            | Description                              |
| -------------------- | ---------------------------------------- |
| **Frontend**         | Streamlit (Python web framework)         |
| **Backend Database** | SQLite (local file `bank_system.db`)     |
| **Language**         | Python                                   |
| **Dependencies**     | `streamlit`, `pandas`                    |
| **Storage**          | Persistent local DB (no server required) |
| **Platform**         | Cross-platform (Windows / macOS / Linux) |

---

## 🧪 9. Common Issues & Fixes

| Problem                                                           | Solution                                                         |
| ----------------------------------------------------------------- | ---------------------------------------------------------------- |
| ❌ `File does not exist: bank_ui.py`                               | Make sure you are in the correct folder before running Streamlit |
| ❌ `AttributeError: streamlit has no attribute experimental_rerun` | Replace `st.experimental_rerun()` with `st.rerun()`              |
| ❌ `Invalid credentials`                                           | Use `admin / admin123` or insert a new login manually            |
| ❌ Tables missing                                                  | Run `python setup_db.py` again to recreate them                  |
| ❌ Database not found                                              | Ensure `bank_system.db` is in the same folder as `bank_ui.py`    |

---

## 🎯 10. Project Demo Summary

**Steps to demonstrate:**

1. Login as admin → verify authentication works
2. Go to “Create Account” → create a few sample users
3. Make a deposit and withdrawal → balance updates automatically
4. Search for that account → verify details
5. View “Transaction History” → show recorded deposits/withdrawals
6. Show “View All Accounts” → displays all customers
7. Logout → access is locked again

This gives a full demonstration of banking system flow.

---

## 🏁 11. Optional Enhancements

Want to make it next-level? You can add:

* Transaction graphs (using Plotly or Matplotlib)
* Account editing / deletion
* PDF receipt generation after each transaction
* Multi-branch login (different branches, different users)
* Email notifications using `smtplib`

---

## ✅ Summary

| Step                 | Command                           |
| -------------------- | --------------------------------- |
| Install dependencies | `pip install streamlit pandas`    |
| Create database      | `python setup_db.py`              |
| Run the app          | `streamlit run bank_ui.py`        |
| Login                | `admin / admin123`                |
| Database file        | `bank_system.db` (auto-generated) |

---

Would you like me to generate a **ready-to-download PDF version** of this guide (formatted with proper headings, logos, and sections) so you can attach it to your mini-project report?
