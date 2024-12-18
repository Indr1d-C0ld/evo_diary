# db/queries.py
import sqlite3

def get_connection(db_path='notes.db'):
    return sqlite3.connect(db_path)

def insert_note(text, category=None, db_path='notes.db'):
    conn = get_connection(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO notes (text, category) VALUES (?,?)", (text, category))
    note_id = c.lastrowid
    conn.commit()
    conn.close()
    return note_id

def insert_tags(note_id, tags, db_path='notes.db'):
    conn = get_connection(db_path)
    c = conn.cursor()
    for tag in tags:
        c.execute("INSERT INTO tags (note_id, tag) VALUES (?,?)", (note_id, tag))
    conn.commit()
    conn.close()

def insert_link(note_id1, note_id2, rel_type='related', db_path='notes.db'):
    conn = get_connection(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO links (note_id1, note_id2, rel_type) VALUES (?,?,?)", (note_id1, note_id2, rel_type))
    conn.commit()
    conn.close()

def list_notes(db_path='notes.db'):
    conn = get_connection(db_path)
    c = conn.cursor()
    c.execute("SELECT id, timestamp, text, category FROM notes ORDER BY timestamp DESC")
    rows = c.fetchall()
    conn.close()
    return rows

def search_notes(keyword, db_path='notes.db'):
    conn = get_connection(db_path)
    c = conn.cursor()
    query = "SELECT id, timestamp, text, category FROM notes WHERE text LIKE ? ORDER BY timestamp DESC"
    c.execute(query, ('%' + keyword + '%',))
    rows = c.fetchall()
    conn.close()
    return rows
