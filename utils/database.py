
import sqlite3
import os

# Base project directory
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

# Database folder
DATABASE_DIR = os.path.join(
    BASE_DIR,
    "database"
)

# Create database folder
os.makedirs(DATABASE_DIR, exist_ok=True)

# Database file path
DB_PATH = os.path.join(
    DATABASE_DIR,
    "chat_history.db"
)

# Connect SQLite
conn = sqlite3.connect(
    DB_PATH,
    check_same_thread=False
)

cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS chats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT,
    answer TEXT
)
""")

conn.commit()


def save_chat(question, answer):

    cursor.execute(
        "INSERT INTO chats(question, answer) VALUES (?, ?)",
        (question, answer)
    )

    conn.commit()


def get_history():

    cursor.execute("SELECT * FROM chats")

    return cursor.fetchall()