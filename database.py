# database.py
import sqlite3

DB_NAME = "/data/chms.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.executescript("""
    -- MEMBERS
    CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE
    );

    -- FUNDS
    CREATE TABLE IF NOT EXISTS funds (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );

    -- PLEDGE CAMPAIGNS
    CREATE TABLE IF NOT EXISTS pledge_campaigns (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        year INTEGER NOT NULL
    );

    -- PLEDGES
    CREATE TABLE IF NOT EXISTS pledges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id INTEGER NOT NULL,
        campaign_id INTEGER NOT NULL,
        pledged_amount REAL NOT NULL,
        FOREIGN KEY (member_id) REFERENCES members(id),
        FOREIGN KEY (campaign_id) REFERENCES pledge_campaigns(id)
    );

    -- CONTRIBUTIONS
    CREATE TABLE IF NOT EXISTS contributions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id INTEGER NOT NULL,
        fund_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        contribution_date DATE NOT NULL,
        payment_method TEXT,
        memo TEXT,
        FOREIGN KEY (member_id) REFERENCES members(id),
        FOREIGN KEY (fund_id) REFERENCES funds(id)
    );

    -- EVENTS
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        event_date DATE NOT NULL,
        attendees INTEGER DEFAULT 0
    );

    -- GROUPS
    CREATE TABLE IF NOT EXISTS groups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );
    """)

    conn.commit()
    conn.close()
