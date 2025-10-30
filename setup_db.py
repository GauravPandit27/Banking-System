import sqlite3

conn = sqlite3.connect("bank_system.db")
cur = conn.cursor()

cur.executescript("""
DROP TABLE IF EXISTS Branch_Info;
DROP TABLE IF EXISTS Account_Info;
DROP TABLE IF EXISTS Deposit_Info;
DROP TABLE IF EXISTS Withdrawal_Info;
DROP TABLE IF EXISTS Login_Info;

CREATE TABLE Branch_Info (
    Branch_No TEXT PRIMARY KEY,
    Branch_Name TEXT NOT NULL,
    City TEXT
);

CREATE TABLE Account_Info (
    Account_No INTEGER PRIMARY KEY AUTOINCREMENT,
    Branch_No TEXT,
    Name TEXT NOT NULL,
    Gender TEXT,
    DOB TEXT,
    Address TEXT,
    Phone TEXT,
    Email TEXT,
    Balance REAL DEFAULT 0,
    FOREIGN KEY (Branch_No) REFERENCES Branch_Info(Branch_No)
);

CREATE TABLE Deposit_Info (
    Deposit_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Account_No INTEGER,
    Amount REAL,
    Deposit_Date TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Account_No) REFERENCES Account_Info(Account_No)
);

CREATE TABLE Withdrawal_Info (
    Withdrawal_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Account_No INTEGER,
    Amount REAL,
    Withdrawal_Date TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Account_No) REFERENCES Account_Info(Account_No)
);

CREATE TABLE Login_Info (
    Username TEXT PRIMARY KEY,
    Password TEXT NOT NULL,
    Role TEXT CHECK (Role IN ('Admin','Staff'))
);

INSERT INTO Branch_Info VALUES ('B001', 'Pune Branch', 'Pune');
INSERT INTO Login_Info VALUES ('admin', 'admin123', 'Admin');
""")

conn.commit()
print("✅ Database 'bank_system.db' created with all tables and sample data.")
conn.close()
