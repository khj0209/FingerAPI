import sqlite3

def init_db():
    conn = sqlite3.connect("./backend/users.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        finger_id TEXT PRIMARY KEY,
        balance INTEGER
    )
    """)
    cur.executemany("INSERT OR REPLACE INTO users VALUES (?, ?)", [
        ('1', 5000),
        ('2', 1000),
        ('3', 3000)
    ])
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
