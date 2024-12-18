# analysis/trends.py
from db.queries import get_connection
import collections

def trending_keywords(last_n=50):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT tag FROM tags JOIN notes ON tags.note_id=notes.id ORDER BY notes.timestamp DESC LIMIT ?", (last_n,))
    tags = [row[0] for row in c.fetchall()]
    conn.close()
    counter = collections.Counter(tags)
    return counter.most_common(5) # top 5 parole chiave

def suggest_next_topic():
    trends = trending_keywords()
    if not trends:
        return None
    # Semplice suggerimento: la keyword più frequente
    return f"Forse potresti approfondire il tema: {trends[0][0]}"
