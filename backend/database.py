import sqlite3

def init_db():
    conn = sqlite3.connect("./users.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        finger_id TEXT PRIMARY KEY,
        phone_last4 TEXT,
        balance INTEGER
    )
    """)
    cur.executemany("INSERT OR REPLACE INTO users VALUES (?, ?, ?)", [
        ('1', '1234', 5000),
        ('2', '5678', 1000),
        ('3', '9999', 3000)
    ])
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
