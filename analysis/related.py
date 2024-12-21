# analysis/related.py
from db.queries import get_connection

def find_related_notes(note_id, threshold=1):
    conn = get_connection()
    c = conn.cursor()
    # Estrai i tag della nota corrente
    c.execute("SELECT tag FROM tags WHERE note_id=?", (note_id,))
    current_tags = set([row[0] for row in c.fetchall()])

    if not current_tags:
        conn.close()
        return []

    # Trova note con tag simili
    placeholders = ','.join('?' for _ in current_tags)
    query = f"SELECT note_id, tag FROM tags WHERE tag IN ({placeholders})"
    c.execute(query, tuple(current_tags))
    tag_map = {}
    for row in c.fetchall():
        nid, tg = row
        if nid != note_id:
            tag_map.setdefault(nid, set()).add(tg)
    conn.close()

    # Filtra note con almeno `threshold` tag in comune
    related = [nid for nid, tgs in tag_map.items() if len(tgs) >= threshold]
    return related
