import sqlite3
import json
from datetime import datetime, timezone
import os

DB_PATH = 'data/events.db'

# First, the function to initialize the sqlite db
def init_db(recreate=False):
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if not os.path.exists(DB_PATH):
        print(f"Creating database at {DB_PATH}")
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            if recreate:
                cursor.execute('DROP TABLE IF EXISTS events')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    details TEXT
                )
            ''')
            conn.commit()
    except sqlite3.Error as e:
        print(f"Error initializing DB: {e}")

def log_event(event_type, details=None):
    try:
        if details is not None and not isinstance(details, (dict, list, str, int, float, bool, type(None))):
            raise ValueError("Details must be serializable as JSON.")
        details_str = json.dumps(details) if details else None
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            timestamp = datetime.now(timezone.utc).isoformat()
            details_str = json.dumps(details) if details else None
            cursor.execute('''
                INSERT INTO events (event_type, timestamp, details)
                VALUES (?, ?, ?)
            ''', (event_type, timestamp, details_str))
            conn.commit()
    except (sqlite3.Error, ValueError) as e:
        raise Exception(f"Error when loggin event: {e}")

def get_events(limit=None):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            query = 'SELECT * FROM events ORDER BY timestamp DESC'
            if limit is not None:
                query += f' LIMIT {limit}'
            return cursor.fetchall()
    except sqlite3.Error as e:
        raise Exception(f"Error when querying events: {e}")

# Test for the functions above
if __name__ == "__main__":
    init_db(recreate=True)
    log_event("detection", {"persons_count": 2, "dominant_color": "RGB(255, 0, 0)"})
    log_event("pause", {"reason": "QR detected"})
    log_event("resume", {"reason": "UI button"})
    events = get_events(limit=5)
    print("Events logged:")
    for event in events:
        print(event)
    print("Test concluded.")
