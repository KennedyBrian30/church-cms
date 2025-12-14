import sqlite3
import os

DB_NAME = "/data/chms.db" if os.path.exists("/data") else "chms.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.executescript("""
    CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT
    );

    CREATE TABLE IF NOT EXISTS funds (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS pledge_campaigns (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS pledges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id INTEGER,
        campaign_id INTEGER,
        pledged_amount REAL,
        FOREIGN KEY (member_id) REFERENCES members(id),
        FOREIGN KEY (campaign_id) REFERENCES pledge_campaigns(id)
    );

    CREATE TABLE IF NOT EXISTS contributions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id INTEGER,
        fund_id INTEGER,
        amount REAL,
        contribution_date DATE,
        payment_method TEXT,
        memo TEXT,
        FOREIGN KEY (member_id) REFERENCES members(id),
        FOREIGN KEY (fund_id) REFERENCES funds(id)
    );

    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        date DATE,
        attendees INTEGER
    );
    """)

    conn.commit()
    conn.close()
