import sqlite3
import json
from datetime import datetime, timezone
import os

DB_PATH = 'data/events.db'

# First, the function to initialize the sqlite db     
def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
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
        print(f"Erro ao inicializar DB: {e}")

def log_event(event_type, details=None):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            timestamp = datetime.now(timezone.utc).isoformat()
            details_str = json.dumps(details) if details else None
            cursor.execute('''
                INSERT INTO events (event_type, timestamp, details)
                VALUES (?, ?, ?)
            ''', (event_type, timestamp, details_str))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao logar evento: {e}")

def get_events():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM events ORDER BY timestamp DESC')
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao consultar eventos: {e}")
        return []
    
# Test for the functions above
if __name__ == "__main__":
    init_db()
    log_event("detection", {"persons_count": 2, "color": "blue", "action": "walking"})
    log_event("pause", {"reason": "QR detected"})
    events = get_events()
    print("Eventos logados:")
    for event in events:
        print(event)
    print("Teste concluido.")