# db.py
import sqlite3
from datetime import datetime

# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect("conversations.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conv_id TEXT,
            role TEXT,
            message TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Save a message to the database
def save_message_to_db(conv_id, role, message):
    conn = sqlite3.connect("conversations.db")
    c = conn.cursor()
    c.execute('''
        INSERT INTO conversations (conv_id, role, message, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (conv_id, role, message, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def load_conversation(conv_id):
    conn = sqlite3.connect("conversations.db")
    c = conn.cursor()
    c.execute('''
        SELECT role, message FROM conversations
        WHERE conv_id = ?
        ORDER BY timestamp ASC
    ''', (conv_id,))
    rows = c.fetchall()
    conn.close()
    return [{"role": role, "content": message} for (role, message) in rows]

def list_conversations():
    conn = sqlite3.connect("conversations.db")
    c = conn.cursor()
    c.execute('''
        SELECT conv_id, MIN(timestamp) as first_message_time
        FROM conversations
        GROUP BY conv_id
        ORDER BY first_message_time ASC
    ''')
    rows = c.fetchall()
    conn.close()
    return [row[0] for row in rows]


