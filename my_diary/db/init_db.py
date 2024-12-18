# db/init_db.py
import sqlite3
import os

def init_db(db_path='notes.db'):
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE notes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        text TEXT,
                        category TEXT
                    )''')
        c.execute('''CREATE TABLE tags (
                        note_id INTEGER,
                        tag TEXT,
                        FOREIGN KEY(note_id) REFERENCES notes(id)
                    )''')
        c.execute('''CREATE TABLE links (
                        note_id1 INTEGER,
                        note_id2 INTEGER,
                        rel_type TEXT,
                        FOREIGN KEY(note_id1) REFERENCES notes(id),
                        FOREIGN KEY(note_id2) REFERENCES notes(id)
                    )''')
        conn.commit()
        conn.close()
    else:
        print("Database già esistente.")
